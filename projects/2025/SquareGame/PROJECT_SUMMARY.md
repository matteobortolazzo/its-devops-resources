# Project Summary: Dodge Game with AI

## Overview
A 2D dodge game built with pygame where players avoid falling objects. The project includes a neural network AI that learns to play using **neuroevolution** (genetic algorithms).

## What's Been Implemented

### 1. Base Game (main.py)
- Player controlled with arrow keys or A/D
- Falling objects from random positions
- Progressive difficulty (faster falling, more frequent spawning)
- Scoring: 1 point per second survived
- Game over on collision

### 2. AI System (ai_player.py)
- **DodgeNet**: Neural network with:
  - 8 inputs (player position + 2 closest objects)
  - 2 hidden layers (16 neurons each)
  - 3 outputs (left, stay, right)
- **AIAgent**: Wrapper with fitness tracking
- **NeuroEvolution**: Genetic algorithm with:
  - Population of 50 agents
  - Elite selection (top 10 survive)
  - Mutation-based reproduction
  - Fitness = survival time

### 3. Training System (train_ai.py)
- Trains for 100 generations
- Each agent plays the game
- Best performers reproduce
- Mutations introduce variation
- Shows best agent every 5 generations
- Saves checkpoints every 10 generations
- Creates `best_agent_final.pth` when complete

### 4. Demo System (demo_ai.py)
- Loads trained AI models
- Visualizes AI playing (green player)
- Can restart with SPACE after game over
- Shows "AI Playing" indicator

### 5. Testing (test_ai.py)
- Tests neural network creation
- Tests agent cloning and mutation
- Tests evolution system
- Tests save/load functionality
- All tests passing ✓

## Files Structure
```
SquareGame/
├── main.py              # Human playable game
├── train_ai.py          # AI training script
├── demo_ai.py           # Watch trained AI play
├── ai_player.py         # Neural network & evolution logic
├── test_ai.py           # Verification tests
├── requirements.txt     # Dependencies
├── README.md            # Full documentation
├── QUICKSTART.md        # Quick start guide
└── best_agent_*.pth     # Saved models (after training)
```

## Dependencies Installed
- pygame 2.6.1
- torch 2.9.1 (with CUDA support)
- numpy 2.3.5

## How to Use

### Play the Game
```bash
python main.py
```

### Train the AI
```bash
python train_ai.py
```
Takes ~10-20 minutes for 100 generations

### Watch AI Play
```bash
python demo_ai.py
```
Requires trained model from previous step

### Test System
```bash
python test_ai.py
```

## Key Features of the AI

### Neuroevolution (Not Backpropagation!)
- No gradient descent
- Pure genetic algorithm
- Networks evolve like organisms
- Survival of the fittest

### State Representation
The AI sees:
1. Its own position (normalized)
2. Position relative to center
3. X/Y position of 2 closest falling objects
4. Relative distances to those objects

Total: 8 input values

### Learning Process
1. Generation 1: Random networks (terrible performance)
2. Evaluate all 50 agents by playing the game
3. Keep top 10 performers
4. Create 40 offspring with mutations
5. Repeat for 100 generations
6. Networks learn to dodge effectively!

## Performance Notes
- Training runs at 300 FPS (fast)
- Demo runs at 60 FPS (normal)
- Works on CPU (no GPU required)
- GPU speeds up training slightly

## Expected Results
- Early generations: Score 0-5 (random movement)
- Mid generations (gen 20-50): Score 10-20 (basic dodging)
- Late generations (gen 50-100): Score 20-40+ (good dodging)
- Best agents can sometimes reach 50+ points!

## What Makes This Cool
1. **Pure evolution** - No backpropagation, just survival!
2. **Emergent behavior** - AI discovers dodging strategies naturally
3. **Visual learning** - Watch it get better every 5 generations
4. **Reproducible** - Save and load trained agents
5. **Educational** - Great example of genetic algorithms in action

## Next Steps (Optional Enhancements)
- Add more input features (object speeds, multiple objects)
- Experiment with network architectures
- Implement crossover (breeding two parents)
- Add speciation (multiple species evolving)
- Visualize neural network activations during play
- Create tournament mode (agents compete)

## Verification
✅ All systems tested and working
✅ Dependencies installed
✅ Can create and train agents
✅ Can save and load models
✅ Ready to use!

Enjoy training your AI! 🎮🤖

