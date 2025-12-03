import pygame
import random
import sys
import numpy as np
from ai_player import NeuroEvolution
import multiprocessing

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
OBJECT_WIDTH = 40
OBJECT_HEIGHT = 40
PLAYER_SPEED = 7
OBJECT_SPEED = 5
FPS = 300  # Speed up training

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Training - Dodge Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, color=BLUE):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class FallingObject:
    def __init__(self, speed_multiplier=1.0):
        self.x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
        self.y = -OBJECT_HEIGHT
        self.width = OBJECT_WIDTH
        self.height = OBJECT_HEIGHT
        self.speed = OBJECT_SPEED * speed_multiplier

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

def check_collision(player, objects):
    player_rect = player.get_rect()
    for obj in objects:
        if player_rect.colliderect(obj.get_rect()):
            return True
    return False

def get_state(player, falling_objects):
    """Extract state features for the neural network"""
    # Find closest objects
    closest_objects = sorted(falling_objects, key=lambda obj: obj.y, reverse=True)[:3]

    # Pad with dummy objects if needed
    while len(closest_objects) < 3:
        closest_objects.append(type('obj', (), {
            'x': SCREEN_WIDTH // 2,
            'y': -100,
            'speed': 0
        })())

    state = [
        player.x / SCREEN_WIDTH,  # Player position (normalized)
        player.x / SCREEN_WIDTH - 0.5,  # Player position relative to center
    ]

    # Add info about 2 closest objects
    for i in range(2):
        obj = closest_objects[i]
        state.extend([
            obj.x / SCREEN_WIDTH,  # Object x position
            obj.y / SCREEN_HEIGHT,  # Object y position
            (obj.x - player.x) / SCREEN_WIDTH,  # Relative x distance
        ])

    return state

def run_game_episode(agent, max_time=30000, render=False, explore_eps=0.0):
    """Run one game episode for an agent.
    Returns (score, quit_requested, movement_count).
    explore_eps: probability to take a random action to avoid premature convergence.
    """
    player = Player()
    falling_objects = []
    score = 0
    game_over = False
    movement_count = 0
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()

    while not game_over:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time

        # Time limit
        if elapsed > max_time:
            break

        score = elapsed // 1000

        # Calculate difficulty
        speed_multiplier = 1.0 + (score * 0.1)
        spawn_interval = max(300, 1000 - score * 30)

        # Spawn falling objects
        if current_time - last_spawn_time > spawn_interval:
            falling_objects.append(FallingObject(speed_multiplier))
            last_spawn_time = current_time

        # Update falling objects
        for obj in falling_objects[:]:
            obj.update()
            if obj.is_off_screen():
                falling_objects.remove(obj)

        # Get AI action
        state = get_state(player, falling_objects)
        action = agent.get_action(state)
        # Epsilon exploration (small random actions to escape local optima)
        if explore_eps > 0.0 and random.random() < explore_eps:
            action = random.choice([0, 1, 2])

        if action == 0:
            player.move("left")
            movement_count += 1
        elif action == 2:
            player.move("right")
            movement_count += 1
        # action == 1 means stay

        # Check collisions
        if check_collision(player, falling_objects):
            game_over = True

        # Render if requested
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score, True, movement_count

            screen.fill(WHITE)
            player.draw(GREEN)
            for obj in falling_objects:
                obj.draw()

            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

    return score, False, movement_count


def _eval_agent_score(agent_tuple):
    """Helper for multiprocessing: evaluate a single agent and return (score, movement_count)."""
    (agent, max_time, explore_eps) = agent_tuple
    score, _, movement_count = run_game_episode(agent, max_time=max_time, render=False, explore_eps=explore_eps)
    return score, movement_count


