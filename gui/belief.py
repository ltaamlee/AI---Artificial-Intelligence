import random
import pygame as pg
import pygame_gui as pgui
from assets.button import uninformed_btn, informed_btn, local_btn, complex_btn, csp_btn, rl_btn, ctrl_btn, Intro_Button
from assets.color import *
from assets.puzzle import Puzzle, BPuzzle
from assets.path import PathVisualizer
#====================================================================================#

def load_music():
    pg.mixer.init()
    pg.mixer.music.load(r'assets\wave.mp3')
    pg.mixer.music.play(loops=-1)

def draw_name(screen):
    font = pg.font.Font(None, 30)
    name_text = font.render("23110312 - Le Thi Thanh Tam", True, black)
    screen.blit(name_text, (1000, 10))

def algo_panel(screen, width, height=None):
    panel_x = 450
    panel_y = 540
    panel_width = width - 2 * 270
    panel_height = 270

    panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel_width, panel_height), border_radius = 50)
    screen.blit(panel, (panel_x, panel_y))

    return panel_x, panel_y, panel_width, panel_height

def algo_btn(screen, width):
    panel_x, panel_y, panel_width, panel_height = algo_panel(screen, width)

    uninformed_btn(screen, panel_x + 30, panel_y + 20)
    informed_btn(screen, panel_x + 170, panel_y + 20)
    local_btn(screen, panel_x + 310, panel_y + 20)
    complex_btn(screen, panel_x + 540, panel_y + 20)
    csp_btn(screen, panel_x + 670, panel_y + 20)
    rl_btn(screen, panel_x + 800, panel_y + 20)
#====================================================================================#

def control_panel(screen, width, hegiht=None):
    panel_x = 1000
    panel_y = 50
    panel_width = width - 1050
    panel_height = 280

    panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel_width, panel_height), border_radius=50)
    screen.blit(panel, (panel_x, panel_y))

    return panel_x, panel_y, panel_width, panel_height

def control_btn(screen, width):
    panel_x, panel_y, panel_width, panel_height = control_panel(screen, width)
    ctrl_btn(screen, panel_x + 50, panel_y + 10)
    
#====================================================================================#
def base():
    pg.init()
    load_music()

    width = pg.display.Info().current_w
    height = pg.display.Info().current_h
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("8-Puzzle")

    bg = pg.image.load(r'assets\beach4.jpg').convert()
    bg = pg.transform.scale(bg, (width, height))

    ipuzzle1 = BPuzzle(screen, 100, 50, "Initial State")
    ipuzzle2 = BPuzzle(screen, 100, ipuzzle1.y_offset + 260)
    ipuzzle3 = BPuzzle(screen, 100, ipuzzle2.y_offset + 260)
    gpuzzle1 = Puzzle(screen, 700, "Goal State 1")
    x_middle = (ipuzzle1.x_offset + gpuzzle1.x_offset) // 2
    gpuzzle2 = Puzzle(screen, x_offset = x_middle, title="Goal State 2")

    gpuzzle_nums = set()
    # cpuzzle.state = [[0 for _ in range(3)] for _ in range(3)]
    mode = "input"

    random_button_rect = pg.Rect((width - 200, 10), (150, 50))  
    solution = [
            [
                [1, 2, 3],
                [4, 5, 6],
                [0, 7, 8]
            ],
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 0, 8]
                
            ]
        ]
    
    back_button = Intro_Button("Back", 150, 40, (width - 180, height - 70), 2)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

            if event.type == pg.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pg.display.set_mode((width, height), pg.RESIZABLE)
                bg = pg.transform.scale(bg, (width, height))
                back_button = Intro_Button("Back", 150, 40, (width - 180, height - 70), 2)


            if event.type == pg.MOUSEBUTTONDOWN:
                if random_button_rect.collidepoint(pg.mouse.get_pos()):
                    # Randomize the initial states 
                    ipuzzle1.state = ipuzzle1.generate_random_state()
                    ipuzzle2.state = ipuzzle2.generate_random_state()
                    ipuzzle3.state = ipuzzle3.generate_random_state()
                    
                    
            # if event.type == pg.MOUSEBUTTONDOWN and mode == "input":
            #     x, y = pg.mouse.get_pos()
            #     if len(gpuzzle_nums) < 9:
            #         gpuzzle.handle_click(x, y, gpuzzle_nums)
            #     elif len(gpuzzle_nums) == 9:
            #         mode = "done"
            #         cpuzzle.state = random.choice([ipuzzle1, ipuzzle2, ipuzzle3]).state.copy()
            #         print("Initial State:", ipuzzle1.state)
            #         print("Goal State:", gpuzzle.state)
                        # if event.type == pg.MOUSEBUTTONDOWN and mode == "input":
                x, y = pg.mouse.get_pos()
                if len(gpuzzle_nums) < 9:
                    gpuzzle1.handle_click(x, y, gpuzzle_nums)
                    gpuzzle2.handle_click(x, y, gpuzzle_nums)
                    
                elif len(gpuzzle_nums) == 9:
                    mode = "done"
                    print("Initial State:", ipuzzle1.state)
                    print("Goal State:", gpuzzle1.state)

        screen.blit(bg, (0, 0))
        draw_name(screen)
        algo_panel(screen, width)
        algo_btn(screen, width)

        # Draw the random button
        pg.draw.rect(screen, (0, 255, 0), random_button_rect)  # Button background (green)
        font = pg.font.Font(None, 30)
        random_text = font.render("Random", True, (0, 0, 0))  # Button text (black)
        screen.blit(random_text, (random_button_rect.x + 40, random_button_rect.y + 10))

        ipuzzle1.draw()
        ipuzzle2.draw()
        ipuzzle3.draw()
        # cpuzzle.draw()
        gpuzzle1.draw()
        gpuzzle2.draw()
        
        
        control_panel(screen, width)
        control_btn(screen, width)
        back_button.draw(screen)

        # Xử lý click
        if back_button.check_click(None):
            return "intro"
        # Khởi tạo
        path_visualizer = PathVisualizer(screen, width - 350, pg.font.SysFont('Montserrat', 24), pos_x=400, pos_y=400)

        # Trong vòng lặp game hoặc hàm render
        path_visualizer.draw(solution, 1, True)
        pg.display.flip()

    pg.quit()
