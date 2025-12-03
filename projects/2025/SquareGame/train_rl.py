import pygame
import random
import sys
import torch
from rl_dqn import DQNAgent

# Pygame setup (headless training uses minimal rendering)
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
OBJECT_WIDTH, OBJECT_HEIGHT = 40, 40
PLAYER_SPEED = 7
OBJECT_SPEED = 5
FPS = 600  # fast headless

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RL Training - Dodge Game")
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
        if direction == 0 and self.x > 0:  # left
            self.x -= self.speed
        elif direction == 2 and self.x < SCREEN_WIDTH - self.width:  # right
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

# Env helpers

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

def check_collision(player, objects):
    rect = player.get_rect()
    for obj in objects:
        if rect.colliderect(obj.get_rect()):
            return True
    return False

# Episode rollouts

def run_episode(agent, max_time_ms=30000, render=False):
    player = Player()
    objs = []
    start = pygame.time.get_ticks()
    last_spawn = start
    score = 0.0
    steps = 0
    total_loss = 0.0

    done = False
    while not done:
        now = pygame.time.get_ticks()
        elapsed = now - start
        if elapsed >= max_time_ms:
            done = True
        score = elapsed / 1000.0

        # difficulty
        speed_mul = 1.0 + (score * 0.1)
        spawn_interval = max(300, 1000 - int(score) * 30)
        if now - last_spawn > spawn_interval:
            objs.append(FallingObject(speed_mul))
            last_spawn = now

        for obj in list(objs):
            obj.update()
            if obj.is_off_screen():
                objs.remove(obj)

        # observe
        state = get_state(player, objs)
        action = agent.select_action(state)

        # act
        player.move(action)

        # reward shaping
        reward = 1.0 / FPS  # ~1 per second
        if check_collision(player, objs):
            reward -= 50.0
            done = True

        next_state = get_state(player, objs)
        agent.replay.push(state, action, reward, next_state, float(done))
        loss = agent.optimize(batch_size=64)
        total_loss += loss
        steps += 1

        if agent.step_count % 1000 == 0:
            agent.update_target()

        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score, True
            screen.fill(WHITE)
            # minimal draw
            pygame.draw.rect(screen, GREEN, player.get_rect())
            for obj in objs:
                pygame.draw.rect(screen, RED, obj.get_rect())
            info = small_font.render(f"Score {int(score)} | steps {steps}", True, BLACK)
            screen.blit(info, (10, 10))
            pygame.display.flip()
            clock.tick(60)

    return score, False


def train_rl():
    # Detect device and report GPU info
    use_cuda = torch.cuda.is_available()
    device = "cuda" if use_cuda else "cpu"
    if use_cuda:
        try:
            gpu_name = torch.cuda.get_device_name(0)
        except Exception:
            gpu_name = "Unknown CUDA device"
        print(f"RL: Using GPU (CUDA) -> {gpu_name}")
    else:
        print("RL: Using CPU (CUDA not available)")

    agent = DQNAgent(device=device)

    episodes = 2000
    render_every = 0  # set to e.g. 100 to visualize

    running = True
    best = 0
    for ep in range(1, episodes + 1):
        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        render = (render_every and ep % render_every == 0)
        score, quit_requested = run_episode(agent, max_time_ms=20000, render=render)
        if quit_requested:
            break
        best = max(best, int(score))

        if ep % 50 == 0:
            print(f"Ep {ep}/{episodes} | last {int(score)} | best {best} | epsilon step {agent.step_count} | device {device}")
            agent.save("best_rl_dqn.pth")

    print("RL training complete. Best score:", best)
    agent.save("best_rl_dqn_final.pth")

if __name__ == "__main__":
    try:
        train_rl()
    finally:
        pygame.quit()
        sys.exit()
