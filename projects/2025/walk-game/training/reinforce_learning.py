import torch
import torch.optim as optim
from environment import GridWorld
from model import PolicyNet

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


def train_reinforce_learning():
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
