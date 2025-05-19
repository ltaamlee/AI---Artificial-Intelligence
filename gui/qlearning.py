# File: qlearning_8puzzle_gui.py

import tkinter as tk
from tkinter import messagebox, font
import random
from copy import deepcopy

ACTIONS = [0, 1, 2, 3]  # 0: Up, 1: Down, 2: Left, 3: Right
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def state_to_tuple(state):
    return tuple(map(tuple, state))

def is_solvable(state):
    flat = [x for row in state for x in row if x != 0]
    inv = sum(1 for i in range(len(flat)) for j in range(i+1, len(flat)) if flat[i] > flat[j])
    return inv % 2 == 0

def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val == 0:
                continue
            target_i = (val - 1) // 3
            target_j = (val - 1) % 3
            distance += abs(i - target_i) + abs(j - target_j)
    return distance

def get_zero_pos(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def step(state, action):
    i, j = get_zero_pos(state)
    new_i, new_j = i, j
    if action == 0: new_i -= 1
    elif action == 1: new_i += 1
    elif action == 2: new_j -= 1
    elif action == 3: new_j += 1
    if 0 <= new_i < 3 and 0 <= new_j < 3:
        new_state = [row[:] for row in state]
        new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
        reward = 100 if new_state == GOAL else -manhattan(new_state)
        return new_state, reward, new_state == GOAL
    return state, -5, False

def max_q_action(q_table, state):
    st = state_to_tuple(state)
    if st not in q_table:
        q_table[st] = {a: 0.0 for a in ACTIONS}
    return max(q_table[st], key=q_table[st].get)

def generate_near_goal_state(goal, steps=5):
    state = deepcopy(goal)
    for _ in range(steps):
        valid = []
        for a in ACTIONS:
            new_state, _, _ = step(state, a)
            if new_state != state:
                valid.append(new_state)
        if valid:
            state = random.choice(valid)
    return state

def q_learning_train(episodes=100000, alpha=0.2, gamma=0.95, epsilon=0.3):
    q_table = {}
    for ep in range(episodes):
        state = generate_near_goal_state(GOAL, steps=random.randint(2, 10))
        for _ in range(30):
            st = state_to_tuple(state)
            if st not in q_table:
                q_table[st] = {a: 0.0 for a in ACTIONS}
            action = random.choice(ACTIONS) if random.random() < epsilon else max_q_action(q_table, state)
            next_state, reward, done = step(state, action)
            nst = state_to_tuple(next_state)
            if nst not in q_table:
                q_table[nst] = {a: 0.0 for a in ACTIONS}
            q_table[st][action] += alpha * (reward + gamma * max(q_table[nst].values()) - q_table[st][action])
            state = next_state
            if done: break
    return q_table

def solve(state, q_table):
    path = [deepcopy(state)]
    for _ in range(50):
        if state == GOAL:
            return path
        st = state_to_tuple(state)
        if st not in q_table:
            return None
        action = max_q_action(q_table, state)
        next_state, _, _ = step(state, action)
        if next_state in path:
            return None
        path.append(next_state)
        state = next_state
    return None

# ----------------- GUI ------------------
class PuzzleUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Q-Learning")
        self.master.geometry("850x550") 

        self.q_table = {}
        self.state = generate_near_goal_state(GOAL, 8)
        self.solution = []
        self.index = 0

        self.custom_font = font.Font(family="Montserrat", size=12, weight="bold")

        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack(pady=10)
        
        self.status = tk.Label(master, text="", font=("Montserrat", 15))
        self.status.pack(pady=5)

        btn_frame1 = tk.Frame(master)
        btn_frame1.pack(pady=5)

        btn_frame2 = tk.Frame(master)
        btn_frame2.pack(pady=5)

        tk.Button(btn_frame1, text="Train", command=self.train, font=self.custom_font, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text="Solve", command=self.start_solving, font=self.custom_font, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text="Auto", command=self.auto_run, font=self.custom_font, bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame2, text="Set", command=self.set_manual, font=self.custom_font, bg="#FF9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Random", command=self.set_random_state, font=self.custom_font, bg="#F44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Q-Table", command=self.show_q_table, font=self.custom_font, bg="#607D8B", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        self.draw_board(self.state)

    def draw_board(self, board):
        self.canvas.delete("all")
        size = 100
        padding = 2 
        self.canvas.create_rectangle(padding, padding, size*3 + padding, size*3 + padding, outline="black", width=5)

        for i in range(3):
            for j in range(3):
                val = board[i][j]
                x, y = j * size + padding, i * size + padding
                color = "#D4A98C" if val != 0 else "#E0E0E0"
                outline_color = "#000000" if val != 0 else "#BDBDBD"
                self.canvas.create_rectangle(x+2, y+2, x+size-2, y+size-2, fill=color, outline=outline_color, width=3)
                if val != 0:
                    self.canvas.create_text(x + size//2, y + size//2, text=str(val),
                                            font=("Montserrat", 32, "bold"), fill="white")

    def train(self):
        self.status.config(text="Đang huấn luyện...")
        self.master.update()
        self.q_table = q_learning_train()
        self.status.config(text="Huấn luyện xong!")

    def start_solving(self):
        if not self.q_table:
            messagebox.showwarning("Chưa huấn luyện", "Bạn cần Train trước khi Solve.")
            return
        self.solution = solve(self.state, self.q_table)
        if not self.solution:
            self.status.config(text="Không giải được.")
        else:
            self.status.config(text=f"Đã tìm được lời giải ({len(self.solution)-1} bước)")
            self.index = 0

    def auto_run(self):
        if not self.solution:
            return
        self.index = 0
        self.animate_step()

    def animate_step(self):
        if self.index < len(self.solution):
            self.draw_board(self.solution[self.index])
            self.index += 1
            self.master.after(500, self.animate_step)

    def set_manual(self):
        win = tk.Toplevel(self.master)
        win.title("Nhập trạng thái tùy chỉnh")
        entries = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                entries[i][j] = tk.Entry(win, width=3, font=("Montserrat", 16), justify='center')
                entries[i][j].grid(row=i, column=j, padx=5, pady=5)

        def apply():
            try:
                vals = []
                for row in entries:
                    for e in row:
                        val = int(e.get())
                        vals.append(val)
                if sorted(vals) != list(range(9)):
                    raise ValueError("Phải nhập đủ 0-8")
                state = [vals[i*3:(i+1)*3] for i in range(3)]
                if not is_solvable(state):
                    raise ValueError("Trạng thái không giải được")
                self.state = state
                self.draw_board(state)
                self.status.config(text="Đã đặt trạng thái thủ công")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        tk.Button(win, text="Áp dụng", command=apply, font=("Montserrat", 12)).grid(row=3, column=0, columnspan=3, pady=10)

    def set_random_state(self):
        self.state = generate_near_goal_state(GOAL, steps=random.randint(5, 20))
        self.draw_board(self.state)
        self.status.config(text="Trạng thái đã được tạo ngẫu nhiên")

    def show_q_table(self):
        if not self.q_table:
            messagebox.showinfo("Thông báo", "Bạn cần huấn luyện (Train) trước khi xem Q-Table.")
            return

        q_win = tk.Toplevel(self.master)
        q_win.title("Q-Table")
        q_win.geometry("800x600")

        text = tk.Text(q_win, wrap="none", font=("Courier", 10))
        text.pack(expand=True, fill="both")

        scroll_y = tk.Scrollbar(q_win, orient="vertical", command=text.yview)
        scroll_y.pack(side="right", fill="y")
        text.config(yscrollcommand=scroll_y.set)

        scroll_x = tk.Scrollbar(q_win, orient="horizontal", command=text.xview)
        scroll_x.pack(side="bottom", fill="x")
        text.config(xscrollcommand=scroll_x.set)

        for state, actions in self.q_table.items():
            text.insert("end", f"State: {state}\n")
            for action, q_val in actions.items():
                direction = ["Up", "Down", "Left", "Right"][action]
                text.insert("end", f"  {direction}: {q_val:.2f}\n")
            text.insert("end", "\n")

def base():
    root = tk.Tk()
    app = PuzzleUI(root)
    root.mainloop()

