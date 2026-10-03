## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Simulation](#simulation)
- [Decision Modes](#decision-modes)
- [Configuration](#configuration)
- [Requirements](#requirements)
- [Running](#running)
- [Usage](#usage)
- [Reinforcement Learning](#reinforcement-learning)
- [Project Goals](#project-goals)
- [Possible Improvements](#possible-improvements)
- [Disclaimer](#disclaimer)
- [License](#license)

# Erkam-nci-BOZ213d01u01
A Dota-inspired jungle farming simulator using Q-learning to learn and visualize efficient farming routes.
# Dota Jungle Q-Learning Simulator

A small reinforcement learning experiment that simulates jungle farming in a Dota-inspired environment.

The project uses **Q-learning** to train an agent to choose jungle camps efficiently and compares its behavior against a simple **nearest-camp baseline**.

The simulation includes a graphical interface built with **Tkinter**, allowing the learned route and farming behavior to be visualized in real time.

## Features

- Dota-inspired jungle farming simulation
- Q-learning reinforcement learning agent
- Nearest-camp baseline strategy
- Adjustable hero damage
- Different jungle camp types:
  - Small
  - Medium
  - Large
  - Ancient
- Camp respawn system
- Travel and combat time simulation
- Gold and XP tracking
- Gold per minute (GPM) statistics
- Real-time visualization with Tkinter
- Background AI training using Python threads
- Comparison between heuristic and learned behavior

## How It Works

The agent observes a simplified state consisting of:

- The hero's current camp/location
- The current simulation time bucket
- The availability of jungle camps

At each decision point, the agent chooses which available camp to visit next.

An action consists of selecting one jungle camp.

The agent receives a reward when it successfully clears a camp.

During training, an epsilon-greedy strategy is used so that the agent initially explores different routes and gradually relies more on previously learned actions.

The Q-value update follows the standard Q-learning rule:

```text
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

Where:

- `α` is the learning rate
- `γ` is the discount factor
- `r` is the reward
- `s` is the current state
- `a` is the selected action

## Simulation

The environment contains simplified jungle camp positions inspired by a Dota-style map.

Each camp has:

- A position
- A camp tier
- Hit points
- Respawn timing
- Availability state

Combat duration depends on the selected hero damage and the HP of the camp.

Travel time is calculated using the distance between the hero and the target camp.

The simulation intentionally simplifies the real game and does not model mechanics such as:

- Terrain
- Trees
- Cliffs
- Pathfinding
- Vision
- Wards
- Camp pulling
- Stacking
- Neutral creep abilities
- Real Dota combat mechanics

The purpose of the project is to experiment with reinforcement learning and route optimization rather than accurately reproduce Dota gameplay.

## Decision Modes

### Nearest Camp

The baseline strategy always selects the closest currently available jungle camp.

### Learned AI

The Q-learning agent selects camps based on the Q-values learned during training.

The AI must be trained for the currently selected hero damage before this mode can be used.

Changing the hero damage requires retraining the agent.

## Configuration

Important simulation parameters can be modified near the top of the Python file.

```python
SIMULATION_TIME = 300.0
TIME_MULTIPLIER = 8.0

HERO_SPEED = 470.0

MIN_DAMAGE = 50
MAX_DAMAGE = 1000
INITIAL_DAMAGE = 100

CAMP_RESPAWN = 60.0

TRAIN_EPISODES = 12000

LEARNING_RATE = 0.15
DISCOUNT = 0.98

EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.9995
```

These parameters control the simulation speed, hero strength, camp behavior and reinforcement learning process.

## Requirements

- Python 3
- Tkinter

The reinforcement learning implementation itself uses only Python's standard library and does not require frameworks such as PyTorch or TensorFlow.

## Running

Clone the repository:

```bash
git clone https://github.com/radagaserkam/Erkam-nci-BOZ213d01u01.git
cd Erkam-nci-BOZ213d01u01
```

Run the program:

```bash
python "dota 2 AI train.py"
```

Depending on your system, you may need to use:

```bash
python3 main.py
```

## Usage

1. Launch the application.
2. Select the hero damage using the slider.
3. Run the simulation using **Nearest Camp** to observe the baseline strategy.
4. Click **Train AI** to train the Q-learning agent.
5. Wait for training to complete.
6. Select **Learned AI**.
7. Reset and start the simulation again.
8. Compare the resulting farming behavior and statistics.

The interface displays information such as:

- Simulation time
- Gold
- XP
- Camps cleared
- Score
- GPM
- Current target

## Reinforcement Learning

The agent uses tabular Q-learning.

The state representation is approximately:

```text
(
    current_location,
    time_bucket,
    available_camps_bitmask
)
```

The action space consists of selecting one of the jungle camps.

Training is performed over multiple simulated farming episodes using an epsilon-greedy exploration strategy.

This project is intentionally small and educational, making it possible to inspect the complete reinforcement learning implementation without relying on external machine learning libraries.

## Project Goals

This project was created as an experiment in:

- Reinforcement learning
- Q-learning
- Route optimization
- Simulation design
- Game AI
- Comparing learned policies with simple heuristics
- Visualizing reinforcement learning behavior

It is not intended to be an accurate Dota simulator or gameplay tool.

## Possible Improvements

Some possible future improvements include:

- More accurate map geometry
- Real pathfinding instead of straight-line movement
- Different rewards for different camp types
- Camp stacking
- More realistic neutral creep statistics
- Variable hero movement speed
- Multiple hero configurations
- Saving and loading trained Q-tables
- Training graphs and statistics
- Policy visualization
- Comparison between different RL algorithms
- Deep Q-Learning / DQN experiments

## Disclaimer

This is an unofficial educational project inspired by Dota-style jungle farming mechanics.

Dota and related names, characters and assets are trademarks or intellectual property of their respective owners.

This project is not affiliated with or endorsed by Valve Corporation.

## License
This project is licensed under the" GNU General Public License v3.0" License.

See the LICENSE file for details.
This project is licensed under the MIT License.

See the `LICENSE` file for details.
