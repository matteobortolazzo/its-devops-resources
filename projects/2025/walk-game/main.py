import matplotlib.pyplot as plt
import torch

from environment import Action, GridWorld
from model import WalkBrain
from renderer import GridWorldRenderer
from training.supervised import train_supervised
from training.evolution import train_evolution
from training.reinforce_learning import train_reinforce_learning

def save_model(model, path="model.pth"):
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")

def load_model(path="model.pth"):
    model = WalkBrain()
    model.load_state_dict(torch.load(path))
    model.eval()
    print(f"Model loaded from {path}")
    return model

def demo_run(env, model, max_steps=25, render=True):
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
    # Choose one: "spv", "evo", "rl"
    mode = "evo"
    env = GridWorld()

    if mode == "spv":
        env, model = train_supervised(env)
    elif mode == "evo":
        env, model = train_evolution(env)
    elif mode == "rl":
        env, model = train_reinforce_learning(env)

    else:
        raise ValueError("Unknown mode")

    demo_run(env, model)
