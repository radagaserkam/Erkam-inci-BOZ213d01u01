import tkinter as tk
from tkinter import ttk
import math
import os
import threading
import queue
import random
from dataclasses import dataclass


# ============================================================
# CONFIGURATION
# ============================================================

MAP_SIZE = 11000

SIMULATION_TIME = 300.0        # 5 simulated minutes
TIME_MULTIPLIER = 8.0          # GUI runs 8x faster than real time
FRAME_MS = 40

HERO_SPEED = 300.0

MIN_DAMAGE = 50
MAX_DAMAGE = 300
INITIAL_DAMAGE = 100

ATTACK_INTERVAL = 1.0

CAMP_RESPAWN = 60.0
CREEP_GOLD = 100
CREEP_XP = 100

# Combat duration by camp tier.
# Ancient is intentionally much slower.
CAMP_HP = {
    "SMALL": 500,
    "MEDIUM": 900,
    "LARGE": 1500,
    "ANCIENT": 3000,
}

CAMP_COLORS = {
    "SMALL": "#22c55e",
    "MEDIUM": "#facc15",
    "LARGE": "#ef4444",
    "ANCIENT": "#a855f7",
}

CAMP_LABELS = {
    "SMALL": "Small",
    "MEDIUM": "Medium",
    "LARGE": "Large",
    "ANCIENT": "Ancient",
}

# Reinforcement Learning
TRAIN_EPISODES = 12000
TIME_BUCKET = 5.0
LEARNING_RATE = 0.15
DISCOUNT = 0.98
EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.9995

# Steam CDN Puck icon

def load_puck(self):
    # İnternet gerektirmeyen basit Puck benzeri PNG üretimi.
    # Tkinter kendi içinde bu PNG'yi yükleyebilir.

    import base64

    puck_png = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMA"
        "AAsTAAALEwEAmpwYAAABM0lEQVR4nO2WsUoDQRRFz8xM7S2CkV9F"
        "i1gQhY3Y2NnY2JjY2FhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
        "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
    )

    try:
        data = base64.b64decode(puck_png)
        self.puck_image = tk.PhotoImage(data=data)

        if self.puck_image.width() > 40:
            factor = max(
                1,
                math.ceil(self.puck_image.width() / 40)
            )

            self.puck_image = self.puck_image.subsample(
                factor,
                factor
            )

    except Exception:
        self.puck_image = None

# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Camp:
    camp_id: str
    x: float
    y: float
    tier: str
    available_at: float = 0.0
    alive: bool = True


@dataclass
class Hero:
    x: float
    y: float
    gold: int = 0
    xp: int = 0
    camps_killed: int = 0
    score: float = 0.0


# ============================================================
# MAP
# ============================================================

def create_camps():
    """
    Approximate overhead Dota-style camp coordinates.
    These are intentionally simplified for the simulator:
    no trees, cliffs, wards, blockers or terrain collision.
    """

    return [
        # ---------------- RADIANT ----------------
        Camp("R-A1", 2100, 7100, "ANCIENT"),
        Camp("R-A2", 3900, 8200, "ANCIENT"),

        Camp("R-L1", 2500, 5900, "LARGE"),
        Camp("R-L2", 4200, 6200, "LARGE"),
        Camp("R-L3", 5200, 7300, "LARGE"),
        Camp("R-L4", 6500, 7800, "LARGE"),
        Camp("R-L5", 7600, 9000, "LARGE"),

        Camp("R-M1", 1500, 5000, "MEDIUM"),
        Camp("R-M2", 3300, 5300, "MEDIUM"),
        Camp("R-M3", 4700, 5700, "MEDIUM"),
        Camp("R-M4", 5900, 6700, "MEDIUM"),
        Camp("R-M5", 7200, 8200, "MEDIUM"),

        Camp("R-S1", 1800, 4200, "SMALL"),
        Camp("R-S2", 3400, 4400, "SMALL"),

        # ---------------- DIRE ----------------
        Camp("D-A1", 7200, 2800, "ANCIENT"),
        Camp("D-A2", 8800, 3900, "ANCIENT"),

        Camp("D-L1", 7600, 1800, "LARGE"),
        Camp("D-L2", 6000, 2200, "LARGE"),
        Camp("D-L3", 8300, 2300, "LARGE"),
        Camp("D-L4", 6900, 3400, "LARGE"),
        Camp("D-L5", 8700, 5000, "LARGE"),

        Camp("D-M1", 5800, 1400, "MEDIUM"),
        Camp("D-M2", 6800, 1700, "MEDIUM"),
        Camp("D-M3", 5100, 2500, "MEDIUM"),
        Camp("D-M4", 7800, 3100, "MEDIUM"),
        Camp("D-M5", 9000, 4200, "MEDIUM"),

        Camp("D-S1", 6500, 1200, "SMALL"),
        Camp("D-S2", 8200, 1500, "SMALL"),
    ]


