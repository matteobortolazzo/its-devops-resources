# Quick Start Guide

## Installation

1. Make sure you're in the project directory:
```bash
cd /home/mborto/Repos/its-resources/projects/2025/SquareGame
```

2. Activate the virtual environment (if not already active):
```bash
source .venv/bin/activate
```

3. Install dependencies (already done, but if needed):
```bash
pip install -r requirements.txt
```

## Usage

### 1. Play the Game Yourself
```bash
python main.py
```
- Use arrow keys or A/D to move
- Avoid the red falling squares
- Each second survived = 1 point

### 2. Train the AI
```bash
python train_ai.py
```
- Trains for 100 generations (takes ~10-20 minutes)
- Shows best agent every 5 generations
- Saves checkpoints every 10 generations
- Creates `best_agent_final.pth` when complete

### 3. Watch the AI Play
```bash
python demo_ai.py
```
- Loads the trained model
- AI player is shown in green
- Watch it dodge the falling objects!

## How the AI Works

The AI uses **neuroevolution** (genetic algorithm):
1. Start with 50 random neural networks
2. Each network plays the game
3. Best performers survive
4. Winners "reproduce" with mutations
5. Repeat for many generations
6. Networks get better over time!

The neural network:
- **Input**: Player position + 2 closest falling objects (8 values)
- **Hidden**: 2 layers of 16 neurons each
- **Output**: 3 actions (move left, stay, move right)

No backpropagation - pure evolution!

## Files

- `main.py` - Human playable game
- `train_ai.py` - Train the AI
- `demo_ai.py` - Watch trained AI play
- `ai_player.py` - Neural network & evolution logic
- `best_agent_*.pth` - Saved AI models (after training)

## Tips

- Training is faster on GPU but works fine on CPU
- You can stop training early (Ctrl+C) and still use the best agent
- The AI learns to position itself under gaps between falling objects
- Difficulty increases over time, so even good AIs eventually die!

Enjoy!

