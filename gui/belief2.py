import tkinter as tk
import random
import time
from collections import deque
from algorithms import *

class EightPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1000x700")
        self.root.minsize(1000, 700)  

        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # Configure column weights to make them exactly equal
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)

        # Left scrollable canvas for input and controls - with fixed width
        left_container = tk.Frame(main_container, width=500)  
        left_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_container.grid_propagate(False)  

        canvas_frame = tk.Frame(left_container)
        canvas_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_frame)
        y_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        x_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Layout scrollbars and canvas
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        
        self.root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.root.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.result_frame = tk.LabelFrame(main_container, text="Solution Viewer", padx=10, pady=10, width=500)
        self.result_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.result_frame.grid_propagate(False)  

        self.mode = tk.StringVar(value="Non-Observe")
        self.initial_states = []
        self.goal_states = []
        self.partial_goal = None
        self.matching_goals = []
        self.solutions = []
        self.exec_time = None
        self.entries = {}
        self.current_solution_index = 0
        self.current_step = 0
        self.is_playing = False
        self.animation_task = None

        self.create_widgets()
        self.update_mode()

    def create_widgets(self):
        try:
            self.root.option_add("*Font", "Montserrat 10")
        except tk.TclError:
            print("Font Montserrat not found, using default font.")

        # Mode selection
        mode_frame = tk.LabelFrame(self.scrollable_frame, text="Select Mode", padx=15, pady=15)
        mode_frame.pack(pady=10, padx=20, fill="x")
        tk.Radiobutton(mode_frame, text="Non-Observe", variable=self.mode, value="Non-Observe", 
                       command=self.update_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(mode_frame, text="Partial Observe", variable=self.mode, value="Partial Observe", 
                       command=self.update_mode).grid(row=0, column=1, padx=10)

        self.initial_frame = tk.LabelFrame(self.scrollable_frame, text="Initial States", padx=15, pady=15)
        self.initial_frame.pack(pady=10, padx=20, fill="x")
        self.goal_frame = tk.LabelFrame(self.scrollable_frame, text="Goal States", padx=15, pady=15)
        self.goal_frame.pack(pady=10, padx=20, fill="x")

        control_frame = tk.Frame(self.scrollable_frame)
        control_frame.pack(pady=10, padx=20, fill="x")
        tk.Button(control_frame, text="Randomize", command=self.randomize_states, 
                  bg="#2196F3", fg="black", activebackground="#0b7dda", 
                  font=("Montserrat", 10)).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Set Manually", command=self.set_manually_from_entries, 
                  bg="#9C27B0", fg="black", activebackground="#7B1FA2", 
                  font=("Montserrat", 10)).grid(row=0, column=1, padx=5)

        self.input_frame = tk.LabelFrame(self.scrollable_frame, text="Manual Input", padx=15, pady=15)
        self.input_frame.pack(pady=10, padx=20, fill="x")
        self.create_input_entries()

        algo_frame = tk.LabelFrame(self.scrollable_frame, text="Select Algorithm", padx=15, pady=15)
        algo_frame.pack(pady=10, padx=20, fill="x")
        self.selected_algo = tk.StringVar(value="BFS")
        algorithm_groups = {
            "# Uninformed": ["BFS", "DFS", "UCS", "IDS"],
            "# Informed": ["GDS", "A*", "IDAS"],
            "# Local": ["SHC", "SAHC", "Stochastic", "SA", "BS", "GEN", "ANDOR"]
        }
        row = 0
        for group_name, algos in algorithm_groups.items():
            tk.Label(algo_frame, text=group_name, font=("Montserrat", 10)).grid(row=row, column=0, sticky="w", pady=(5, 2))
            row += 1
            for j, algo in enumerate(algos):
                tk.Radiobutton(algo_frame, text=algo, variable=self.selected_algo, value=algo).grid(row=row, column=j, padx=5, pady=2)
            row += 1

        tk.Button(self.scrollable_frame, text="Run", command=self.run_algorithm, 
                  bg="#F44336", fg="black", activebackground="#d32f2f", 
                  font=("Montserrat", 10)).pack(pady=10, padx=20)
        self.result_label = tk.Label(self.scrollable_frame, text="", font=("Montserrat", 12), wraplength=600)
        self.result_label.pack(pady=10, padx=20, fill="x")

        # Solution viewer controls - enhanced for better visibility
        control_frame = tk.Frame(self.result_frame)
        control_frame.pack(pady=5, fill="x")
        
        # Center the controls
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(6, weight=1)
        
        button_frame = tk.Frame(control_frame)
        button_frame.grid(row=0, column=1, columnspan=4)
        
        tk.Button(button_frame, text="Start", command=self.start_animation, 
                  bg="#4CAF50", fg="black", activebackground="#45a049", 
                  font=("Montserrat", 10)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Prev", command=self.prev_step, 
                  bg="#009688", fg="black", activebackground="#00796B", 
                  font=("Montserrat", 10)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Play", command=self.play_animation, 
                  bg="#4CAF50", fg="black", activebackground="#45a049", 
                  font=("Montserrat", 10)).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Pause", command=self.pause_animation, 
                  bg="#FF9800", fg="black", activebackground="#F57C00", 
                  font=("Montserrat", 10)).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Next", command=self.next_step, 
                  bg="#2196F3", fg="black", activebackground="#0b7dda", 
                  font=("Montserrat", 10)).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Next Solution", command=self.next_solution, 
                  bg="#9C27B0", fg="black", activebackground="#7B1FA2", 
                  font=("Montserrat", 10)).grid(row=0, column=5, padx=5)

        # Make the canvas larger to better utilize the right panel space
        self.result_canvas = tk.Canvas(self.result_frame, width=320, height=320, bg="#FFFFFF", highlightthickness=2, highlightbackground="#aaa")
        self.result_canvas.pack(pady=20, expand=True)
        self.step_label = tk.Label(self.result_frame, text="Step: 0 / 0", font=("Montserrat", 12))
        self.step_label.pack(pady=10)

    def create_input_entries(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        layout_frame = tk.Frame(self.input_frame)
        layout_frame.pack(fill="x")
        if self.mode.get() == "Non-Observe":
            entry_canvas = tk.Frame(layout_frame)
            entry_canvas.pack(fill="x")
            
            for i in range(5):
                frame = tk.Frame(entry_canvas)
                frame.grid(row=0, column=i, padx=10)
                tk.Label(frame, text=f"State {i+1}:", font=("Montserrat", 10)).grid(row=0, column=0, columnspan=3)
                for j in range(3):
                    for k in range(3):
                        entry = tk.Entry(frame, width=3)
                        entry.grid(row=j+1, column=k, padx=2, pady=2)
                        self.entries[(i, j, k)] = entry
        else:
            # Create a canvas for horizontally scrollable entries if needed
            entry_canvas = tk.Frame(layout_frame)
            entry_canvas.pack(fill="x")
            
            for i in range(3):
                frame = tk.Frame(entry_canvas)
                frame.grid(row=0, column=i, padx=10)
                tk.Label(frame, text=f"State {i+1}:", font=("Montserrat", 10)).grid(row=0, column=0, columnspan=3)
                for j in range(3):
                    for k in range(3):
                        entry = tk.Entry(frame, width=3)
                        entry.grid(row=j+1, column=k, padx=2, pady=2)
                        self.entries[(i, j, k)] = entry
            for k in range(3):
                self.entries[(2, 1, k)].config(state="disabled")
                self.entries[(2, 2, k)].config(state="disabled")
                self.entries[(2, 1, k)].delete(0, tk.END)
                self.entries[(2, 2, k)].delete(0, tk.END)
                self.entries[(2, 1, k)].insert(0, "0")
                self.entries[(2, 2, k)].insert(0, "0")
            self.entries[(2, 0, 0)].insert(0, "1")
            self.entries[(2, 0, 1)].insert(0, "2")
            self.entries[(2, 0, 2)].insert(0, "3")
            self.entries[(2, 0, 0)].config(state="disabled")
            self.entries[(2, 0, 1)].config(state="disabled")
            self.entries[(2, 0, 2)].config(state="disabled")

    def update_mode(self):
        for widget in self.initial_frame.winfo_children():
            widget.destroy()
        for widget in self.goal_frame.winfo_children():
            widget.destroy()
        self.initial_canvases = []
        self.goal_canvases = []

        initial_container = tk.Frame(self.initial_frame)
        initial_container.pack(fill="x")
        
        goal_container = tk.Frame(self.goal_frame)
        goal_container.pack(fill="x")

        if self.mode.get() == "Non-Observe":
            self.initial_frame.config(text="Initial States (3 Puzzles)")
            for i in range(3):
                canvas = tk.Canvas(initial_container, width=120, height=120, bg="#ffffff", highlightthickness=3, highlightbackground="#ccc")
                canvas.grid(row=0, column=i, padx=10, pady=5)
                self.initial_canvases.append(canvas)
            self.goal_frame.config(text="Goal States (2 Puzzles)")
            for i in range(2):
                canvas = tk.Canvas(goal_container, width=120, height=120, bg="#ffffff", highlightthickness=3, highlightbackground="#ccc")
                canvas.grid(row=0, column=i, padx=10, pady=5)
                self.goal_canvases.append(canvas)
        else:
            self.initial_frame.config(text="Initial States (2 Puzzles)")
            for i in range(2):
                canvas = tk.Canvas(initial_container, width=120, height=120, bg="#ffffff", highlightthickness=3, highlightbackground="#ccc")
                canvas.grid(row=0, column=i, padx=10, pady=5)
                self.initial_canvases.append(canvas)
            self.goal_frame.config(text="Partial Goal State")
            canvas = tk.Canvas(goal_container, width=120, height=120, bg="#ffffff", highlightthickness=3, highlightbackground="#ccc")
            canvas.grid(row=0, column=0, padx=10, pady=5)
            self.goal_canvases.append(canvas)

        self.create_input_entries()
        self.randomize_states()

    def draw_state(self, canvas, state, partial=False):
        canvas.delete("all")
        if canvas == self.result_canvas:
            canvas_width = canvas.winfo_width() or 320
            canvas_height = canvas.winfo_height() or 320
            tile_size = min(canvas_width, canvas_height) // 3
        else:
            tile_size = 40
        offset = 0
        for i in range(3):
            for j in range(3):
                x1 = j * tile_size + offset
                y1 = i * tile_size + offset
                x2 = x1 + tile_size
                y2 = y1 + tile_size
                if partial and i > 0:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="#DDFF9D", outline="#666")
                elif state[i][j] == 0:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="#666")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="#ffe7be", outline="#666")
                    canvas.create_text(x1 + tile_size/2, y1 + tile_size/2, text=str(state[i][j]), font=("Montserrat", 20 if canvas == self.result_canvas else 15))
                canvas.create_rectangle(x1, y1, x2, y2, outline="#666")

    def randomize_states(self):
        if self.mode.get() == "Non-Observe":
            self.initial_states = []
            for _ in range(3):
                numbers = list(range(9))
                random.shuffle(numbers)
                state = [numbers[:3], numbers[3:6], numbers[6:]]
                self.initial_states.append(state)
            for i in range(len(self.initial_states)):
                self.draw_state(self.initial_canvases[i], self.initial_states[i])

            self.goal_states = []
            for _ in range(2):
                numbers = list(range(9))
                random.shuffle(numbers)
                state = [numbers[:3], numbers[3:6], numbers[6:]]
                self.goal_states.append(state)
            for i in range(len(self.goal_states)):
                self.draw_state(self.goal_canvases[i], self.goal_states[i])
        else:
            self.initial_states = []
            for _ in range(2):
                numbers = list(range(9))
                random.shuffle(numbers)
                state = [numbers[:3], numbers[3:6], numbers[6:]]
                self.initial_states.append(state)
            for i in range(len(self.initial_states)):
                self.draw_state(self.initial_canvases[i], self.initial_states[i])

            self.partial_goal = [[1, 2, 3], [0, 0, 0], [0, 0, 0]]
            self.draw_state(self.goal_canvases[0], self.partial_goal, partial=True)

    def set_manually_from_entries(self):
        try:
            if self.mode.get() == "Non-Observe":
                self.initial_states = []
                self.goal_states = []
                for i in range(5):
                    state = []
                    for j in range(3):
                        row = [int(self.entries[(i, j, k)].get() or 0) for k in range(3)]
                        state.append(row)
                    if i < 3:
                        self.initial_states.append(state)
                    else:
                        self.goal_states.append(state)
                for state in self.initial_states + self.goal_states:
                    flat = sum(state, [])
                    if sorted(flat) != list(range(9)):
                        raise ValueError("Each state must contain numbers 0-8 exactly once")
                for i in range(len(self.initial_states)):
                    self.draw_state(self.initial_canvases[i], self.initial_states[i])
                for i in range(len(self.goal_states)):
                    self.draw_state(self.goal_canvases[i], self.goal_states[i])
            else:
                self.initial_states = []
                for i in range(2):
                    state = []
                    for j in range(3):
                        row = [int(self.entries[(i, j, k)].get() or 0) for k in range(3)]
                        state.append(row)
                    self.initial_states.append(state)
                self.partial_goal = []
                for j in range(3):
                    row = [int(self.entries[(2, j, k)].get() or 0) for k in range(3)]
                    self.partial_goal.append(row)
                for state in self.initial_states:
                    flat = sum(state, [])
                    if sorted(flat) != list(range(9)):
                        raise ValueError("Each state must contain numbers 0-8 exactly once")
                if self.partial_goal[0] != [1, 2, 3] or any(x != 0 for row in self.partial_goal[1:] for x in row):
                    raise ValueError("Partial goal must have first row [1, 2, 3] and rest zeros")
                for i in range(len(self.initial_states)):
                    self.draw_state(self.initial_canvases[i], self.initial_states[i])
                self.draw_state(self.goal_canvases[0], self.partial_goal, partial=True)
            self.result_label.config(text="States set successfully!")
        except ValueError as e:
            self.result_label.config(text=f"Error: {str(e)}")
        except Exception as e:
            self.result_label.config(text=f"Invalid input: {str(e)}")

    def run_algorithm(self):
        start_time = time.time()
        self.solutions = []
        algo_map = {
            "BFS": BFS, "DFS": DFS, "UCS": UCS, "IDS": IDS,
            "GDS": GDS, "A*": ASTAR, "IDAS": IDAS,
            "SHC": SHC, "SAHC": SAHC, "Stochastic": Stochastic,
            "SA": SA, "BS": BS, "GEN": GEN, "ANDOR": ANDOR
        }
        algo = algo_map.get(self.selected_algo.get())
        if not algo:
            self.result_label.config(text="Unknown algorithm selected.")
            return

        if self.mode.get() == "Non-Observe":
            for init in self.initial_states:
                for goal in self.goal_states:
                    result = algo(init, goal)
                    self.solutions.append((init, goal, result))
        else:
            self.matching_goals = []
            self.goal_canvases.clear()
            remaining = [0, 4, 5, 6, 7, 8]
            candidates = []
            for _ in range(4):
                random.shuffle(remaining)
                g = [[1, 2, 3], remaining[:3], remaining[3:]]
                candidates.append(g)
            for init in self.initial_states:
                for goal in candidates:
                    result = algo(init, goal)
                    if result and goal[0] == self.partial_goal[0]:
                        self.matching_goals.append(goal)
                        self.solutions.append((init, goal, result))
            for widget in self.goal_frame.winfo_children():
                widget.destroy()
            for i, goal in enumerate(self.matching_goals):
                canvas = tk.Canvas(self.goal_frame, width=120, height=120, bg="#ffffff", highlightthickness=2, highlightbackground="#ccc")
                canvas.grid(row=0, column=i, padx=10, pady=5)
                self.draw_state(canvas, goal)
                self.goal_canvases.append(canvas)

        self.exec_time = time.time() - start_time
        self.result_label.config(text=f"Execution Time: {self.exec_time:.2f}s Solutions Computed: {len(self.solutions)}")
        self.current_solution_index = 0
        self.current_step = 0
        self.update_solution_display()

    def update_solution_display(self):
        if not self.solutions:
            self.result_canvas.delete("all")
            self.result_canvas.create_text(160, 160, text="No Solutions", fill="red", font=("Montserrat", 15))
            self.step_label.config(text="Step: 0 / 0")
            return

        init, goal, path = self.solutions[self.current_solution_index]
        if not path:
            self.result_canvas.delete("all")
            self.result_canvas.create_text(160, 160, text="No Solution", fill="red", font=("Montserrat", 15))
            self.step_label.config(text="Step: 0 / 0")
            return

        path = [p["state"] if isinstance(p, dict) else p for p in path]
        self.current_step = min(self.current_step, len(path) - 1)
        self.draw_state(self.result_canvas, path[self.current_step])
        self.step_label.config(text=f"Step: {self.current_step + 1} / {len(path)}")

    def start_animation(self):
        self.current_step = 0
        self.pause_animation()
        self.update_solution_display()

    def play_animation(self):
        if not self.solutions or self.is_playing:
            return
        self.is_playing = True
        self.animate()

    def pause_animation(self):
        self.is_playing = False
        if self.animation_task:
            self.root.after_cancel(self.animation_task)
            self.animation_task = None

    def next_step(self):
        if not self.solutions:
            return
        init, goal, path = self.solutions[self.current_solution_index]
        if not path:
            return
        path = [p["state"] if isinstance(p, dict) else p for p in path]
        if self.current_step < len(path) - 1:
            self.current_step += 1
            self.update_solution_display()

    def prev_step(self):
        if not self.solutions:
            return
        if self.current_step > 0:
            self.current_step -= 1
            self.update_solution_display()

    def next_solution(self):
        if not self.solutions:
            return
        self.current_solution_index = (self.current_solution_index + 1) % len(self.solutions)
        self.current_step = 0
        self.pause_animation()
        self.update_solution_display()

    def animate(self):
        if not self.is_playing or not self.solutions:
            return
        init, goal, path = self.solutions[self.current_solution_index]
        if not path:
            self.pause_animation()
            return
        path = [p["state"] if isinstance(p, dict) else p for p in path]
        if self.current_step < len(path) - 1:
            self.current_step += 1
            self.update_solution_display()
            self.animation_task = self.root.after(500, self.animate)
        else:
            self.pause_animation()

def base():
    root = tk.Tk()
    app = EightPuzzleApp(root)
    root.mainloop()