# ============================================================
# HELPERS
# ============================================================

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def travel_time(hero_x, hero_y, camp):
    return distance(hero_x, hero_y, camp.x, camp.y) / HERO_SPEED


def combat_time(camp_tier, damage):
    hp = CAMP_HP[camp_tier]
    attacks = math.ceil(hp / max(1, damage))
    return attacks * ATTACK_INTERVAL


def nearest_available_camp(hero_x, hero_y, camps, current_time):
    available = [
        camp for camp in camps
        if camp.alive and camp.available_at <= current_time
    ]

    if not available:
        return None

    return min(
        available,
        key=lambda camp: distance(hero_x, hero_y, camp.x, camp.y)
    )


def available_mask(camps, current_time):
    mask = 0
    for i, camp in enumerate(camps):
        if camp.alive and camp.available_at <= current_time:
            mask |= (1 << i)
    return mask


# ============================================================
# RL ENVIRONMENT
# ============================================================

class FarmingEnvironment:
    """
    Discrete reinforcement-learning environment.

    State:
        current camp/location index
        time bucket
        camp availability bitmask

    Action:
        choose one of the 28 camps

    Reward:
        +100 gold when a camp is fully cleared.

    The episode lasts 120 simulated seconds.
    """

    def __init__(self, damage):
        self.damage = int(damage)
        self.num_camps = len(create_camps())
        self.reset()

    def reset(self):
        self.camps = create_camps()
        self.hero_x = 1000.0
        self.hero_y = 9500.0
        self.current_time = 0.0
        self.current_location = -1

    def state(self):
        bucket = int(self.current_time / TIME_BUCKET)
        mask = available_mask(self.camps, self.current_time)
        return (
            self.current_location,
            bucket,
            mask,
        )

    def valid_actions(self):
        return [
            i for i, camp in enumerate(self.camps)
            if camp.alive and camp.available_at <= self.current_time
        ]

    def step(self, action_index):
        """
        Execute one complete decision:
        travel -> fight -> clear -> respawn scheduling.
        """

        if self.current_time >= SIMULATION_TIME:
            return self.state(), 0.0, True

        camp = self.camps[action_index]

        if not (camp.alive and camp.available_at <= self.current_time):
            # Invalid action. Small penalty and continue.
            return self.state(), -5.0, False

        travel = distance(
            self.hero_x,
            self.hero_y,
            camp.x,
            camp.y
        ) / HERO_SPEED

        fight = combat_time(camp.tier, self.damage)

        duration = travel + fight
        finish_time = self.current_time + duration

        # The camp is only cleared if the hero has enough time
        # to finish the combat before the episode ends.
        if finish_time > SIMULATION_TIME:
            self.current_time = SIMULATION_TIME
            return self.state(), 0.0, True

        self.current_time = finish_time
        self.hero_x = camp.x
        self.hero_y = camp.y
        self.current_location = action_index

        camp.alive = False
        camp.available_at = self.current_time + CAMP_RESPAWN

        reward = float(CREEP_GOLD)

        done = self.current_time >= SIMULATION_TIME
        return self.state(), reward, done


# ============================================================
# Q-LEARNING AGENT
# ============================================================

