import tkinter as tk
from tkinter import messagebox, font
import random
import copy
from collections import deque

class PuzzleBoard:
    def __init__(self):
        self.size = 3
        self.state = [[0] * self.size for _ in range(self.size)]
        
    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def generate_random_state(self):
        nums = list(range(9))
        random.shuffle(nums)
        return [nums[i * self.size:(i + 1) * self.size] for i in range(self.size)]
    
    @staticmethod
    def test_state_validity(state):
        flat = [v for row in state for v in row]
        if sorted(flat) != list(range(9)):
            return False
        for i in range(3):
            for j in range(2):
                if state[i][j] != 0 and state[i][j + 1] != 0:
                    if state[i][j + 1] != state[i][j] + 1:
                        return False
        for j in range(3):
            for i in range(2):
                if state[i][j] != 0 and state[i + 1][j] != 0:
                    if state[i + 1][j] != state[i][j] + 3:
                        return False
        return True

class PuzzleSolver:
    def __init__(self):
        self.size = 3
    
    @staticmethod
    def check_constraints(board):
        nums = [board[i][j] for i in range(3) for j in range(3) if board[i][j] is not None]
        if len(nums) != len(set(nums)) or (len(nums) == 9 and sorted(nums) != list(range(9))):
            return False
        for i in range(3):
            for j in range(2):
                left, right = board[i][j], board[i][j + 1]
                if left is not None and right is not None and left != 0 and right != left + 1:
                    return False
        for j in range(3):
            for i in range(2):
                up, down = board[i][j], board[i + 1][j]
                if up is not None and down is not None and up != 0 and down != up + 3:
                    return False
        return True
    
    def ac3_check(self, board, domains):
        arcs = deque()
        for i in range(self.size):
            for j in range(self.size - 1):
                arcs.append(((i, j), (i, j + 1)))
                arcs.append(((i, j + 1), (i, j)))
        for j in range(self.size):
            for i in range(self.size - 1):
                arcs.append(((i, j), (i + 1, j)))
                arcs.append(((i + 1, j), (i, j)))
        
        while arcs:
            (x_i, x_j), (y_i, y_j) = arcs.popleft()
            if self.revise(board, domains, (x_i, x_j), (y_i, y_j)):
                if not domains[x_i][x_j]:
                    return False
                for i in range(self.size):
                    for j in range(self.size):
                        if (i, j) != (y_i, y_j) and ((i, j) == (x_i - 1, x_j) or 
                                                    (i, j) == (x_i + 1, x_j) or 
                                                    (i, j) == (x_i, x_j - 1) or 
                                                    (i, j) == (x_i, x_j + 1)):
                            arcs.append(((i, j), (x_i, x_j)))
        return True
    
    def revise(self, board, domains, xi, xj):
        xi_i, xi_j = xi
        xj_i, xj_j = xj
        revised = False
        
        xj_val = board[xj_i][xj_j]
        if xj_val is not None:
            new_domain = []
            for x in domains[xi_i][xi_j]:
                if xi_j + 1 == xj_j and xj_val == x + 1:
                    new_domain.append(x)
                elif xi_j - 1 == xj_j and xj_val + 1 == x:
                    new_domain.append(x)
                elif xi_i + 1 == xj_i and xj_val == x + 3:
                    new_domain.append(x)
                elif xi_i - 1 == xj_i and xj_val + 3 == x:
                    new_domain.append(x)
                elif xi_i == xj_i and abs(xi_j - xj_j) > 1 or xi_j == xj_j and abs(xi_i - xj_i) > 1:
                    new_domain.append(x)
            if len(new_domain) < len(domains[xi_i][xi_j]):
                domains[xi_i][xi_j] = new_domain
                revised = True
        else:
            new_domain = []
            for x in domains[xi_i][xi_j]:
                valid = False
                for y in domains[xj_i][xj_j]:
                    if xi_j + 1 == xj_j and y == x + 1:
                        valid = True
                    elif xi_j - 1 == xj_j and y + 1 == x:
                        valid = True
                    elif xi_i + 1 == xj_i and y == x + 3:
                        valid = True
                    elif xi_i - 1 == xj_i and y + 3 == x:
                        valid = True
                    elif xi_i == xj_i and abs(xi_j - xj_j) > 1 or xi_j == xj_j and abs(xi_i - xj_i) > 1:
                        valid = True
                if valid:
                    new_domain.append(x)
            if len(new_domain) < len(domains[xi_i][xi_j]):
                domains[xi_i][xi_j] = new_domain
                revised = True
                
        return revised
    
    def backtracking(self, pos=0, board=None, steps=None, use_ac3=False):
        if board is None:
            board = [[None] * self.size for _ in range(self.size)]
        if steps is None:
            steps = []
            
        if pos == 9:
            if self.check_constraints(board):
                steps.append([row[:] for row in board])
                return True
            return False
            
        row, col = divmod(pos, self.size)
        
        domains = [[list(range(9)) for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] is not None:
                    domains[i][j] = [board[i][j]]
                else:
                    used = {board[k][l] for k in range(self.size) for l in range(self.size) if board[k][l] is not None}
                    domains[i][j] = [n for n in range(9) if n not in used]
        
        if use_ac3 and not self.ac3_check(board, domains):
            return False
            
        nums = random.sample(domains[row][col], len(domains[row][col]))
            
        for num in nums:
            board[row][col] = num
            if self.check_constraints(board):
                steps.append([row[:] for row in board])
                new_domains = [[domains[i][j].copy() for j in range(self.size)] for i in range(self.size)]
                new_domains[row][col] = [num]
                if not use_ac3 or self.ac3_check(board, new_domains):
                    if self.backtracking(pos + 1, board, steps, use_ac3):
                        return True
            board[row][col] = None
            steps.append([row[:] for row in board])
            
        return False

class PuzzleUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Generator")
        self.master.geometry("600x650")
        self.master.resizable(False, False)
        self.master.configure(bg='white')  
        
        self.board = PuzzleBoard()
        self.solver = PuzzleSolver()
        
        self.custom_font = font.Font(family="Montserrat", size=12)
        self.title_font = font.Font(family="Montserrat", size=14, weight="bold")
        self.big_font = font.Font(family="Montserrat", size=40, weight="bold")
        self.small_none_font = font.Font(family="Montserrat", size=20, slant="italic")
        
        self.history = []
        self.current_step = -1
        self.auto_running = False
        self.try_count = 0
        self.max_tries = 10000
        self.max_history = 1000
        self.after_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.canvas = tk.Canvas(self.master, width=300, height=300, bg='white', 
                              highlightthickness=2, highlightbackground="black")
        self.canvas.pack(pady=10)
        
        self.status_label = tk.Label(self.master, text="Nhấn Play để bắt đầu tạo trạng thái", 
                                   font=self.title_font, bg='white', fg='black')
        self.status_label.pack(pady=5)
        
        self.try_label = tk.Label(self.master, text="Lượt thử: 0", font=self.custom_font, 
                                 bg='white', fg='black')
        self.try_label.pack()
        
        self.init_buttons()
        self.draw_board(self.board.get_state())
        
    def init_buttons(self):
        btn_frame = tk.Frame(self.master, bg='white')
        btn_frame.pack(pady=10)
        
        self.btn_play = tk.Button(btn_frame, text="Play", width=8, command=self.play, 
                                bg="#4CAF50", fg="white", font=self.custom_font)
        self.btn_play.grid(row=0, column=0, padx=5)
        
        self.btn_pause = tk.Button(btn_frame, text="Pause", width=8, command=self.pause, 
                                 bg="#F44336", fg="white", font=self.custom_font)
        self.btn_pause.grid(row=0, column=1, padx=5)
        self.btn_pause.config(state=tk.DISABLED)
        
        self.btn_prev = tk.Button(btn_frame, text="Prev", width=8, command=self.prev_step, 
                                font=self.custom_font)
        self.btn_prev.grid(row=0, column=2, padx=5)
        self.btn_prev.config(state=tk.DISABLED)
        
        self.btn_next = tk.Button(btn_frame, text="Next", width=8, command=self.next_step, 
                                font=self.custom_font)
        self.btn_next.grid(row=0, column=3, padx=5)
        self.btn_next.config(state=tk.DISABLED)
        
        self.btn_pause_solver = tk.Button(btn_frame, text="Pause Solver", width=12, command=self.pause_solver, 
                                        bg="#FF9800", fg="white", font=self.custom_font)
        self.btn_pause_solver.grid(row=0, column=4, padx=5)
        self.btn_pause_solver.config(state=tk.DISABLED)
        
        self.btn_reset = tk.Button(self.master, text="Reset", width=20, command=self.reset_board, 
                                 font=self.custom_font)
        self.btn_reset.pack(pady=5)
        
        self.btn_backtrack = tk.Button(self.master, text="Backtracking", width=20, 
                                     command=self.solve_with_backtracking, font=self.custom_font, 
                                     bg="#3F51B5", fg="white")
        self.btn_backtrack.pack(pady=5)
        
        self.btn_bt_ac3 = tk.Button(self.master, text="Backtracking + AC-3", width=20, 
                                  command=self.solve_with_bt_ac3, font=self.custom_font, 
                                  bg="#009688", fg="white")
        self.btn_bt_ac3.pack(pady=5)
        
    def draw_board(self, board):
        self.canvas.delete("all")
        size = 100
        for i in range(3):
            for j in range(3):
                val = board[i][j]
                x0, y0 = j * size, i * size
                x1, y1 = x0 + size, y0 + size
                color = "#D4A98C" if val not in (0, None) else "#E0E0E0"
                self.canvas.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2, fill=color, 
                                          outline="black", width=3)
                if val is not None and val != 0:
                    self.canvas.create_text(x0 + size // 2, y0 + size // 2, text=str(val), 
                                         font=self.big_font, fill="white")
                elif val is None:
                    self.canvas.create_text(x0 + size // 2, y0 + size // 2, text="None", 
                                         font=self.small_none_font, fill="#888888")

    def auto_random_step(self):
        if not self.auto_running:
            self.status_label.config(text="Đã dừng.")
            self.btn_play.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)
            return

        if self.try_count >= self.max_tries:
            self.status_label.config(text="Không tìm được trạng thái hợp lệ!")
            messagebox.showwarning("Thông báo", "Không tìm được trạng thái hợp lệ!")
            self.auto_running = False
            self.btn_play.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)
            self.try_count = 0
            self.update_button_states()
            return

        new_state = self.board.generate_random_state()
        self.board.set_state(new_state)
        self.draw_board(new_state)

        if len(self.history) >= self.max_history:
            self.history.pop(0)
        self.history.append(copy.deepcopy(new_state))
        self.current_step = len(self.history) - 1
        self.try_count += 1
        self.try_label.config(text=f"Lượt thử: {self.try_count}")

        if self.board.test_state_validity(new_state):
            self.status_label.config(text="Tìm được trạng thái hợp lệ!")
            self.auto_running = False
            self.btn_play.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)
            self.try_count = 0
            self.update_button_states()
            messagebox.showinfo("Thành công", "Đã tạo trạng thái hợp lệ!")
        else:
            self.after_id = self.master.after(10, self.auto_random_step)

    def play(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.auto_running = True
        self.history = []  
        self.current_step = -1
        self.btn_play.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        self.status_label.config(text="Đang tạo trạng thái...")
        self.auto_random_step()

    def pause(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.auto_running = False
        self.btn_play.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.status_label.config(text="Tạm dừng.")
        self.update_button_states()

    def pause_solver(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.btn_pause_solver.config(state=tk.DISABLED)
        self.btn_play.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.status_label.config(text="Tạm dừng thuật toán.")
        self.update_button_states()

    def update_button_states(self):
        """Cập nhật trạng thái"""
        if not self.history:
            self.btn_prev.config(state=tk.DISABLED)
            self.btn_next.config(state=tk.DISABLED)
        else:
            self.btn_prev.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
            self.btn_next.config(state=tk.NORMAL if self.current_step < len(self.history) - 1 else tk.DISABLED)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.board.set_state(self.history[self.current_step])
            self.draw_board(self.board.get_state())
            self.status_label.config(text=f"Trạng thái {self.current_step + 1}/{len(self.history)}")
            self.update_button_states()

    def next_step(self):
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.board.set_state(self.history[self.current_step])
            self.draw_board(self.board.get_state())
            self.status_label.config(text=f"Trạng thái {self.current_step + 1}/{len(self.history)}")
            self.update_button_states()

    def solve_with_backtracking(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.status_label.config(text="Đang tìm trạng thái bằng Backtracking...")
        self.master.update()

        self.backtrack_steps = []
        success = self.solver.backtracking(0, None, self.backtrack_steps, use_ac3=False)

        if not success:
            self.status_label.config(text="Không tìm thấy trạng thái hợp lệ!")
            messagebox.showwarning("Thông báo", "Không tìm thấy trạng thái hợp lệ bằng Backtracking.")
            self.update_button_states()
            return

        self.status_label.config(text="Đang hiển thị quá trình tìm bằng Backtracking...")
        self.try_label.config(text=f"Số bước thử: {len(self.backtrack_steps)}")
        self.history = self.backtrack_steps 
        self.current_step = 0
        self.btn_pause_solver.config(state=tk.NORMAL)

        def animate_step():
            if self.current_step < len(self.history):
                self.board.set_state(self.history[self.current_step])
                self.draw_board(self.board.get_state())
                self.status_label.config(text=f"Trạng thái {self.current_step + 1}/{len(self.history)}")
                self.current_step += 1
                self.update_button_states()
                self.after_id = self.master.after(120, animate_step)
            else:
                self.status_label.config(text="Tìm thấy trạng thái hợp lệ bằng Backtracking.")
                self.btn_prev.config(state=tk.NORMAL)
                self.btn_next.config(state=tk.DISABLED)
                self.btn_pause_solver.config(state=tk.DISABLED)
                self.after_id = None

        animate_step()

    def solve_with_bt_ac3(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.status_label.config(text="Đang tìm trạng thái bằng Backtracking + AC-3...")
        self.master.update()

        self.btac3_steps = []
        success = self.solver.backtracking(0, None, self.btac3_steps, use_ac3=True)

        if not success:
            self.status_label.config(text="Không tìm thấy trạng thái hợp lệ!")
            messagebox.showwarning("Thông báo", "Không tìm thấy trạng thái hợp lệ bằng Backtracking + AC-3.")
            self.update_button_states()
            return

        self.status_label.config(text="Đang hiển thị quá trình tìm bằng Backtracking + AC-3...")
        self.try_label.config(text=f"Số bước thử: {len(self.btac3_steps)}")
        self.history = self.btac3_steps  
        self.current_step = 0
        self.btn_pause_solver.config(state=tk.NORMAL)

        def animate_step():
            if self.current_step < len(self.history):
                self.board.set_state(self.history[self.current_step])
                self.draw_board(self.board.get_state())
                self.status_label.config(text=f"Trạng thái {self.current_step + 1}/{len(self.history)}")
                self.current_step += 1
                self.update_button_states()
                self.after_id = self.master.after(120, animate_step)
            else:
                self.status_label.config(text="Tìm thấy trạng thái hợp lệ bằng Backtracking + AC-3.")
                self.btn_prev.config(state=tk.NORMAL)
                self.btn_next.config(state=tk.DISABLED)
                self.btn_pause_solver.config(state=tk.DISABLED)
                self.after_id = None

        animate_step()

    def reset_board(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.board.set_state([[0] * 3 for _ in range(3)])
        self.history = []
        self.current_step = -1
        self.try_count = 0
        self.try_label.config(text="Lượt thử: 0")
        self.status_label.config(text="Đã reset puzzle.")
        self.draw_board(self.board.get_state())
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        self.btn_play.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_pause_solver.config(state=tk.DISABLED)

def base():
    root = tk.Tk()
    app = PuzzleUI(root)
    root.mainloop()
