import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from environment import GridWorld, Action
from model import PolicyNet

def expert_action(state, env: GridWorld):
    """
    Simple heuristic expert:
    - Move towards goal (4,4)
    - Avoid stepping into lava (2,2) if possible
    - Actions: 0=up,1=down,2=left,3=right
    """
    size = env.size
    x = int(round(state[0] * (size - 1))) # From float back to int
    y = int(round(state[1] * (size - 1))) # From float back to int
    goal_x, goal_y = env.goal
    lava_x, lava_y = env.lava

    possible_actions = []

    # Try to reduce x distance to goal
    if x < goal_x:
        possible_actions.append(Action.RIGHT)
    elif x > goal_x:
        possible_actions.append(Action.LEFT)

    # Try to reduce y distance to goal
    if y < goal_y:
        possible_actions.append(Action.UP)
    elif y > goal_y:
        possible_actions.append(Action.DOWN)

    if not possible_actions:
        possible_actions = [0]  # arbitrary, already at goal

    # Avoid stepping into the lava, if possible
    for action in possible_actions:
        next_x, next_y = x, y
        if action == Action.UP:
            next_y += 1
        elif action == Action.DOWN:
            next_y -= 1
        elif action == Action.LEFT:
            next_x -= 1
        elif action == Action.RIGHT:
            next_x += 1
        if (next_x, next_y) != (lava_x, lava_y):
            return action

    return possible_actions[0]


def generate_supervised_data(env, n_samples=500):
    X, y = [], []
    for _ in range(n_samples):
        # random non-terminal position
        while True:
            x_coord = np.random.randint(0, env.size)
            y_coord = np.random.randint(0, env.size)
            if (x_coord, y_coord) not in (env.goal, env.lava):
                break
        env.pos = (x_coord, y_coord)
        state = env.get_state()
        action = expert_action(state, env)
        X.append(state)
        y.append(action.value)

    # X (N x array(6)) is converted to matrix(N, 6)
    # y (N x int) is converted to array(N)
    return np.stack(X), np.array(y, dtype=np.int64) # PyTorch needs int64 for targets


def train_supervised():
    print("=== Supervised Learning ===")
    env = GridWorld()
    X, y = generate_supervised_data(env)
    X_t = torch.from_numpy(X) # Convert X to PyTorch tensor
    y_t = torch.from_numpy(y) # Convert Y to PyTorch tensor

    model = PolicyNet()
    opt = optim.Adam(model.parameters(), lr=1e-2) # Standard optimizer with 0.01 learning rate
    loss_fn = nn.CrossEntropyLoss() # Standard loss function for classification (0,1,2,3)

    for epoch in range(100):
        logits = model(X_t) ## matrix(500, 4)
        loss = loss_fn(logits, y_t)

        opt.zero_grad() # Clear gradients for the next train step
        loss.backward() # Compute gradients based on loss
        opt.step() # Update model parameters to minimize loss

        # Print progress
        if (epoch + 1) % 20 == 0:
            predicted_action = logits.argmax(dim=1) # array(500), find index of the action with the highest probability
            accuracy = ((predicted_action == y_t) # Get if predicted action equals true action
                        .float() # Convert bool to float (1.0/0.0)
                        .mean() # Calculate mean of all elements
                        .item()) # Convert float to native Python float
            print(f"Epoch {epoch+1:3d} | loss={loss.item():.3f} | acc={accuracy:.2f}")

    return env, model
