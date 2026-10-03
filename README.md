# Erkam-inci-BOZ213d01u01
A Dota-inspired jungle farming simulator using Q-learning to learn and visualize efficient farming routes.

# Dota Farming RL

A simple Dota-inspired jungle farming simulator built with Python and Tkinter.

The project uses **Q-learning** to learn jungle farming routes and compares the learned strategy with a simple **nearest-camp heuristic**.

The goal is to experiment with reinforcement learning, route selection, and game AI in a small visual environment.

## Features

- Dota-inspired jungle farming simulation
- Tabular Q-learning agent
- Nearest-camp baseline strategy
- Adjustable hero damage
- Small, Medium, Large, and Ancient camps
- Camp respawn system
- Travel and combat time simulation
- Real-time Tkinter visualization
- Background AI training
- Training progress display
- Gold, camps cleared, GPM, time, and target statistics

## How It Works

The map contains 28 simplified jungle camps.

Each camp has:

- A position
- A camp type
- A health value
- A respawn timer

The hero moves between camps, clears them, and receives **100 gold** for each completed camp.

Combat duration depends on the hero's damage and the camp's health.

The simulation lasts **300 simulated seconds**.

## Q-Learning

The AI uses tabular Q-learning.

The state is represented as:

```text
(
    last_camp,
    time_bucket,
    available_camps_mask
)
```

Where:

- `last_camp` is the previously cleared camp
- `time_bucket` represents the current simulation time
- `available_camps_mask` represents which camps are currently available

The action is simply:

```text
Choose the next jungle camp.
```

The agent receives a reward when it successfully clears a camp.

The Q-learning update is:

```text
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

The default parameters are:

```python
EPISODES = 12000
ALPHA = 0.15
GAMMA = 0.98

EPS_START = 1.0
EPS_MIN = 0.05
EPS_DECAY = 0.9995
```

An epsilon-greedy strategy is used during training so that the agent gradually moves from exploration toward learned decisions.

## Decision Modes

### Nearest Camp

The baseline strategy always selects the closest currently available camp.

### Learned AI

The Q-learning agent selects the next camp according to its learned Q-values.

The AI is trained for the currently selected hero damage.

If the damage value is changed, the AI must be trained again.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/radagaserkam/Erkam-inci-BOZ213d01u01.git
cd Erkam-inci-BOZ213d01u01
```

Run the program:

```bash
python dota 2 AI train.py
```

or:

```bash
python3 dota 2 AI train.py
```

## Requirements

- Python 3
- Tkinter

No machine learning libraries such as TensorFlow or PyTorch are required.

The reinforcement learning algorithm is implemented directly in Python.

> On some Linux distributions, Tkinter may need to be installed separately.

## Usage

1. Start the program.
2. Select the hero damage.
3. Use **Nearest Camp** to run the baseline strategy.
4. Click **Train AI**.
5. Wait for the Q-learning training to finish.
6. Select **Learned AI**.
7. Reset and start the simulation.
8. Compare the resulting route and GPM.

## Simplifications

This is not intended to reproduce Dota gameplay accurately.

The simulator does not include mechanics such as:

- Real map geometry
- Trees and cliffs
- Pathfinding
- Vision
- Neutral creep abilities
- Camp stacking
- Pulling
- Hero abilities
- Real combat mechanics

Movement between camps is calculated using straight-line distance.

The project is primarily an experiment in **reinforcement learning and route optimization**.

## Possible Improvements

Future additions could include:

- More accurate map geometry
- Pathfinding
- Different rewards for different camp types
- Saving and loading trained Q-tables
- Training performance graphs
- Camp stacking
- Multiple heroes
- More realistic combat
- Comparison with other reinforcement learning algorithms

## Disclaimer

This is an unofficial educational project inspired by Dota-style jungle farming mechanics.

Dota and related names are the property of their respective owners.

This project is not affiliated with or endorsed by Valve Corporation.

## License
This project is licensed under the" GNU General Public License v3.0" License.

See the LICENSE file for details.
This project is licensed under the" GNU General Public License v3.0" License.
See the `LICENSE` file for details.
