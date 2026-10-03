import math, queue, random, threading, tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

# ---------- Config ----------
MAP, CW, CH = 11000, 800, 680
SIM_TIME, SPEED, RESPAWN = 300.0, 470.0, 60.0
FRAME_MS, TIME_SCALE = 40, 8.0
DAMAGE_MIN, DAMAGE_MAX, DAMAGE_DEFAULT = 50, 1000, 500

HP = {"SMALL": 500, "MEDIUM": 900, "LARGE": 1500, "ANCIENT": 3000}
COLOR = {"SMALL": "#22c55e", "MEDIUM": "#facc15",
         "LARGE": "#ef4444", "ANCIENT": "#a855f7"}

EPISODES, BUCKET = 12000, 5.0
ALPHA, GAMMA = 0.15, 0.98
EPS_START, EPS_MIN, EPS_DECAY = 1.0, 0.05, 0.9995

CAMPS = [
    ("R-A1",2100,7100,"ANCIENT"), ("R-A2",3900,8200,"ANCIENT"),
    ("R-L1",2500,5900,"LARGE"),   ("R-L2",4200,6200,"LARGE"),
    ("R-L3",5200,7300,"LARGE"),   ("R-L4",6500,7800,"LARGE"),
    ("R-L5",7600,9000,"LARGE"),   ("R-M1",1500,5000,"MEDIUM"),
    ("R-M2",3300,5300,"MEDIUM"),  ("R-M3",4700,5700,"MEDIUM"),
    ("R-M4",5900,6700,"MEDIUM"),  ("R-M5",7200,8200,"MEDIUM"),
    ("R-S1",1800,4200,"SMALL"),   ("R-S2",3400,4400,"SMALL"),

    ("D-A1",7200,2800,"ANCIENT"), ("D-A2",8800,3900,"ANCIENT"),
    ("D-L1",7600,1800,"LARGE"),   ("D-L2",6000,2200,"LARGE"),
    ("D-L3",8300,2300,"LARGE"),   ("D-L4",6900,3400,"LARGE"),
    ("D-L5",8700,5000,"LARGE"),   ("D-M1",5800,1400,"MEDIUM"),
    ("D-M2",6800,1700,"MEDIUM"),  ("D-M3",5100,2500,"MEDIUM"),
    ("D-M4",7800,3100,"MEDIUM"),  ("D-M5",9000,4200,"MEDIUM"),
    ("D-S1",6500,1200,"SMALL"),   ("D-S2",8200,1500,"SMALL"),
]

@dataclass
class Camp:
    name: str
    x: float
    y: float
    tier: str
    ready: float = 0.0

def new_camps():
    return [Camp(*c) for c in CAMPS]

def distance(a, b, c, d):
    return math.hypot(c-a, d-b)

def fight_time(tier, damage):
    return math.ceil(HP[tier] / damage)

def mask(camps, t):
    m = 0
    for i, c in enumerate(camps):
        if t >= c.ready:
            m |= 1 << i
    return m

# ---------- RL environment ----------
class Env:
    def __init__(self, damage):
        self.damage = damage
        self.reset()

    def reset(self):
        self.camps = new_camps()
        self.x, self.y, self.t, self.last = 1000.0, 9500.0, 0.0, -1
        return self.state()

    def state(self):
        return self.last, int(self.t / BUCKET), mask(self.camps, self.t)

    def actions(self):
        return [i for i,c in enumerate(self.camps) if self.t >= c.ready]

    def step(self, i):
        c = self.camps[i]
        if self.t < c.ready:
            return self.state(), -5.0, False

        finish = self.t + distance(self.x,self.y,c.x,c.y)/SPEED + fight_time(c.tier,self.damage)
        if finish > SIM_TIME:
            self.t = SIM_TIME
            return self.state(), 0.0, True

        self.t, self.x, self.y, self.last = finish, c.x, c.y, i
        c.ready = self.t + RESPAWN
        return self.state(), 100.0, False

# ---------- Q-learning ----------
class Agent:
    def __init__(self):
        self.q, self.eps = {}, EPS_START

    def value(self, s, a):
        return self.q.get((s,a), 0.0)

    def best(self, s, actions):
        return max(actions, key=lambda a: self.value(s,a)) if actions else None

    def choose(self, s, actions):
        return random.choice(actions) if random.random() < self.eps else self.best(s, actions)

    def learn(self, s, a, r, ns, na):
        old = self.value(s,a)
        future = max((self.value(ns,x) for x in na), default=0.0)
        self.q[(s,a)] = old + ALPHA * (r + GAMMA*future - old)

