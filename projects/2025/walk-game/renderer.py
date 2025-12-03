import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

class GridWorldRenderer:
    def __init__(self, env):
        self.env = env
        self.size = env.size

        plt.ion()
        self.fig, self.ax = plt.subplots()

        # Grid aligns with cell edges
        self.ax.set_xlim(-0.5, self.size - 0.5)
        self.ax.set_ylim(-0.5, self.size - 0.5)

        # Cell boundary grid lines
        self.ax.set_xticks(np.arange(-0.5, self.size, 1))
        self.ax.set_yticks(np.arange(-0.5, self.size, 1))
        self.ax.grid(True, which="major", linewidth=0.5, color="gray")

        # Hide tick labels
        self.ax.tick_params(which="major", bottom=False, left=False,
                            labelbottom=False, labelleft=False)

        self.img = None
        self.agent_scatter = None

    def _build_grid(self):
        grid = np.zeros((self.size, self.size), dtype=np.int32)
        lx, ly = self.env.lava
        gx, gy = self.env.goal
        grid[ly, lx] = 1
        grid[gy, gx] = 2
        return grid

    def draw(self):
        grid = self._build_grid()

        from matplotlib.colors import ListedColormap
        cmap = ListedColormap(["white", "red", "green"])

        if self.img is None:
            self.img = self.ax.imshow(
                grid,
                cmap=cmap,
                vmin=0,
                vmax=2,
                origin="lower",
                interpolation="none",
                extent=(-0.5, self.size - 0.5, -0.5, self.size - 0.5),
            )
            self.agent_scatter = self.ax.scatter([], [], s=200, color="blue")
        else:
            self.img.set_data(grid)

        ax, ay = self.env.pos
        self.agent_scatter.set_offsets([[ax, ay]])

        self.fig.canvas.draw()
        plt.pause(0.25)
