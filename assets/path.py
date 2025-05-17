import pygame as pg
from assets.color import *

class PathVisualizer:
    def __init__(self, screen, width, font, pos_x=50, pos_y=400):
        self.screen = screen
        self.width = width
        self.font = font
        self.path_box_width = width - 100
        self.path_box_height = 90
        self.path_box = pg.Rect(pos_x, pos_y, self.path_box_width, self.path_box_height)
        self.step_size = 60
        self.title_font = pg.font.SysFont('Montserrat', 30, bold=True)

    def get_move_direction(self, current_state, next_state):
        current_zero = next((i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0)
        next_zero = next((i, j) for i in range(3) for j in range(3) if next_state[i][j] == 0)

        diff = (next_zero[0] - current_zero[0], next_zero[1] - current_zero[1])
        return {(-1, 0): "U", (1, 0): "D", (0, -1): "L", (0, 1): "R"}.get(diff, "N")

    def get_moved_value(self, current_state, next_state):
        for i in range(3):
            for j in range(3):
                if current_state[i][j] != 0 and current_state[i][j] != next_state[i][j]:
                    return current_state[i][j]
        return None


    def draw_box(self):
                # Vẽ khung ngoài (luôn luôn vẽ)
        pg.draw.rect(self.screen, baby_blue, self.path_box, border_radius=50)
        pg.draw.rect(self.screen, blue, self.path_box, 2, border_radius=50)

        # Vẽ tiêu đề
        title = self.title_font.render("Solution Path:", True, white)
        self.screen.blit(title, (self.path_box.x + 10, self.path_box.y - 50))
        
    def draw(self, solution, current_step, selected_button):
        # Vẽ khung ngoài (luôn luôn vẽ)
        pg.draw.rect(self.screen, baby_blue, self.path_box, border_radius=50)
        pg.draw.rect(self.screen, blue, self.path_box, 2, border_radius=50)

        # Vẽ tiêu đề
        title = self.title_font.render("Solution Path:", True, white)
        self.screen.blit(title, (self.path_box.x + 10, self.path_box.y - 50))

        # Nếu không có lời giải hoặc chưa chọn thuật toán, KHÔNG vẽ các bước
        if not selected_button or not solution or len(solution) <= 1:
            return

        # Tiếp tục vẽ các bước như cũ
        visible_steps = min(self.path_box_width // self.step_size - 1, len(solution) - 1)
        start_idx = max(0, min(current_step - visible_steps // 2, len(solution) - visible_steps - 1))
        end_idx = min(start_idx + visible_steps, len(solution) - 1)

        for i in range(start_idx, end_idx + 1):
            x = self.path_box.x + 10 + (i - start_idx) * self.step_size
            y = self.path_box.y + 40

            # Vẽ vòng tròn cho từng bước
            circle_color = yellow if i == current_step else blue
            pg.draw.circle(self.screen, circle_color, (x + self.step_size // 2, y), 20)

            # Hiển thị nhãn bước
            if i == 0:
                label = "S"
            else:
                moved_val = self.get_moved_value(solution[i - 1], solution[i])
                label = str(moved_val) if moved_val is not None else "?"

            text = self.font.render(label, True, black)
            self.screen.blit(text, (x + self.step_size // 2 - text.get_width() // 2, y - text.get_height() // 2))

            # Mũi tên & hướng đi
            if i < end_idx:
                arrow_start = (x + self.step_size // 2 + 20, y)
                arrow_end = (x + self.step_size + self.step_size // 2 - 20, y)
                pg.draw.line(self.screen, black, arrow_start, arrow_end, 2)
                pg.draw.polygon(self.screen, black, [
                    (arrow_end[0], arrow_end[1]),
                    (arrow_end[0] - 8, arrow_end[1] - 6),
                    (arrow_end[0] - 8, arrow_end[1] + 6)
                ])

                move_dir = self.get_move_direction(solution[i], solution[i + 1])
                dir_text = self.font.render(move_dir, True, black)
                self.screen.blit(dir_text, ((arrow_start[0] + arrow_end[0]) // 2 - dir_text.get_width() // 2, y + 12))
