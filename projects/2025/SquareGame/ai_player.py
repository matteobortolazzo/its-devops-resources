import torch
import torch.nn as nn
import copy
import random

class DodgeNet(nn.Module):
    """Neural network for the AI player"""
    def __init__(self, input_size=8, hidden_size=16):
        super(DodgeNet, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 3)  # Output: [left, stay, right]
        )

    def forward(self, x):
        return self.network(x)

    def get_action(self, state):
        """Get action from network output"""
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            output = self.forward(state_tensor)
            action = torch.argmax(output, dim=1).item()
        return action  # 0=left, 1=stay, 2=right


class AIAgent:
    """An AI agent with its own neural network"""
    def __init__(self, network=None):
        if network is None:
            self.network = DodgeNet()
        else:
            self.network = network
        self.fitness = 0
        self.score = 0

    def get_action(self, state):
        return self.network.get_action(state)

    def clone(self):
        """Create a copy of this agent"""
        new_network = DodgeNet()
        new_network.load_state_dict(copy.deepcopy(self.network.state_dict()))
        return AIAgent(new_network)

    def mutate(self, mutation_rate=0.1, mutation_scale=0.3):
        """Mutate the network weights"""
        with torch.no_grad():
            for param in self.network.parameters():
                if random.random() < mutation_rate:
                    noise = torch.randn_like(param) * mutation_scale
                    param.add_(noise)


class NeuroEvolution:
    """Genetic algorithm for evolving neural networks"""
    def __init__(self, population_size=50, elite_size=10):
        self.population_size = population_size
        self.elite_size = elite_size
        self.population = [AIAgent() for _ in range(population_size)]
        self.generation = 0
        self.best_fitness = 0
        self.best_agent = None

    def evolve(self):
        """Evolve the population to the next generation"""
        # Sort by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Track best agent
        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_agent = self.population[0].clone()

        # Keep elite agents
        new_population = []
        for i in range(self.elite_size):
            new_population.append(self.population[i].clone())

        # Create offspring from elite agents
        while len(new_population) < self.population_size:
            # Select parent from elite pool
            parent = random.choice(self.population[:self.elite_size])
            child = parent.clone()

            # Mutate child
            mutation_rate = 0.2
            mutation_scale = 0.3
            child.mutate(mutation_rate, mutation_scale)

            new_population.append(child)

        self.population = new_population
        self.generation += 1

        # Reset fitness for new generation
        for agent in self.population:
            agent.fitness = 0
            agent.score = 0

    def get_population(self):
        return self.population

    def get_best_agent(self):
        return self.best_agent if self.best_agent else self.population[0]

    def save_best(self, filepath):
        """Save the best agent's network"""
        if self.best_agent:
            torch.save(self.best_agent.network.state_dict(), filepath)
            print(f"Saved best agent to {filepath}")

    def load_agent(self, filepath):
        """Load an agent from file"""
        network = DodgeNet()
        network.load_state_dict(torch.load(filepath))
        return AIAgent(network)

