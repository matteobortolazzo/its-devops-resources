# Dodge Game

A simple 2D pygame where you control a player that must avoid falling objects for as long as possible.

**Now with AI!** Train a neural network to play the game using neuroevolution (genetic algorithms).

## Features
- Move left/right with arrow keys (← →) or A/D keys
- Avoid red falling objects
- Score increases by 1 point per second survived
- Difficulty increases over time (objects spawn faster and fall faster)
- Press SPACE to restart after game over
- **AI Mode**: Train neural networks to learn how to play!

## Installation

Make sure you have Python installed, then install the dependencies:

```bash
pip install pygame torch numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## How to Play (Human)

```bash
python main.py
```

## How to Train the AI

Train an AI agent using neuroevolution (genetic algorithm):

```bash
python train_ai.py
```

The training process:
- Creates a population of 50 neural networks
- Each network plays the game and gets a fitness score
- Best performers reproduce with mutations
- Evolves for 100 generations
- Shows best agent every 5 generations
- Saves best agent every 10 generations

Training takes about 10-20 minutes depending on your hardware.

## Watch the AI Play

After training, watch the trained AI play:

```bash
python demo_ai.py
```

The AI (shown in green) will use its trained neural network to dodge the falling objects.

## How the AI Works

### Neural Network Architecture
- **Input Layer (8 neurons)**: 
  - Player position
  - Position of 2 closest falling objects
  - Relative distances
- **Hidden Layers**: 2 layers with 16 neurons each
- **Output Layer (3 neurons)**: Left, Stay, Right

### Neuroevolution
- **Population**: 50 agents per generation
- **Selection**: Top 10 agents (elite) survive
- **Reproduction**: Elite agents create mutated offspring
- **Mutation**: 20% of weights get random noise
- **Fitness**: Survival time (score)

The AI learns purely through evolution - no backpropagation or gradient descent!

## Controls
- **Left Arrow** or **A**: Move left
- **Right Arrow** or **D**: Move right
- **SPACE**: Restart game (when game over)
- **Close Window**: Quit game

## Gameplay
- The blue square (or green for AI) at the bottom is your player
- Red squares fall from the top
- Move left and right to dodge them
- Each second you survive = 1 point
- Game ends when you collide with a falling object

## Files
- `main.py`: Human playable game
- `train_ai.py`: Train the AI using neuroevolution
- `demo_ai.py`: Watch a trained AI play
- `ai_player.py`: Neural network and evolution logic
- `best_agent_*.pth`: Saved AI models (created after training)

Good luck!

