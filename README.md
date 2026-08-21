# Pac-Man Clone — Python + Pygame

## Description
A classic Pac-Man clone built from scratch in Python using Pygame. Navigate a hand-crafted 19x21 maze, eat every dot to win, and avoid four ghosts that chase you with a mix of pathfinding and randomness.


<img width="456" height="594" alt="Screenshot 2026-08-21 at 10 47 10 PM" src="https://github.com/user-attachments/assets/e21e7870-f07d-4f4a-979b-a0fce0dedb2e" />





## Features
- Fully custom maze layout (walls, dots, and a ghost-house area)
- Smooth grid-based movement with input buffering (queues your next turn before you reach the intersection)
- Animated Pac-Man mouth (chomping effect synced to movement)
- 4 ghosts, each a distinct color, with semi-intelligent chase behavior (70% chance to move toward the player, 30% random) plus no-reverse movement logic
- Score tracking (+10 per dot) and a 3-lives system
- Win state when all dots are cleared, game-over state when lives run out
- Restart with `R` after winning or losing
- Screen wrap-around (classic tunnel-style movement off one edge to the other)

## Requirements
- Python 3.8+
- Pygame

```bash
pip install pygame
```

## Getting Started
```bash
python3 pacman.py
```

## Controls
| Key | Action |
|---|---|
| ↑ / ↓ / ← / → | Move Pac-Man |
| R | Restart (after Game Over or Win) |

## How It Works
- **Maze**: represented as a grid of `1` (wall), `0` (path with a dot), and `2` (empty path, used for the ghost house).
- **Player**: moves in fixed grid steps, snapping to tile alignment before accepting a new direction so turns feel responsive but grid-locked.
- **Ghosts**: at each tile intersection, pick a new direction — excluding an immediate reverse — weighted toward closing the distance to Pac-Man, with occasional random moves to keep things unpredictable.
- **Collision**: a ghost occupying the same tile as Pac-Man costs a life and resets Pac-Man's position.

## Known Issues / Rough Edges
- `main()` calling itself recursively on restart (`R` key) works but will leak Pygame windows/state on repeated restarts rather than cleanly resetting — a dedicated `reset_game()` function would be safer for long play sessions.
- Ghosts respawn at the same position after eating Pac-Man, but don't reset to their ghost-house start on player death — only the player resets.
- No ghost "frightened/eaten" mode (no power pellets yet).
- No sound effects/music.

## Roadmap Ideas
- Power pellets that let Pac-Man eat ghosts temporarily
- Proper ghost-house exit/return logic and distinct AI personalities (blinky/pinky/inky/clyde-style)
- Sound effects and background music
- High-score persistence

## Author
Shreya Jain