class QLearningAgent:
    def __init__(self):
        self.q = {}
        self.epsilon = EPSILON_START

    def value(self, state, action):
        return self.q.get((state, action), 0.0)

    def best_action(self, state, valid_actions):
        if not valid_actions:
            return None

        return max(
            valid_actions,
            key=lambda action: self.value(state, action)
        )

    def choose_action(self, state, valid_actions, training=True):
        if not valid_actions:
            return None

        if training and random.random() < self.epsilon:
            return random.choice(valid_actions)

        return self.best_action(state, valid_actions)

    def update(self, state, action, reward, next_state, next_actions):
        old_q = self.value(state, action)

        if next_actions:
            next_best = max(
                self.value(next_state, a)
                for a in next_actions
            )
        else:
            next_best = 0.0

        new_q = old_q + LEARNING_RATE * (
            reward + DISCOUNT * next_best - old_q
        )

        self.q[(state, action)] = new_q

    def decay(self):
        self.epsilon = max(
            EPSILON_MIN,
            self.epsilon * EPSILON_DECAY
        )


# ============================================================
# TRAINER
# ============================================================

def train_agent(damage, progress_callback=None):
    """
    Train without GUI rendering.

    Returns:
        QLearningAgent
        training statistics
    """

    agent = QLearningAgent()
    scores = []

    for episode in range(TRAIN_EPISODES):
        env = FarmingEnvironment(damage)

        total_reward = 0.0
        state = env.state()

        while env.current_time < SIMULATION_TIME:

            actions = env.valid_actions()

            if not actions:
                break

            action = agent.choose_action(
                state,
                actions,
                training=True
            )

            next_state, reward, done = env.step(action)

            next_actions = (
                env.valid_actions()
                if not done else []
            )

            agent.update(
                state,
                action,
                reward,
                next_state,
                next_actions
            )

            total_reward += reward
            state = next_state

            if done:
                break

        agent.decay()
        scores.append(total_reward)

        if progress_callback and (
            episode % 100 == 0
            or episode == TRAIN_EPISODES - 1
        ):
            recent = scores[-100:]
            avg = sum(recent) / len(recent)

            progress_callback(
                episode + 1,
                TRAIN_EPISODES,
                avg,
                agent.epsilon,
                len(agent.q)
            )

    return agent, scores


# ============================================================
# GUI SIMULATOR
# ============================================================

