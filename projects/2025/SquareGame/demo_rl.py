import pygame
import random
import sys
import torch
from rl_dqn import DQNAgent

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
OBJECT_WIDTH, OBJECT_HEIGHT = 40, 40
PLAYER_SPEED = 7
OBJECT_SPEED = 5
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RL Demo - Dodge Game")
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
        if direction == 0 and self.x > 0:
            self.x -= self.speed
        elif direction == 2 and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
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
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT


def get_state(player, falling_objects):
    closest = sorted(falling_objects, key=lambda obj: obj.y, reverse=True)[:3]
    while len(closest) < 3:
        closest.append(type('obj', (), {'x': SCREEN_WIDTH // 2, 'y': -100})())
    state = [
        player.x / SCREEN_WIDTH,
        player.x / SCREEN_WIDTH - 0.5,
    ]
    for i in range(2):
        obj = closest[i]
        state.extend([
            obj.x / SCREEN_WIDTH,
            obj.y / SCREEN_HEIGHT,
            (obj.x - player.x) / SCREEN_WIDTH,
        ])
    return state


def main():
    agent = DQNAgent()
    try:
        agent.load("best_rl_dqn_final.pth")
    except Exception:
        try:
            agent.load("best_rl_dqn.pth")
        except Exception:
            print("No trained RL model found. Run train_rl.py first.")
            pygame.quit()
            sys.exit()

    player = Player()
    objs = []
    start = pygame.time.get_ticks()
    last_spawn = start
    score = 0
    game_over = False

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            now = pygame.time.get_ticks()
            score = (now - start) // 1000
            speed_mul = 1.0 + (score * 0.1)
            spawn_interval = max(300, 1000 - score * 30)
            if now - last_spawn > spawn_interval:
                objs.append(FallingObject(speed_mul))
                last_spawn = now

            for obj in list(objs):
                obj.update()
                if obj.is_off_screen():
                    objs.remove(obj)

            action = agent.select_action(get_state(player, objs))
            player.move(action)

            if player.get_rect().collidelist([o.get_rect() for o in objs]) != -1:
                game_over = True

        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, player.get_rect())
        for obj in objs:
            pygame.draw.rect(screen, RED, obj.get_rect())
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

