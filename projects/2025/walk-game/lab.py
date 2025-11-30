import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


# ---------------------------
# Environment: 5x5 GridWorld
# ---------------------------
class GridWorld:
    """
    5x5 grid:
    - Start at (0,0)
    - Goal at (4,4)
    - Lava at (2,2)
    Actions: 0=up,1=down,2=left,3=right
    """

    def __init__(self, size=5):
        self.pos = (0, 0)
        self.size = size
        self.goal = (size - 1, size - 1)
        self.lava = (2, 2)
        self.reset()

    def reset(self):
        self.pos = (0, 0)
        return self.get_state()

    def get_state(self):
        x, y = self.pos
        goal_x, goal_y = self.goal
        lava_x, lava_y = self.lava
        # Convert to an array of floats in range [0,1]
        state = np.array([x, y, goal_x, goal_y, lava_x, lava_y], dtype=np.float32) / (self.size - 1)
        return state

    def step(self, action):
        x, y = self.pos

        # 0=up,1=down,2=left,3=right
        if action == 0 and y > 0:
            y -= 1
        elif action == 1 and y < self.size - 1:
            y += 1
        elif action == 2 and x > 0:
            x -= 1
        elif action == 3 and x < self.size - 1:
            x += 1

        self.pos = (x, y)

        reward = -0.01  # small step penalty
        done = False

        if self.pos == self.lava:
            reward = -1.0
            done = True
        elif self.pos == self.goal:
            reward = 1.0
            done = True

        return self.get_state(), reward, done, {}


# -----------------------------------------
# Shared neural network policy (PyTorch)
# -----------------------------------------
class PolicyNet(nn.Module):
    def __init__(self, input_dim=6, hidden=32, n_actions=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, x):
        return self.net(x)


# -----------------------------------------
# 1) Supervised learning: imitate expert
# -----------------------------------------
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
        possible_actions.append(3)  # right
    elif x > goal_x:
        possible_actions.append(2)  # left

    # Try to reduce y distance to goal
    if y < goal_y:
        possible_actions.append(1)  # down
    elif y > goal_y:
        possible_actions.append(0)  # up

    if not possible_actions:
        possible_actions = [0]  # arbitrary, already at goal

    # Avoid stepping into the lava, if possible
    for action in possible_actions:
        next_x, next_y = x, y
        if action == 0:
            next_y -= 1
        elif action == 1:
            next_y += 1
        elif action == 2:
            next_x -= 1
        elif action == 3:
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
        y.append(action)
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


# -----------------------------------------
# 2) Reinforcement Learning (REINFORCE)
# -----------------------------------------
def run_episode_reinforce(env, model, max_steps=50, gamma=0.99):
    log_probs = []
    rewards = []

    state = env.reset()
    done = False
    for t in range(max_steps): # t is just a step counter
        s_t = torch.from_numpy(state).unsqueeze(0)
        logits = model(s_t) # Run the model
        probs = torch.softmax(logits, dim=-1) # Convert logits to probabilities (the sum is 1)
        dist = torch.distributions.Categorical(probs) # Wrap them in a distribution to have sample() and log_prob() methods

        action = dist.sample()
        log_prob = dist.log_prob(action)

        next_state, reward, done, _ = env.step(action.item()) # Execute the action

        log_probs.append(log_prob)
        rewards.append(reward)
        state = next_state

        if done:
            break

    if not done and len(rewards) >= max_steps:
        rewards[-1] -= 0.5  # Penalty for timeout

    returns = [] # List of cumulative rewards at each time step
    G = 0.0 # Cumulative reward at the current time step
    for reward in reversed(rewards):
        # Reward discounted the older it is. This is because future rewards are less important.
        G = reward + gamma * G
        returns.insert(0, G)

    returns = torch.tensor(returns, dtype=torch.float32)

    # Only normalize if there's variance, otherwise use raw returns
    if returns.std() > 1e-6:
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    loss = -torch.sum(torch.stack(log_probs) * returns)
    total_reward = sum(rewards)
    return loss, total_reward


