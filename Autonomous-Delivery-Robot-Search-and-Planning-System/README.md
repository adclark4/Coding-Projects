# Autonomous Delivery Robot Search & Planning System

## Overview

This project is a Python-based artificial intelligence search and planning system that models an autonomous delivery robot navigating a small delivery network.

The robot must pick up a package from a depot, manage a limited battery supply, recharge when necessary, travel through connected locations, and successfully deliver the package to a customer.

The project compares multiple search algorithms on the same problem to evaluate how different strategies affect solution quality and search efficiency.

The system uses:

- Breadth-First Search (BFS)
- Uniform-Cost Search (UCS)
- A* Search

Each algorithm operates on the same state representation, actions, path-cost function, and goal conditions so their behavior can be compared fairly.

---

## Features

- State-space search problem representation
- Autonomous delivery robot simulation
- Package pickup and delivery tracking
- Battery resource management
- Charging station logic
- Legal action and transition handling
- Breadth-First Search implementation
- Uniform-Cost Search implementation
- A* Search implementation
- Custom heuristic function
- Repeated-state and cycle handling
- Path-cost tracking
- Generated and expanded node tracking
- Maximum frontier tracking
- Runtime measurement
- Search algorithm comparison
- Valid and invalid action testing

---

## Problem Representation

Each state is represented as:

`[robot_location, package_status, battery_level]`

The state tracks:

- `robot_location` – current location of the robot
- `package_status` – `at_depot`, `carried`, or `delivered`
- `battery_level` – remaining battery units

The initial state is:

`('Depot', 'at_depot', 5)`

The goal is reached when:

`robot_location = Customer AND package_status = delivered`

---

## Available Actions

The robot can perform the following actions:

- `Move(destination)`
  - Moves the robot to a directly connected location if enough battery is available.
- `PickUp`
  - Picks up the package while the robot is at the Depot.
- `Recharge`
  - Restores the robot's battery to full capacity at the Charging Station.
- `Deliver`
  - Delivers the package when the robot is at the Customer and carrying the package.

Because these actions have preconditions and effects that change the system state, the problem requires planning rather than simple route finding.

---

## Search Algorithms

### Breadth-First Search

Breadth-First Search explores the state space level by level using a queue.

BFS prioritizes solutions with fewer actions but does not use path cost when deciding which state to explore next.

### Uniform-Cost Search

Uniform-Cost Search expands the frontier node with the lowest accumulated path cost.

This allows the algorithm to account for differences in movement, pickup, recharge, and delivery costs.

### A* Search

A* combines the current path cost with a heuristic estimate of the remaining cost:

`f(n) = g(n) + h(n)`

Where:

- `g(n)` = path cost so far
- `h(n)` = estimated remaining cost

The heuristic estimates the remaining travel and required action costs while ignoring battery-related detours and recharge costs.

---

## Algorithm Results

| Algorithm | Solution Length | Path Cost | Generated Nodes | Expanded Nodes | Max Frontier | Runtime |
|---|---:|---:|---:|---:|---:|---:|
| BFS | 6 | 11 | 32 | 27 | 9 | 0.00016367 s |
| UCS | 6 | 11 | 30 | 22 | 9 | 0.00014946 s |
| A* | 6 | 11 | 16 | 8 | 8 | 0.00007228 s |

All three algorithms found the same six-action solution:

`PickUp → Move(Main Street) → Move(Charging Station) → Recharge → Move(Customer) → Deliver`

A* produced the same solution length and path cost while generating and expanding fewer nodes than BFS and UCS.

---

## Heuristic

The A* heuristic estimates the remaining cost required to complete the delivery.

Depending on the current package status, the estimate may include:

- Travel to the Depot
- Package pickup cost
- Travel toward the Customer
- Delivery cost

Battery-related detours and recharge costs are intentionally excluded from the heuristic estimate.

This keeps the heuristic simple and optimistic while still providing useful guidance during search.

---

## Testing

The implementation includes tests for:

- Initial state
- Legal actions
- States with multiple available actions
- Invalid actions
- Goal-test behavior
- Heuristic values
- BFS execution
- UCS execution
- A* execution
- Final returned action sequences

---

## Tech Stack

- Language: Python 3
- Environment: Google Colab / Jupyter Notebook
- Standard Libraries:
  - `collections`
  - `heapq`
  - `itertools`
  - `time`
- Version Control: GitHub

---

## Project File

The main implementation is located in:

`Project_1_Delivery_Robot_Search_and_Planning.ipynb`

The notebook contains:

- Problem definition
- State representation
- Legal actions
- Transition model
- Goal test
- Path-cost function
- BFS
- UCS
- A*
- Heuristic function
- Test cases
- Algorithm comparison

---

## How to Run

1. Download or clone the repository.

2. Open:

   `Delivery Robot Search and Planning.ipynb`

   in Google Colab or Jupyter Notebook.

3. Run all notebook cells.

4. Review the output for:

   - Solution found
   - Action sequence
   - Solution length
   - Total path cost
   - Generated nodes
   - Expanded nodes
   - Maximum frontier size
   - Runtime

No additional Python packages are required.
