import matplotlib
import matplotlib.pyplot as plt
import torch

from environment import Action
from renderer import GridWorldRenderer
from training.evo import train_evolution
from training.rl import train_reinforce
from training.supervised import train_supervised


def demo_run(env, model, max_steps=20, render=True):
    print("\n=== Demo run ===")
    renderer = GridWorldRenderer(env) if render else None

    state = env.reset()
    total_reward = 0.0

    if renderer is not None:
        renderer.draw()

    for step in range(max_steps):
        s_t = (torch
               .from_numpy(state) # Convert state to PyTorch tensor and
               .unsqueeze(0)) # Add batch dimension (how many samples to process at once)
        with torch.no_grad(): # Disable autograd to speed up inference
            logits = model(s_t) # Run the model
            action_index = torch.argmax(logits, dim=-1).item() # Choose action with the highest probability
            action = Action(action_index) # Convert index to enum

        state, reward, done, _ = env.step(action) # Execute the action
        total_reward += reward

        x, y = env.pos
        print(f"Step {step:2d}: pos=({x},{y})  reward={reward:.2f}")

        if renderer is not None:
            renderer.draw()

        if done:
            break

    print("Total reward:", total_reward)
    # keep the window open at the end
    if render:
        print("Close the matplotlib window to continue.")
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    # Choose one: "supervised", "rl", "evo"
    mode = "supervised"

    if mode == "supervised":
        env, model = train_supervised()
    elif mode == "rl":
        env, model = train_reinforce()
    elif mode == "evo":
        env, model = train_evolution()
    else:
        raise ValueError("Unknown mode")

    demo_run(env, model)