def train_reinforce():
    print("=== Reinforcement Learning (REINFORCE) ===")
    env = GridWorld()
    model = PolicyNet()
    opt = optim.Adam(model.parameters(), lr=1e-2) # Standard optimizer with 0.01 learning rate

    for episode in range(500):
        loss, total_reward = run_episode_reinforce(env, model)

        opt.zero_grad() # Clear gradients for the next train step
        loss.backward() # Compute gradients based on loss
        opt.step() # Update model parameters to minimize loss

        if (episode + 1) % 50 == 0:
            print(f"Episode {episode+1:3d} | reward={total_reward:.2f} | loss={loss.item():.3f}")

    return env, model


# -----------------------------------------
# 3) Neuroevolution: evolve weights
# -----------------------------------------
def evaluate_policy(env, model, episodes=5, max_steps=50):
    total = 0.0
    for _ in range(episodes):
        state = env.reset()
        ep_reward = 0.0
        for _ in range(max_steps):
            s_t = torch.from_numpy(state).unsqueeze(0)
            with torch.no_grad():
                logits = model(s_t)
                action = torch.argmax(logits, dim=-1).item()
            state, reward, done, _ = env.step(action)
            ep_reward += reward
            if done:
                break
        total += ep_reward
    return total / episodes


def mutate(model, sigma=0.1):
    child = copy.deepcopy(model)
    with torch.no_grad():
        for p in child.parameters():
            p.add_(sigma * torch.randn_like(p))
    return child


def train_evolution():
    print("=== Neuroevolution ===")
    env = GridWorld()
    pop_size = 20
    elite_frac = 0.2
    sigma = 0.1
    generations = 50

    population = [PolicyNet() for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [evaluate_policy(env, ind) for ind in population]
        ranked = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        best_fitness = ranked[0][1]

        print(f"Gen {gen:2d} | best fitness={best_fitness:.3f}")

        n_elite = max(1, int(elite_frac * pop_size))
        elites = [ind for ind, _ in ranked[:n_elite]]

        new_pop = elites.copy()
        while len(new_pop) < pop_size:
            parent = np.random.choice(elites)
            child = mutate(parent, sigma=sigma)
            new_pop.append(child)

        population = new_pop

    # final best individual
    fitnesses = [evaluate_policy(env, ind) for ind in population]
    best_idx = int(np.argmax(fitnesses))
    print("Final best fitness:", fitnesses[best_idx])
    return env, population[best_idx]


# -----------------------------------------
# Simple rollout viewer
# -----------------------------------------
def demo_run(env, model, max_steps=20):
    print("\n=== Demo run ===")
    state = env.reset()
    total_reward = 0.0
    for step in range(max_steps):
        s_t = (torch
               .from_numpy(state) # Convert state to PyTorch tensor and
               .unsqueeze(0)) # Add batch dimension (how many samples to process at once)
        with torch.no_grad(): # Disable autograd to speed up inference
            logits = model(s_t) # Run the model
            action = torch.argmax(logits, dim=-1).item() # Choose action with the highest probability
        state, reward, done, _ = env.step(action) # Execute the action
        total_reward += reward

        size = env.size
        x = int(round(state[0] * (size - 1)))
        y = int(round(state[1] * (size - 1)))
        print(f"Step {step:2d}: pos=({x},{y})  reward={reward:.2f}")

        if done:
            break
    print("Total reward:", total_reward)


if __name__ == "__main__":
    # Choose one: "supervised", "rl", "evo"
    mode = "rl"

    if mode == "supervised":
        env, model = train_supervised()
    elif mode == "rl":
        env, model = train_reinforce()
    elif mode == "evo":
        env, model = train_evolution()
    else:
        raise ValueError("Unknown mode")

    demo_run(env, model)
