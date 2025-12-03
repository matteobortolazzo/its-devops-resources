# Dodge Game

A simple 2D pygame where you control a player that must avoid falling objects for as long as possible.

## Features
- Move left/right with arrow keys (← →) or A/D keys
- Avoid red falling objects
- Score increases by 1 point per second survived
- Difficulty increases over time (objects spawn faster)
- Press SPACE to restart after game over

## Installation

Make sure you have Python installed, then install the dependencies:

```bash
pip install pygame
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## Controls
- **Left Arrow** or **A**: Move left
- **Right Arrow** or **D**: Move right
- **SPACE**: Restart game (when game over)
- **Close Window** or **ESC**: Quit game

## Gameplay
- The blue square at the bottom is your player
- Red squares fall from the top
- Move left and right to dodge them
- Each second you survive = 1 point
- Game ends when you collide with a falling object

Good luck!

