import copy
import numpy as np
import torch
from environment import GridWorld, Action
from model import WalkBrain

def evaluate_policy(env, model, episodes=5, max_steps=50):
    total = 0.0
    for _ in range(episodes):
        state = env.reset()
        ep_reward = 0.0
        for _ in range(max_steps):
            s_t = torch.from_numpy(state).unsqueeze(0)
            with torch.no_grad():
                logits = model(s_t) # Run the model
                action_index = torch.argmax(logits, dim=-1).item() # Choose action with the highest probability
                action = Action(action_index)
            state, reward, done, _ = env.step(action)
            ep_reward += reward
            if done:
                break
        total += ep_reward
    return total / episodes


def mutate(model, sigma=0.1):
    child = copy.deepcopy(model)
    with torch.no_grad():
        # For each parameter of the child, add Gaussian noise with standard deviation sigma
        for p in child.parameters():
            p.add_(sigma * torch.randn_like(p))
    return child

def train_evolution(env, hidden=32):
    print("=== Neuroevolution ===")
    pop_size = 20
    elite_frac = 0.2
    sigma = 0.1
    generations = 50

    population = [(WalkBrain(hidden=hidden)) for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [evaluate_policy(env, ind) for ind in population]

        # Sort individuals by fitness, best first
        ranked = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)

        # Get the best individual
        best_fitness = ranked[0][1]
        print(f"Gen {gen:2d} | best fitness={best_fitness:.3f}")

        # Get the best individuals (elites)
        n_elite = max(1, int(elite_frac * pop_size))
        elites = [ind for ind, _ in ranked[:n_elite]]

        new_pop = elites.copy()
        while len(new_pop) < pop_size:
            parent = np.random.choice(elites)
            child = mutate(parent, sigma=sigma)
            new_pop.append(child)

        population = new_pop

    # Get the best individual
    fitnesses = [evaluate_policy(env, ind) for ind in population]
    best_idx = int(np.argmax(fitnesses))
    print("Final best fitness:", fitnesses[best_idx])
    return env, population[best_idx]