class FarmingSimulator:
    def __init__(self, root):
        self.root = root

        root.title("Dota Jungle Farming Simulator + Reinforcement Learning")
        root.geometry("1120x720")
        root.resizable(False, False)

        self.sim_time = 0.0
        self.running = False

        self.damage = INITIAL_DAMAGE

        self.hero = Hero(
            x=1000,
            y=9500
        )

        self.camps = create_camps()
        self.target = None
        self.combat_remaining = 0.0

        self.total_travel = 0.0
        self.total_combat = 0.0

        self.q_agent = None
        self.ai_damage = None
        self.play_mode = "NEAREST"

        self.training_thread = None
        self.training_queue = queue.Queue()
        self.training_in_progress = False

        self.puck_image = None

        self.create_gui()

        self.load_puck_image()
        self.reset()

    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------

    def create_gui(self):
        main = tk.Frame(self.root, bg="#111111")
        main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            main,
            width=810,
            height=690,
            bg="#234d29",
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            padx=(10, 5),
            pady=10
        )

        panel = tk.Frame(
            main,
            width=275,
            bg="#161616"
        )
        panel.pack(
            side="right",
            fill="y",
            padx=(5, 10),
            pady=10
        )

        tk.Label(
            panel,
            text="DOTA FARMING",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#161616"
        ).pack(pady=(16, 10))

        # Damage
        tk.Label(
            panel,
            text="Hero Damage",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#161616"
        ).pack()

        self.damage_value = tk.Label(
            panel,
            text=str(self.damage),
            font=("Arial", 20, "bold"),
            fg="#7dd3fc",
            bg="#161616"
        )
        self.damage_value.pack(pady=3)

        self.damage_slider = tk.Scale(
            panel,
            from_=MIN_DAMAGE,
            to=MAX_DAMAGE,
            orient="horizontal",
            length=200,
            showvalue=False,
            command=self.change_damage,
            bg="#161616",
            fg="white",
            troughcolor="#333333",
            highlightthickness=0
        )
        self.damage_slider.set(INITIAL_DAMAGE)
        self.damage_slider.pack()

        # Mode
        tk.Label(
            panel,
            text="Decision Mode",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#161616"
        ).pack(pady=(10, 3))

        self.mode_var = tk.StringVar(value="NEAREST")

        tk.Radiobutton(
            panel,
            text="Nearest Camp (baseline)",
            variable=self.mode_var,
            value="NEAREST",
            command=self.change_mode,
            bg="#161616",
            fg="white",
            selectcolor="#333333",
            activebackground="#161616",
            activeforeground="white"
        ).pack(anchor="w", padx=18)

        self.ai_radio = tk.Radiobutton(
            panel,
            text="Learned AI",
            variable=self.mode_var,
            value="AI",
            command=self.change_mode,
            bg="#161616",
            fg="white",
            selectcolor="#333333",
            activebackground="#161616",
            activeforeground="white",
            state="disabled"
        )
        self.ai_radio.pack(anchor="w", padx=18)

        # Buttons
        self.start_button = tk.Button(
            panel,
            text="START",
            width=20,
            command=self.start
        )
        self.start_button.pack(pady=(12, 5))

        self.reset_button = tk.Button(
            panel,
            text="RESET",
            width=20,
            command=self.reset
        )
        self.reset_button.pack(pady=2)

        self.train_button = tk.Button(
            panel,
            text="TRAIN AI",
            width=20,
            command=self.start_training
        )
        self.train_button.pack(pady=(5, 2))

        # Training status
        self.training_label = tk.Label(
            panel,
            text="AI: not trained",
            font=("Arial", 9, "bold"),
            fg="#facc15",
            bg="#161616",
            wraplength=235
        )
        self.training_label.pack(pady=(4, 8))

        # Divider
        tk.Label(
            panel,
            text="CAMP TYPES",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#161616"
        ).pack(pady=(4, 6))

        self.create_legend(panel, "ANCIENT")
        self.create_legend(panel, "LARGE")
        self.create_legend(panel, "MEDIUM")
        self.create_legend(panel, "SMALL")

        # Stats
        tk.Label(
            panel,
            text="STATS",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#161616"
        ).pack(pady=(10, 5))

        self.time_label = self.create_stat(panel, "Time")
        self.gold_label = self.create_stat(panel, "Gold")
        self.xp_label = self.create_stat(panel, "XP")
        self.camp_label = self.create_stat(panel, "Camps")
        self.score_label = self.create_stat(panel, "Score")
        self.gpm_label = self.create_stat(panel, "GPM")
        self.target_label = self.create_stat(panel, "Target")

        self.status_label = tk.Label(
            panel,
            text="READY",
            font=("Arial", 10, "bold"),
            fg="#22c55e",
            bg="#161616",
            wraplength=235
        )
        self.status_label.pack(pady=12)

        # Training progress
        self.progress = ttk.Progressbar(
            panel,
            orient="horizontal",
            length=220,
            mode="determinate",
            maximum=TRAIN_EPISODES
        )
        self.progress.pack(pady=(0, 5))

        self.root.after(100, self.poll_training_queue)

    def create_legend(self, parent, tier):
        row = tk.Frame(parent, bg="#161616")
        row.pack(fill="x", padx=25, pady=1)

        swatch = tk.Canvas(
            row,
            width=14,
            height=14,
            bg="#161616",
            highlightthickness=0
        )
        swatch.pack(side="left", padx=(0, 7))

        swatch.create_oval(
            2, 2, 12, 12,
            fill=CAMP_COLORS[tier],
            outline="white"
        )

        tk.Label(
            row,
            text=CAMP_LABELS[tier],
            fg="white",
            bg="#161616",
            anchor="w"
        ).pack(side="left")

        hp = CAMP_HP[tier]
        tk.Label(
            row,
            text=f"{hp} HP",
            fg="#999999",
            bg="#161616",
            anchor="e"
        ).pack(side="right")

    def create_stat(self, parent, name):
        row = tk.Frame(parent, bg="#161616")
        row.pack(fill="x", padx=18, pady=1)

        tk.Label(
            row,
            text=name,
            fg="#aaaaaa",
            bg="#161616"
        ).pack(side="left")

        value = tk.Label(
            row,
            text="0",
            fg="white",
            bg="#161616"
        )
        value.pack(side="right")

        return value

    # --------------------------------------------------------
    # Puck icon
    # --------------------------------------------------------

    def load_puck_image(self):
        try:
            if not os.path.exists(PUCK_FILE):
                urllib.request.urlretrieve(PUCK_URL, PUCK_FILE)

            self.puck_image = tk.PhotoImage(file=PUCK_FILE)

            # Keep the sprite compact.
            w = self.puck_image.width()
            if w > 48:
                factor = max(1, math.ceil(w / 40))
                self.puck_image = self.puck_image.subsample(
                    factor,
                    factor
                )
        except Exception:
            self.puck_image = None

    # --------------------------------------------------------
    # User controls
    # --------------------------------------------------------

    def change_damage(self, value):
        new_damage = int(float(value))
        self.damage = new_damage
        self.damage_value.config(text=str(new_damage))

        # A model trained for a different damage value is not valid.
        if self.ai_damage != self.damage:
            self.ai_radio.config(state="disabled")
            if self.mode_var.get() == "AI":
                self.mode_var.set("NEAREST")
                self.play_mode = "NEAREST"

            if self.q_agent is not None:
                self.training_label.config(
                    text=(
                        f"AI model trained at {self.ai_damage} damage. "
                        f"Retrain for {self.damage}."
                    ),
                    fg="#facc15"
                )
        else:
            if self.q_agent is not None:
                self.ai_radio.config(state="normal")

    def change_mode(self):
        self.play_mode = self.mode_var.get()

    # --------------------------------------------------------
    # Reset / start
    # --------------------------------------------------------

    def reset(self):
        self.running = False

        self.sim_time = 0.0

        self.hero = Hero(
            x=1000,
            y=9500
        )

        self.camps = create_camps()

        self.target = None
        self.combat_remaining = 0.0

        self.total_travel = 0.0
        self.total_combat = 0.0

        self.progress["value"] = 0

        self.update_stats()
        self.draw_everything()

        if self.training_in_progress:
            self.status_label.config(
                text="AI TRAINING RUNS IN BACKGROUND"
            )
        else:
            self.status_label.config(
                text="READY",
                fg="#22c55e"
            )

    def start(self):
        if self.training_in_progress:
            return

        if self.running:
            return

        if self.play_mode == "AI":
            if self.q_agent is None or self.ai_damage != self.damage:
                self.status_label.config(
                    text="TRAIN AI FIRST",
                    fg="#facc15"
                )
                return

        self.running = True

        self.status_label.config(
            text="RUNNING",
            fg="#22c55e"
        )

        self.update()

    # --------------------------------------------------------
    # AI training
    # --------------------------------------------------------

    def start_training(self):
        if self.training_in_progress:
            return

        if self.running:
            self.running = False

        damage_for_training = self.damage

        self.training_in_progress = True
        self.train_button.config(state="disabled")
        self.ai_radio.config(state="disabled")
        self.training_label.config(
            text=f"Training at {damage_for_training} damage...",
            fg="#38bdf8"
        )

        self.progress["value"] = 0

        self.training_thread = threading.Thread(
            target=self._training_worker,
            args=(damage_for_training,),
            daemon=True
        )
        self.training_thread.start()

    def _training_worker(self, damage):
        try:
            def callback(ep, total, avg, epsilon, q_size):
                self.training_queue.put(
                    ("progress", ep, total, avg, epsilon, q_size)
                )

            agent, scores = train_agent(
                damage,
                progress_callback=callback
            )

            self.training_queue.put(
                ("done", damage, agent, scores)
            )

        except Exception as error:
            self.training_queue.put(
                ("error", repr(error))
            )

    def poll_training_queue(self):
        try:
            while True:
                message = self.training_queue.get_nowait()

                if message[0] == "progress":
                    _, ep, total, avg, epsilon, q_size = message

                    self.progress["maximum"] = total
                    self.progress["value"] = ep

                    self.training_label.config(
                        text=(
                            f"Training {ep}/{total}\n"
                            f"Avg reward: {avg:.1f}\n"
                            f"Epsilon: {epsilon:.3f}\n"
                            f"Q entries: {q_size}"
                        ),
                        fg="#38bdf8"
                    )

                elif message[0] == "done":
                    _, damage, agent, scores = message

                    self.q_agent = agent
                    self.ai_damage = damage

                    self.training_in_progress = False
                    self.train_button.config(state="normal")
                    self.ai_radio.config(state="normal")

                    recent = scores[-100:]
                    avg = sum(recent) / len(recent)

                    self.training_label.config(
                        text=(
                            f"AI trained at {damage} damage\n"
                            f"Avg final reward: {avg:.1f}\n"
                            f"Q entries: {len(agent.q)}"
                        ),
                        fg="#22c55e"
                    )

                    self.status_label.config(
                        text="AI READY",
                        fg="#22c55e"
                    )

                elif message[0] == "error":
                    self.training_in_progress = False
                    self.train_button.config(state="normal")
                    self.training_label.config(
                        text=f"Training error: {message[1]}",
                        fg="#ef4444"
                    )

        except queue.Empty:
            pass

        self.root.after(100, self.poll_training_queue)

    # --------------------------------------------------------
    # Target selection
    # --------------------------------------------------------

    def current_state(self):
        bucket = int(self.sim_time / TIME_BUCKET)
        mask = available_mask(self.camps, self.sim_time)

        if self.target is None:
            current_location = -1
        else:
            current_location = self.camps.index(self.target)

        return (
            current_location,
            bucket,
            mask
        )

    def choose_target(self):
        available = [
            (i, camp)
            for i, camp in enumerate(self.camps)
            if camp.alive and camp.available_at <= self.sim_time
        ]

        if not available:
            return None

        # --------------------------------------------
        # Learned AI
        # --------------------------------------------
        if (
            self.play_mode == "AI"
            and self.q_agent is not None
            and self.ai_damage == self.damage
        ):
            state = self.current_state()

            action = self.q_agent.best_action(
                state,
                [i for i, _ in available]
            )

            if action is not None:
                return self.camps[action]

        # --------------------------------------------
        # Baseline: nearest camp
        # --------------------------------------------
        return min(
            (camp for _, camp in available),
            key=lambda camp: distance(
                self.hero.x,
                self.hero.y,
                camp.x,
                camp.y
            )
        )

    # --------------------------------------------------------
    # Combat / finish
    # --------------------------------------------------------

    def start_combat(self):
        if self.target is None:
            return

        self.combat_remaining = combat_time(
            self.target.tier,
            self.damage
        )

        self.status_label.config(
            text=f"FIGHTING {self.target.camp_id}",
            fg="#ef4444"
        )

    def finish_camp(self):
        if self.target is None:
            return

        camp = self.target

        camp.alive = False
        camp.available_at = self.sim_time + CAMP_RESPAWN

        self.hero.gold += CREEP_GOLD
        self.hero.xp += CREEP_XP
        self.hero.camps_killed += 1
        self.hero.score += CREEP_GOLD

        self.target = None
        self.combat_remaining = 0.0

        self.status_label.config(
            text="CHOOSING NEXT CAMP",
            fg="#facc15"
        )

    # --------------------------------------------------------
    # Simulation
    # --------------------------------------------------------

    def update(self):
        if not self.running:
            return

        real_seconds = FRAME_MS / 1000.0
        sim_delta = real_seconds * TIME_MULTIPLIER
        remaining = sim_delta

        while remaining > 0:
            step = min(remaining, 0.05)
            self.sim_time += step

            if self.target is None:
                self.target = self.choose_target()

                if self.target is None:
                    remaining -= step
                    continue

                self.status_label.config(
                    text=f"GOING TO {self.target.camp_id}",
                    fg="#38bdf8"
                )

            # Movement
            if self.target is not None and self.combat_remaining <= 0:
                target = self.target

                dx = target.x - self.hero.x
                dy = target.y - self.hero.y
                dist = math.hypot(dx, dy)

                if dist > 1:
                    move_distance = HERO_SPEED * step

                    if move_distance >= dist:
                        self.hero.x = target.x
                        self.hero.y = target.y
                        self.start_combat()
                    else:
                        ratio = move_distance / dist
                        self.hero.x += dx * ratio
                        self.hero.y += dy * ratio

                    self.total_travel += step
                else:
                    self.start_combat()

            # Combat
            if self.combat_remaining > 0:
                fight_step = min(step, self.combat_remaining)
                self.combat_remaining -= fight_step
                self.total_combat += fight_step

                if self.combat_remaining <= 0:
                    self.finish_camp()

            remaining -= step

        # Respawns
        for camp in self.camps:
            if (
                not camp.alive
                and self.sim_time >= camp.available_at
            ):
                camp.alive = True

        # End
        if self.sim_time >= SIMULATION_TIME:
            self.sim_time = SIMULATION_TIME
            self.running = False
            self.status_label.config(
                text="FINISHED",
                fg="#22c55e"
            )

        self.update_stats()
        self.draw_everything()

        if self.running:
            self.root.after(FRAME_MS, self.update)

    # --------------------------------------------------------
    # Drawing
    # --------------------------------------------------------

    def world_to_screen(self, x, y):
        return (
            (x / MAP_SIZE) * 810,
            (y / MAP_SIZE) * 690
        )

    def draw_everything(self):
        self.canvas.delete("all")

        width = 810
        height = 690

        # Background
        self.canvas.create_rectangle(
            0, 0, width, height,
            fill="#234d29",
            outline=""
        )

        # Simplified river
        self.canvas.create_line(
            0, height,
            width, 0,
            fill="#356b7a",
            width=38
        )

        # Map border
        self.canvas.create_rectangle(
            3, 3, width - 3, height - 3,
            outline="#8a8a8a",
            width=2
        )

        # Camps
        for camp in self.camps:
            sx, sy = self.world_to_screen(camp.x, camp.y)

            if camp.alive:
                color = CAMP_COLORS[camp.tier]
            else:
                color = "#555555"

            self.canvas.create_oval(
                sx - 9, sy - 9,
                sx + 9, sy + 9,
                fill=color,
                outline="white",
                width=1
            )

            self.canvas.create_text(
                sx,
                sy - 18,
                text=camp.camp_id,
                fill="white",
                font=("Arial", 7)
            )

        # Target path
        if self.target is not None:
            tx, ty = self.world_to_screen(
                self.target.x,
                self.target.y
            )
            hx, hy = self.world_to_screen(
                self.hero.x,
                self.hero.y
            )

            self.canvas.create_line(
                hx, hy, tx, ty,
                fill="#ffffff",
                dash=(4, 4),
                width=2
            )

        # Puck
        hx, hy = self.world_to_screen(
            self.hero.x,
            self.hero.y
        )

        if self.puck_image is not None:
            self.canvas.create_image(
                hx,
                hy,
                image=self.puck_image
            )
        else:
            self.canvas.create_oval(
                hx - 13, hy - 13,
                hx + 13, hy + 13,
                fill="#60a5fa",
                outline="white",
                width=2
            )
            self.canvas.create_text(
                hx, hy,
                text="P",
                fill="white",
                font=("Arial", 12, "bold")
            )

        self.canvas.create_text(
            hx,
            hy + 25,
            text="PUCK",
            fill="white",
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # Stats
    # --------------------------------------------------------

    def update_stats(self):
        self.time_label.config(
            text=f"{self.sim_time:.1f}s / {SIMULATION_TIME:.0f}s"
        )

        self.gold_label.config(text=str(self.hero.gold))
        self.xp_label.config(text=str(self.hero.xp))
        self.camp_label.config(text=str(self.hero.camps_killed))
        self.score_label.config(text=f"{self.hero.score:.0f}")

        if self.sim_time > 0:
            gpm = self.hero.gold / self.sim_time * 60
        else:
            gpm = 0

        self.gpm_label.config(text=f"{gpm:.0f}")

        if self.target is not None:
            self.target_label.config(
                text=f"{self.target.camp_id} ({self.target.tier})"
            )
        else:
            self.target_label.config(text="-")


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = FarmingSimulator(root)
    root.mainloop()

compile(code, '<string>', 'exec')
print("syntax ok", len(code.splitlines()))


print("PROGRAM BASLADI")

if __name__ == "__main__":
    print("MAIN CALISIYOR")
    root = tk.Tk()
    app = FarmingSimulator(root)
    root.mainloop()