def train_ai():
    """Train the AI using neuroevolution with anti-idle incentives and exploration."""
    population_size = 50
    generations = 100
    max_time = 30000

    neuro_evo = NeuroEvolution(population_size=population_size, elite_size=10)

    running = True
    best_history = []
    for gen in range(generations):
        if not running:
            break

        # UI status
        screen.fill(WHITE)
        title = font.render("AI Training - Dodge Game", True, BLACK)
        gen_text = font.render(f"Generation {gen + 1}/{generations}", True, BLACK)
        hint = small_font.render("Evaluating agents... (multi-core)", True, GREEN)
        screen.blit(title, (20, 20))
        screen.blit(gen_text, (20, 60))
        screen.blit(hint, (20, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        population = neuro_evo.get_population()

        # Small exploration in early generations, then decay
        explore_eps = max(0.0, 0.2 - 0.002 * gen)  # starts 0.2, ~0 by gen 100

        # Parallel evaluation
        results = []
        try:
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
                inputs = [(agent, max_time, explore_eps) for agent in population]
                results = pool.map(_eval_agent_score, inputs)
        except Exception:
            # Fallback sequential
            for agent in population:
                score, quit_requested, movement_count = run_game_episode(agent, max_time=max_time, render=False, explore_eps=explore_eps)
                if quit_requested:
                    running = False
                    break
                results.append((score, movement_count))
        if not running:
            break

        # Assign fitness with anti-idle penalty and small movement bonus
        scores = []
        movements = []
        for agent, (score, movement_count) in zip(population, results):
            idle_penalty = 5 if movement_count == 0 else 0  # penalize purely idle policies
            move_bonus = min(3, movement_count // 25)  # tiny bonus for making some moves
            fitness = max(0, score - idle_penalty + move_bonus)
            agent.fitness = fitness
            agent.score = score
            scores.append(score)
            movements.append(movement_count)

        # Stats
        avg_score = float(np.mean(scores)) if scores else 0.0
        max_score = int(max(scores)) if scores else 0
        min_score = int(min(scores)) if scores else 0
        avg_moves = float(np.mean(movements)) if movements else 0.0

        print(f"\nGeneration {gen + 1}/{generations}")
        print(f"  Avg Score: {avg_score:.2f} | Max: {max_score} | Min: {min_score}")
        print(f"  Avg Moves: {avg_moves:.1f}")
        print(f"  Best Ever: {neuro_evo.best_fitness}")

        # Track stagnation and adapt mutation by tweaking evolution params
        best_history.append(max_score)
        if len(best_history) >= 5 and max(best_history[-5:]) - min(best_history[-5:]) <= 1:
            # If best score stagnates over last 5 generations, temporarily increase mutation
            # We'll implement this by mutating the elite copies once more after evolve
            neuro_evo.evolve()
            for agent in neuro_evo.get_population()[:neuro_evo.elite_size]:
                agent.mutate(mutation_rate=0.4, mutation_scale=0.5)
        else:
            neuro_evo.evolve()

        # Show best agent every 5 generations
        if (gen + 1) % 5 == 0:
            print(f"\n  Showing best agent from generation {gen + 1}...")
            best_agent = neuro_evo.get_best_agent()
            score, quit_requested, _ = run_game_episode(best_agent, max_time=max_time, render=True, explore_eps=0.0)
            if quit_requested:
                running = False
                break
            print(f"  Best agent scored: {score}")

        # Save best agent every 10 generations
        if (gen + 1) % 10 == 0:
            neuro_evo.save_best(f"best_agent_gen_{gen + 1}.pth")

    # Final save
    neuro_evo.save_best("best_agent_final.pth")
    print("\nTraining complete!")
    print(f"Best fitness achieved: {neuro_evo.best_fitness}")

    # Demo
    print("\nDemonstrating best agent...")
    best_agent = neuro_evo.get_best_agent()
    while running:
        score, quit_requested, _ = run_game_episode(best_agent, max_time=60000, render=True, explore_eps=0.0)
        if quit_requested:
            break
        print(f"Demo score: {score}")

if __name__ == "__main__":
    try:
        train_ai()
    finally:
        pygame.quit()
        sys.exit()
