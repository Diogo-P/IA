# 8-Puzzle Search Algorithms Solver

A Python implementation of classic uninformed and informed search algorithms to solve the **8-Puzzle** problem, complete with a graphical interface for visualization and performance analysis.

## Overview

This project models the 8-Puzzle as a state-space search problem, demonstrating how different traversal strategies and heuristics impact execution time, memory consumption, and path optimality. These underlying graph-search principles directly apply to real-world optimization problems such as routing, pathfinding, and logistics.

## Implemented Algorithms

* **BFS (Breadth-First Search):** Explores the state space level by level. Guarantees the shortest path (optimal solution) at the cost of higher memory usage.
* **DFS (Depth-First Search):** Explores as deep as possible along each branch before backtracking. Lower memory footprint, but does not guarantee an optimal path.
* **A\* (A-Star) with Manhattan Distance:** Combines the actual path cost $g(n)$ with the admissible Manhattan distance heuristic $h(n)$, drastically reducing the number of expanded nodes while guaranteeing an optimal solution.

## Project Structure

```text
├── algoritmos/      # Core search algorithm implementations (BFS, DFS, A*)
├── interface.py     # Graphical user interface for puzzle visualization
├── puzzle.py        # 8-Puzzle state representation and valid move logic
└── main.py          # Application entry point
```

## Prerequisites

* **Python 3.8+**
* Standard Python libraries (no external dependencies required if using `tkinter`; if you use `pygame` or another library, install it via `pip`).

## How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Diogo-P/IA.git](https://github.com/Diogo-P/IA.git)
   cd IA
   ```

2. **Execute the application:**
   ```bash
   python main.py
   ```

## Complexity Analysis

| Algorithm | Complete | Optimal | Time Complexity | Space Complexity |
| :--- | :---: | :---: | :---: | :---: |
| **BFS** | Yes | Yes | $O(b^d)$ | $O(b^d)$ |
| **DFS** | No* | No | $O(b^m)$ | $O(b \cdot m)$ |
| **A\* (Manhattan)** | Yes | Yes | $O(b^d)$ (worst case) | $O(b^d)$ |

*\*Complete only in finite state spaces with cycle/visited-state checking.*  
*($b$: branching factor, $d$: depth of optimal solution, $m$: maximum depth of the state space)*

## Preview

<!--
To add a screenshot:
1. Create an `assets/` folder in the root directory.
2. Save a screenshot of the GUI running as `assets/preview.png`.
3. Uncomment the line below:
-->
<!-- ![8-Puzzle Solver Interface](assets/preview.png) -->
