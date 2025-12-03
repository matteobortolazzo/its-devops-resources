import pygame
import random
import sys
from ai_player import AIAgent, DodgeNet
import torch

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
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Demo - Dodge Game")
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

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

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
    closest_objects = sorted(falling_objects, key=lambda obj: obj.y, reverse=True)[:3]

    while len(closest_objects) < 3:
        closest_objects.append(type('obj', (), {
            'x': SCREEN_WIDTH // 2,
            'y': -100,
            'speed': 0
        })())

    state = [
        player.x / SCREEN_WIDTH,
        player.x / SCREEN_WIDTH - 0.5,
    ]

    for i in range(2):
        obj = closest_objects[i]
        state.extend([
            obj.x / SCREEN_WIDTH,
            obj.y / SCREEN_HEIGHT,
            (obj.x - player.x) / SCREEN_WIDTH,
        ])

    return state

def load_ai_agent(filepath):
    """Load a trained AI agent"""
    try:
        network = DodgeNet()
        network.load_state_dict(torch.load(filepath))
        return AIAgent(network)
    except FileNotFoundError:
        print(f"Model file {filepath} not found. Please train the AI first using train_ai.py")
        return None

def main():
    # Try to load the best agent
    agent = load_ai_agent("best_agent_final.pth")
    if agent is None:
        agent = load_ai_agent("best_agent_gen_10.pth")
    if agent is None:
        print("No trained model found. Run train_ai.py first!")
        pygame.quit()
        sys.exit()

    player = Player()
    falling_objects = []
    score = 0
    game_over = False
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Restart
                    player = Player()
                    falling_objects = []
                    score = 0
                    game_over = False
                    start_time = pygame.time.get_ticks()
                    last_spawn_time = pygame.time.get_ticks()

        if not game_over:
            # Update score
            current_time = pygame.time.get_ticks()
            score = (current_time - start_time) // 1000

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

            # AI makes decision
            state = get_state(player, falling_objects)
            action = agent.get_action(state)

            if action == 0:
                player.move("left")
            elif action == 2:
                player.move("right")

            # Check collisions
            if check_collision(player, falling_objects):
                game_over = True

        # Drawing
        screen.fill(WHITE)

        if not game_over:
            player.draw()
            for obj in falling_objects:
                obj.draw()

            score_text = font.render(f"Score: {score}", True, BLACK)
            ai_text = small_font.render("AI Playing", True, GREEN)
            screen.blit(score_text, (10, 10))
            screen.blit(ai_text, (10, 50))
        else:
            game_over_text = font.render("GAME OVER!", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            restart_text = small_font.render("Press SPACE to restart", True, BLACK)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