def train(damage, callback):
    agent = Agent()
    scores = []

    for ep in range(EPISODES):
        env, total = Env(damage), 0.0
        s = env.state()

        while env.t < SIM_TIME:
            actions = env.actions()
            if not actions:
                break
            a = agent.choose(s, actions)
            ns, r, done = env.step(a)
            na = [] if done else env.actions()
            agent.learn(s, a, r, ns, na)
            s, total = ns, total + r
            if done:
                break

        agent.eps = max(EPS_MIN, agent.eps * EPS_DECAY)
        scores.append(total)

        if ep % 100 == 0 or ep == EPISODES-1:
            recent = scores[-100:]
            callback(ep+1, sum(recent)/len(recent), agent.eps, len(agent.q))

    return agent, scores

# ---------- GUI ----------
class App:
    BG = "#161616"

    def __init__(self, root):
        self.root = root
        root.title("Dota Farming RL")
        root.geometry("1080x700")
        root.resizable(False, False)

        self.damage = DAMAGE_DEFAULT
        self.agent = None
        self.agent_damage = None
        self.training = False
        self.running = False
        self.messages = queue.Queue()

        self.build_ui()
        self.reset()
        root.after(100, self.poll_training)

    def build_ui(self):
        main = tk.Frame(self.root, bg="#111")
        main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main, width=CW, height=CH, bg="#234d29", highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=10)

        panel = tk.Frame(main, width=240, bg=self.BG)
        panel.pack(side="right", fill="y", padx=10, pady=10)

        def label(text, **kw):
            return tk.Label(panel, text=text, bg=self.BG, fg=kw.pop("fg","white"), **kw)

        label("DOTA FARMING", font=("Arial",18,"bold")).pack(pady=12)
        label("Hero Damage").pack()
        self.damage_label = label(str(self.damage), fg="#7dd3fc", font=("Arial",18,"bold"))
        self.damage_label.pack()

        self.slider = tk.Scale(panel, from_=DAMAGE_MIN, to=DAMAGE_MAX, orient="horizontal",
                               showvalue=False, command=self.change_damage,
                               bg=self.BG, fg="white", highlightthickness=0)
        self.slider.set(self.damage)
        self.slider.pack()

        self.mode = tk.StringVar(value="NEAREST")
        for text, value in [("Nearest Camp","NEAREST"), ("Learned AI","AI")]:
            b = tk.Radiobutton(panel, text=text, value=value, variable=self.mode,
                               bg=self.BG, fg="white", selectcolor="#333",
                               activebackground=self.BG, activeforeground="white")
            b.pack(anchor="w", padx=25)
            if value == "AI":
                self.ai_button = b
                b.config(state="disabled")

        tk.Button(panel, text="START", width=20, command=self.start).pack(pady=(10,2))
        tk.Button(panel, text="RESET", width=20, command=self.reset).pack(pady=2)
        self.train_button = tk.Button(panel, text="TRAIN AI", width=20, command=self.start_training)
        self.train_button.pack(pady=2)

        self.train_label = label("AI: not trained", fg="#facc15", wraplength=220)
        self.train_label.pack(pady=8)

        self.progress = ttk.Progressbar(panel, length=210, maximum=EPISODES)
        self.progress.pack()

        label("STATS", font=("Arial",11,"bold")).pack(pady=(12,4))
        self.stats = {}
        for name in ("Time","Gold","Camps","GPM","Target"):
            row = tk.Frame(panel, bg=self.BG)
            row.pack(fill="x", padx=18)
            tk.Label(row, text=name, bg=self.BG, fg="#aaa").pack(side="left")
            value = tk.Label(row, text="0", bg=self.BG, fg="white")
            value.pack(side="right")
            self.stats[name] = value

        self.status = label("READY", fg="#22c55e", font=("Arial",10,"bold"))
        self.status.pack(pady=12)

    def change_damage(self, value):
        self.damage = int(float(value))
        self.damage_label.config(text=str(self.damage))
        valid = self.agent is not None and self.agent_damage == self.damage
        self.ai_button.config(state="normal" if valid else "disabled")
        if not valid and self.mode.get() == "AI":
            self.mode.set("NEAREST")

    def reset(self):
        self.running = False
        self.t = 0.0
        self.x, self.y, self.last = 1000.0, 9500.0, -1
        self.gold = self.kills = 0
        self.camps = new_camps()
        self.target = None
        self.phase = "IDLE"
        self.combat_left = 0.0
        self.update_stats()
        self.draw()
        self.status.config(text="READY", fg="#22c55e")

    def start(self):
        if self.running or self.training:
            return
        if self.mode.get() == "AI" and (self.agent is None or self.agent_damage != self.damage):
            self.status.config(text="TRAIN AI FIRST", fg="#facc15")
            return
        self.running = True
        self.tick()

    def start_training(self):
        if self.training:
            return
        self.running = False
        self.training = True
        damage = self.damage
        self.train_button.config(state="disabled")
        self.ai_button.config(state="disabled")
        self.train_label.config(text=f"Training at {damage} damage...", fg="#38bdf8")
        self.progress["value"] = 0

        def worker():
            try:
                def cb(ep, avg, eps, size):
                    self.messages.put(("p",ep,avg,eps,size))
                agent, scores = train(damage, cb)
                self.messages.put(("d",damage,agent,scores))
            except Exception as e:
                self.messages.put(("e",repr(e)))

        threading.Thread(target=worker, daemon=True).start()

    def poll_training(self):
        try:
            while True:
                msg = self.messages.get_nowait()

                if msg[0] == "p":
                    _, ep, avg, eps, size = msg
                    self.progress["value"] = ep
                    self.train_label.config(
                        text=f"{ep}/{EPISODES}\nAvg: {avg:.1f}  ε: {eps:.3f}\nQ: {size}",
                        fg="#38bdf8"
                    )

                elif msg[0] == "d":
                    _, damage, agent, scores = msg
                    self.agent, self.agent_damage, self.training = agent, damage, False
                    self.train_button.config(state="normal")
                    if damage == self.damage:
                        self.ai_button.config(state="normal")
                    avg = sum(scores[-100:]) / len(scores[-100:])
                    self.train_label.config(text=f"AI ready ({damage} dmg)\nAvg reward: {avg:.1f}",
                                            fg="#22c55e")

                else:
                    self.training = False
                    self.train_button.config(state="normal")
                    self.train_label.config(text=f"Error: {msg[1]}", fg="#ef4444")
        except queue.Empty:
            pass

        self.root.after(100, self.poll_training)

    def state(self):
        return self.last, int(self.t/BUCKET), mask(self.camps,self.t)

    def available(self):
        return [i for i,c in enumerate(self.camps) if self.t >= c.ready]

    def choose_target(self):
        actions = self.available()
        if not actions:
            return None
        if self.mode.get() == "AI":
            return self.agent.best(self.state(), actions)
        return min(actions, key=lambda i: distance(self.x,self.y,self.camps[i].x,self.camps[i].y))

    def tick(self):
        if not self.running:
            return

        remaining = FRAME_MS/1000 * TIME_SCALE

        while remaining > 0 and self.t < SIM_TIME:
            dt = min(0.05, remaining)

            if self.target is None:
                self.target = self.choose_target()
                if self.target is None:
                    self.t += dt
                    remaining -= dt
                    continue
                self.phase = "MOVE"

            c = self.camps[self.target]

            if self.phase == "MOVE":
                dx, dy = c.x-self.x, c.y-self.y
                d = math.hypot(dx,dy)
                move = SPEED*dt

                if d <= move:
                    self.x, self.y = c.x, c.y
                    self.phase = "FIGHT"
                    self.combat_left = fight_time(c.tier,self.damage)
                else:
                    self.x += dx/d*move
                    self.y += dy/d*move

            else:
                self.combat_left -= dt
                if self.combat_left <= 0:
                    c.ready = self.t + RESPAWN
                    self.gold += 100
                    self.kills += 1
                    self.last = self.target
                    self.target = None
                    self.phase = "IDLE"

            self.t += dt
            remaining -= dt

        if self.t >= SIM_TIME:
            self.t = SIM_TIME
            self.running = False
            self.status.config(text="FINISHED", fg="#22c55e")
        else:
            self.status.config(text="RUNNING", fg="#22c55e")
            self.root.after(FRAME_MS, self.tick)

        self.update_stats()
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0,0,CW,CH,fill="#234d29",outline="")
        c.create_line(0,CH,CW,0,fill="#356b7a",width=38)

        def screen(x,y):
            return x/MAP*CW, y/MAP*CH

        for camp in self.camps:
            x,y = screen(camp.x,camp.y)
            fill = COLOR[camp.tier] if self.t >= camp.ready else "#555"
            c.create_oval(x-8,y-8,x+8,y+8,fill=fill,outline="white")
            c.create_text(x,y-16,text=camp.name,fill="white",font=("Arial",7))

        hx,hy = screen(self.x,self.y)

        if self.target is not None:
            tx,ty = screen(self.camps[self.target].x,self.camps[self.target].y)
            c.create_line(hx,hy,tx,ty,fill="white",dash=(4,4))

        c.create_oval(hx-12,hy-12,hx+12,hy+12,fill="#60a5fa",outline="white")
        c.create_text(hx,hy,text="P",fill="white",font=("Arial",11,"bold"))

    def update_stats(self):
        self.stats["Time"].config(text=f"{self.t:.1f}/{SIM_TIME:.0f}s")
        self.stats["Gold"].config(text=str(self.gold))
        self.stats["Camps"].config(text=str(self.kills))
        self.stats["GPM"].config(text=f"{self.gold/self.t*60:.0f}" if self.t else "0")
        self.stats["Target"].config(
            text=self.camps[self.target].name if self.target is not None else "-"
        )

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
