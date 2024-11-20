# Nim Game implemented with AI Using Pygame

This is a Python implementation of the classic **Nim Game**, where a player competes against an AI. The AI uses the XOR-sum strategy to make optimal moves. The game is built using the **Pygame** library, featuring interactive gameplay with restart and end-game options.

---

## **How to Play**
1. The game starts with 3 piles of stones.
2. On each turn, the player or the AI must remove **at least 1 stone** from a single pile.
3. The player who is forced to take the last stone loses the game.

---

## **Features**
- **Interactive Gameplay**:
  - Players can select a pile and choose how many stones to remove using the keyboard (keys `1-9`).
- **AI Opponent**:
  - The AI uses a winning XOR strategy for optimal moves.
- **Restart Button**:
  - Allows restarting the game at any time with randomly generated piles.
- **End Game Button**:
  - Allows the player to quit the game immediately.
- **Dynamic Displays**:
  - Displays the total number of stones, the last move, and whose turn it is.

---

## **Requirements**
- **Python 3.7+**
- **Pygame 2.0+**

---

## **Setup and Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/nim-game.git](https://github.com/emmanuelayanful/AI4SCIENCE.git)
2. Install requirements:
   ```bash
    pip install -r requirements.txt
