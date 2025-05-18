import pygame as pg
from assets.color import *
import random

cell = 80

class Puzzle:
    def __init__(self, screen, x_offset, title = None):
        self.screen = screen
        self.x_offset = x_offset
        self.title = title
        self.state = [[None for _ in range(3)] for _ in range(3)]
        self.font = pg.font.SysFont('Montserrat', 30, bold=True)
        self.title_font = pg.font.SysFont('Montserrat', 30, bold=True)
        
        self.solution = []          # List các trạng thái 
        self.current_step = 0       # Bước hiện tại trong solution
        self.is_playing = False     # Trạng thái đang play
        self.play_speed = 10         # số frames mỗi bước (để delay)

        self.frame_count = 0

    def draw(self, highlight=None):
        base_y = 60  

        outer_rect = pg.Rect(self.x_offset - 10, base_y - 10, cell * 3 + 20, cell * 3 + 20)
        pg.draw.rect(self.screen, white, outer_rect)

        inner_border = 4
        inner_rect = pg.Rect(
            self.x_offset - inner_border,
            base_y - inner_border,
            cell * 3 + inner_border * 2,
            cell * 3 + inner_border * 2
        )
        pg.draw.rect(self.screen, blue, inner_rect, 2)

        if self.title:
            title_text = self.title_font.render(self.title, True, white)
            title_rect = title_text.get_rect(center=(self.x_offset + (cell * 3) // 2, base_y - 30))
            self.screen.blit(title_text, title_rect)

        for i in range(3):
            for j in range(3):
                x = j * cell + self.x_offset
                y = i * cell + base_y
                rect = pg.Rect(x, y, cell, cell)

                pg.draw.rect(self.screen, beige, rect)
                pg.draw.rect(self.screen, white, rect, 4)

                if highlight and highlight == (i, j):
                    pg.draw.rect(self.screen, blue, rect, 6)

                value = self.state[i][j]
                if value not in (None, 0):
                    text = self.font.render(str(value), True, ebony)
                    text_rect = text.get_rect(center=(x + cell // 2, y + cell // 2))
                    self.screen.blit(text, text_rect)

    def handle_click(self, x, y, puzzle_nums):
        if self.x_offset <= x < self.x_offset + cell * 3 and 80 <= y < 80 + cell * 3:
            row = (y - 80) // cell
            col = (x - self.x_offset) // cell

            if self.state[row][col] is None:
                num = len(puzzle_nums) + 1
                if num == 9:
                    num = 0
                if num not in puzzle_nums:
                    self.state[row][col] = num
                    puzzle_nums.add(num)
                    return True 
        return False
    
    def draw_with_move_highlight(self, highlight=None):
        base_y = 60  

        outer_rect = pg.Rect(self.x_offset - 10, base_y - 10, cell * 3 + 20, cell * 3 + 20)
        pg.draw.rect(self.screen, white, outer_rect)

        inner_border = 4
        inner_rect = pg.Rect(
            self.x_offset - inner_border,
            base_y - inner_border,
            cell * 3 + inner_border * 2,
            cell * 3 + inner_border * 2
        )
        pg.draw.rect(self.screen, blue, inner_rect, 2)

        if self.title:
            title_text = self.title_font.render(self.title, True, white)
            title_rect = title_text.get_rect(center=(self.x_offset + (cell * 3) // 2, base_y - 30))
            self.screen.blit(title_text, title_rect)

        for i in range(3):
            for j in range(3):
                x = j * cell + self.x_offset
                y = i * cell + base_y
                rect = pg.Rect(x, y, cell, cell)

                # Nền ô
                pg.draw.rect(self.screen, beige, rect)

                value = self.state[i][j]

                # Nếu ô là 0 (ô trống) tô màu nền khác (xanh lá)
                if value == 0:
                    pg.draw.rect(self.screen, (0, 200, 0), rect)  # green
                else:
                    # Vẽ viền đỏ nếu highlight trùng ô này (đang di chuyển)
                    if highlight and highlight == (i, j):
                        pg.draw.rect(self.screen, (255, 0, 0), rect, 6)  # đỏ dày
                    else:
                        # Viền trắng mặc định
                        pg.draw.rect(self.screen, white, rect, 4)

                # Vẽ số nếu không phải ô trống hoặc None
                if value not in (None, 0):
                    text = self.font.render(str(value), True, ebony)
                    text_rect = text.get_rect(center=(x + cell // 2, y + cell // 2))
                    self.screen.blit(text, text_rect)

    def set_solution(self, solution):
        self.solution = solution
        self.current_step = 0
        if solution:
            self.state = [row[:] for row in solution[0]]
        self.is_playing = False
        self.frame_count = 0

    def next_step(self):
        if self.solution and self.current_step < len(self.solution) - 1:
            self.current_step += 1
            self.state = [row[:] for row in self.solution[self.current_step]]

    def prev_step(self):
        if self.solution and self.current_step > 0:
            self.current_step -= 1
            self.state = [row[:] for row in self.solution[self.current_step]]

    def restart(self):
        if self.solution:
            self.current_step = 0
            self.state = [row[:] for row in self.solution[0]]
            self.is_playing = False
            self.frame_count = 0
            
    def reset(self):
        self.state = [[None for _ in range(3)] for _ in range(3)]
        self.solution = []
        self.current_step = 0
        self.is_playing = False
        def play(self):
            if self.solution:
                self.is_playing = True

    def play(self):
        self.is_playing = True
        
    def pause(self):
        self.is_playing = False

    def update(self):
        if self.is_playing and self.solution:
            self.frame_count += 1
            if self.frame_count >= self.play_speed:
                self.next_step()
                self.frame_count = 0
                # Nếu đã chạy đến cuối thì pause
                if self.current_step == len(self.solution) - 1:
                    self.pause()
                    
def input_states(ipuzzle, gpuzzle):
    ipuzzle_nums = set()
    gpuzzle_nums = set()
    running = True

    while running:
        ipuzzle.draw()
        gpuzzle.draw()
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if len(ipuzzle_nums) < 9:
                    ipuzzle.handle_click(x, y, ipuzzle_nums)
                elif len(gpuzzle_nums) < 9:
                    gpuzzle.handle_click(x, y, gpuzzle_nums)

                if len(ipuzzle_nums) == 9 and len(gpuzzle_nums) == 9:
                    running = False

    return ipuzzle.state, gpuzzle.state

class BPuzzle:
    def __init__(self, screen, x_offset, y_offset = None, title = None):
        self.screen = screen
        self.x_offset = x_offset
        self.title = title
        self.state = self.generate_random_state()
        self.font = pg.font.SysFont('Montserrat', 30, bold=True)
        self.title_font = pg.font.SysFont('Montserrat', 30, bold=True)  
        
        self.y_offset = y_offset if y_offset is not None else 70
    
    def generate_random_state(self):
        numbers = list(range(1, 9)) + [0] 
        random.shuffle(numbers)
        return [numbers[i:i+3] for i in range(0, len(numbers), 3)]
    
    def draw(self, highlight=None):
        outer_rect = pg.Rect(self.x_offset - 10, self.y_offset, cell * 3 + 20, cell * 3 + 20)
        pg.draw.rect(self.screen, white, outer_rect)

        inner_border = 4
        inner_rect = pg.Rect(
            self.x_offset - inner_border, 
            self.y_offset + (10 - inner_border), 
            cell * 3 + inner_border * 2, 
            cell * 3 + inner_border * 2
        )
        pg.draw.rect(self.screen, blue, inner_rect, 2)

        if self.title:
            title_text = self.title_font.render(self.title, True, white)
            title_rect = title_text.get_rect(center=(self.x_offset + (cell * 3) // 2, 30))
            self.screen.blit(title_text, title_rect)

        for i in range(3):
            for j in range(3):
                x = j * cell + self.x_offset
                y = i * cell + 10 + self.y_offset
                rect = pg.Rect(x, y, cell, cell)
                
                pg.draw.rect(self.screen, beige, rect)
                pg.draw.rect(self.screen, white, rect, 4)

                if highlight and highlight == (i, j):
                    pg.draw.rect(self.screen, blue, rect, 6)

                value = self.state[i][j]
                if value != 0: 
                    text = self.font.render(str(value), True, ebony)
                    text_rect = text.get_rect(center=(x + cell // 2, y + cell // 2))
                    self.screen.blit(text, text_rect)
                    
    def handle_click(self, x, y, puzzle_nums):
        if self.x_offset <= x < self.x_offset + cell * 3 and 80 <= y < 80 + cell * 3:
            row = (y - 80) // cell
            col = (x - self.x_offset) // cell

            if self.state[row][col] is None:
                num = len(puzzle_nums) + 1
                if num == 9:
                    num = 0
                if num not in puzzle_nums:
                    self.state[row][col] = num
                    puzzle_nums.add(num)
                    return True 
        return False


# pg.init()
# screen = pg.display.set_mode((700, 400))
# pg.display.set_caption("8 Puzzle Input")

# ipuzzle = Puzzle(screen, x_offset=100, title="Initial State")
# gpuzzle = Puzzle(screen, x_offset=400, title="Goal State")
# initial_state, goal_state = input_states(screen, ipuzzle, gpuzzle)

# print("Initial State:", initial_state)
# print("Goal State:", goal_state)
# pg.quit()
