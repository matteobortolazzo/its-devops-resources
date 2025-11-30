import torch
import torch.optim as optim
from environment import GridWorld, Action
from model import PolicyNet, BigPolicyNet

def run_episode_reinforce(env, model, max_steps=50, gamma=0.99, entropy_coef=0.01):
    log_probs = []
    rewards = []
    entropies = []

    state = env.reset()
    done = False
    for t in range(max_steps): # t is just a step counter
        s_t = torch.from_numpy(state).unsqueeze(0)
        logits = model(s_t) # Run the model
        probs = torch.softmax(logits, dim=-1) # Get probabilities for each action
        dist = torch.distributions.Categorical(probs) # Wrap them in a distribution to have sample() and log_prob() methods

        sampled_action = dist.sample()
        log_prob = dist.log_prob(sampled_action)
        entropy = dist.entropy() # Bonus for exploration

        action = Action(sampled_action.item())
        next_state, reward, done, _ = env.step(action) # Execute the action

        log_probs.append(log_prob)
        rewards.append(reward)
        entropies.append(entropy)
        state = next_state

        if done:
            break

    if not done and len(rewards) >= max_steps:
        rewards[-1] -= 1  # Penalty for timeout

    returns = [] # List of cumulative rewards at each time step
    G = 0.0 # Cumulative reward at the current time step
    for reward in reversed(rewards):
        # Reward discounted the older it is. This is because future rewards are less important.
        G = reward + gamma * G
        returns.insert(0, G)

    returns = torch.tensor(returns, dtype=torch.float32)

    # Normalize returns for stability
    if len(returns) > 1 and returns.std() > 1e-6:
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    policy_loss = -torch.sum(torch.stack(log_probs) * returns)
    entropy_loss = -entropy_coef * torch.sum(torch.stack(entropies))
    loss = policy_loss + entropy_loss

    total_reward = sum(rewards)
    return loss, total_reward


def train_reinforce_learning():
    print("=== Reinforcement Learning (REINFORCE) ===")
    env = GridWorld()
    model = BigPolicyNet() # PolicyNet()
    opt = optim.Adam(model.parameters(), lr=3e-3) # Standard optimizer with 0.01 learning rate

    # Track running average for monitoring
    running_reward = None
    best_reward = float('-inf')

    for episode in range(2000):
        loss, total_reward = run_episode_reinforce(env, model, entropy_coef=0.02)

        opt.zero_grad() # Clear gradients for the next train step
        loss.backward() # Compute gradients based on loss
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0) # Prevent exploding gradients
        opt.step() # Update model parameters to minimize loss

        # Track running average
        if running_reward is None:
            running_reward = total_reward
        else:
            running_reward = 0.95 * running_reward + 0.05 * total_reward

        if total_reward > best_reward:
            best_reward = total_reward

        if (episode + 1) % 100 == 0:
            print(f"Episode {episode+1:4d} | reward={total_reward:6.2f} | "
                  f"running={running_reward:6.2f} | best={best_reward:6.2f} | loss={loss.item():.3f}")

    return env, model
