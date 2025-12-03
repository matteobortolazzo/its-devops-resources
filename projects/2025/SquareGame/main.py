import pygame
import random
import sys

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
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

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
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

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

def main():
    player = Player()
    falling_objects = []
    score = 0
    game_over = False
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()
    spawn_interval = 1000  # Spawn every 1 second initially

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Restart game
                    player = Player()
                    falling_objects = []
                    score = 0
                    game_over = False
                    start_time = pygame.time.get_ticks()
                    last_spawn_time = pygame.time.get_ticks()
                    spawn_interval = 1000

        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move("left")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move("right")

            # Update score (1 point per second)
            current_time = pygame.time.get_ticks()
            score = (current_time - start_time) // 1000

            # Calculate difficulty multipliers based on score
            speed_multiplier = 1.0 + (score * 0.1)  # Speed increases by 10% every second
            spawn_interval = max(300, 1000 - score * 30)  # Spawn faster over time, minimum 0.3s

            # Spawn falling objects
            if current_time - last_spawn_time > spawn_interval:
                falling_objects.append(FallingObject(speed_multiplier))
                last_spawn_time = current_time

            # Update falling objects
            for obj in falling_objects[:]:
                obj.update()
                if obj.is_off_screen():
                    falling_objects.remove(obj)

            # Check collisions
            if check_collision(player, falling_objects):
                game_over = True

        # Drawing
        screen.fill(WHITE)

        if not game_over:
            player.draw()
            for obj in falling_objects:
                obj.draw()

            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
        else:
            # Game over screen
            game_over_text = font.render("GAME OVER!", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

