import torch.nn as nn
import torch
import torch.optim as optim
from environment import GridWorld, Action

class ActorCritic(nn.Module):
    def __init__(self, input_dim=6, hidden=64, n_actions=4):
        super().__init__()
        # Shared feature extractor
        self.shared = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
        )
        # Actor: outputs action logits
        self.actor = nn.Linear(hidden, n_actions)
        # Critic: outputs state value estimate
        self.critic = nn.Linear(hidden, 1)

    def forward(self, x):
        shared = self.shared(x)
        return self.actor(shared), self.critic(shared)


def run_episode_ac(env, model, max_steps=100, gamma=0.99):
    log_probs = []
    values = []
    rewards = []
    entropies = []

    state = env.reset()

    for t in range(max_steps):
        s_t = torch.from_numpy(state).unsqueeze(0)
        logits, value = model(s_t)  # Get both policy and value

        probs = torch.softmax(logits, dim=-1)
        dist = torch.distributions.Categorical(probs)

        action = dist.sample()
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()  # Encourages exploration

        next_state, reward, done, _ = env.step(Action(action.item()))

        log_probs.append(log_prob)
        values.append(value)
        rewards.append(reward)
        entropies.append(entropy)
        state = next_state

        if done:
            break

    # Compute actual returns (Monte Carlo)
    returns = []
    G = 0.0
    for reward in reversed(rewards):
        G = reward + gamma * G
        returns.insert(0, G)

    returns = torch.tensor(returns, dtype=torch.float32).unsqueeze(1)
    values = torch.cat(values)

    # Advantage = actual - predicted
    advantages = returns - values.detach()  # Don't backprop through critic's predictions

    # Actor loss: maximize log_prob weighted by advantage
    actor_loss = -torch.sum(torch.stack(log_probs) * advantages.squeeze())

    # Critic loss: minimize TD error
    critic_loss = torch.nn.functional.mse_loss(values, returns)

    # Entropy bonus: encourages exploration
    entropy_loss = -0.01 * sum(entropies)

    # Combined loss
    loss = actor_loss + 0.5 * critic_loss + entropy_loss

    return loss, sum(rewards)


def train_actor_critic():
    print("=== Reinforcement Learning (Actor-Critic) ===")
    env = GridWorld()
    model = ActorCritic()
    opt = optim.Adam(model.parameters(), lr=3e-4)

    for episode in range(2000):
        loss, total_reward = run_episode_ac(env, model)

        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        opt.step()

        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1:4d} | reward={total_reward:.2f} | loss={loss.item():.3f}")

    return env, model