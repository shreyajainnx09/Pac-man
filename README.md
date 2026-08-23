<div align="center">

# 👻 Pac-Man Clone
### A classic Pac-Man clone built from scratch in Python & Pygame

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Pygame](https://img.shields.io/badge/Pygame-000000?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Pygame-000000?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## 📌 Description

A classic **Pac-Man** clone built from scratch in Python using Pygame. Navigate a hand-crafted 19×21 maze, eat every dot to win, and avoid four ghosts that chase you using a mix of pathfinding and randomness — arrow keys only.

![Pac-Man gameplay screenshot](<img width="456" height="594" alt="Screenshot 2026-08-21 at 10 47 10 PM" src="https://github.com/user-attachments/assets/800ecb3b-91b0-4e9b-bf77-4c5b84552a86" />
)

## 🎯 Features

- Fully custom maze layout (walls, dots, and a ghost-house area)
- Smooth grid-based movement with **input buffering** — queues your next turn before you reach the intersection
- Animated Pac-Man mouth (chomping effect synced to movement)
- 4 ghosts, each a distinct color, with semi-intelligent chase behavior (70% chance to move toward the player, 30% random) plus no-reverse movement logic
- Score tracking (+10 per dot) and a 3-lives system
- Win state when all dots are cleared, game-over state when lives run out
- Restart with `R` after winning or losing
- Screen wrap-around (classic tunnel-style movement off one edge to the other)

## 🎮 Controls

| Key | Action |
|---|---|
| ↑ / ↓ / ← / → | Move Pac-Man |
| `R` | Restart (after Game Over or Win) |

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Game logic |
| 🎮 Pygame | Rendering, input, and game loop |

## ⚙️ Setup

**Requirements**
- Python 3.8+
- Pygame

```bash
git clone https://github.com/shreyajainnx09/Pac-man.git
cd Pac-man
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install pygame
```

## ▶️ Run

```bash
python3 pacman.py
```

## 🧠 How It Works

- **Maze** — represented as a grid of `1` (wall), `0` (path with a dot), and `2` (empty path, used for the ghost house)
- **Player** — moves in fixed grid steps, snapping to tile alignment before accepting a new direction so turns feel responsive but grid-locked
- **Ghosts** — at each tile intersection, pick a new direction (excluding an immediate reverse) weighted toward closing the distance to Pac-Man, with occasional random moves to keep things unpredictable
- **Collision** — a ghost occupying the same tile as Pac-Man costs a life and resets Pac-Man's position

## 📁 Project Structure

```
Pac-man/
│
├── pacman.py        → Pygame implementation (maze, Player, ghost AI, game loop)
└── README.md
```

## 🐛 Known Issues / Rough Edges

- `main()` calls itself recursively on restart (`R` key) — works, but will leak Pygame windows/state on repeated restarts rather than cleanly resetting; a dedicated `reset_game()` function would be safer for long play sessions
- Ghosts respawn at the same position after eating Pac-Man, but don't reset to their ghost-house start on player death — only the player resets
- No ghost "frightened/eaten" mode (no power pellets yet)
- No sound effects/music

## 🌟 Ideas for Extending

- Power pellets that let Pac-Man eat ghosts temporarily
- Proper ghost-house exit/return logic and distinct AI personalities (Blinky/Pinky/Inky/Clyde-style)
- Sound effects and background music
- High-score persistence

## 👩🏻‍💻 Author

**Shreya Jain**
BCA | Data Analytics | Python | SQL | Tableau
