import numpy as np
from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class GridWorld:
    """
    5x5 grid:
    - Start at (0,0)
    - Goal at (4,4)
    - Lava at (2,2)
    Actions: 0=up,1=down,2=left,3=right
    """

    def __init__(self, size=5):
        self.pos = (0, 0)
        self.size = size
        self.goal = (size - 1, size - 1)
        self.lava = (2, 2)
        self.reset()

    def reset(self):
        self.pos = (0, 0)
        return self.get_state()

    def get_state(self):
        x, y = self.pos
        goal_x, goal_y = self.goal
        lava_x, lava_y = self.lava
        # Convert to an array of floats in range [0,1]
        state = np.array([x, y, goal_x, goal_y, lava_x, lava_y], dtype=np.float32) / (self.size - 1)
        return state

    def step(self, action):
        x, y = self.pos
        x_old, y_old = x, y

        if action == Action.UP and y < self.size - 1:
            y += 1
        elif action == Action.DOWN and y > 0:
            y -= 1
        elif action == Action.LEFT and x > 0:
            x -= 1
        elif action == Action.RIGHT and x < self.size - 1:
            x += 1

        moved = (x != x_old or y != y_old)
        self.pos = (x, y)

        # Distance-based reward
        old_dist = abs(x_old - self.goal[0]) + abs(y_old - self.goal[1])
        new_dist = abs(x - self.goal[0]) + abs(y - self.goal[1])

        if not moved:
            reward = -0.5
        else:
            reward = 0.1 * (old_dist - new_dist) - 0.01

        done = False

        if self.pos == self.lava:
            reward = -5.0
            done = True
        elif self.pos == self.goal:
            reward = 10.0
            done = True

        return self.get_state(), reward, done, {}

