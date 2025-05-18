import pygame as pg
import time
from assets.button import uninformed_btn, informed_btn, local_btn, complex_btn, csp_btn, rl_btn, ctrl_btn, Intro_Button
from assets.color import *
from assets.puzzle import Puzzle
from assets.path import PathVisualizer
from algorithms import BFS, DFS

#====================================================================================#

def load_music():
    pg.mixer.init()
    pg.mixer.music.load(r'assets\wave.mp3')
    pg.mixer.music.play(loops=-1)

def draw_name(screen):
    font = pg.font.Font(None, 30)
    name_text = font.render("23110312 - Le Thi Thanh Tam", True, black)
    screen.blit(name_text, (1000, 10))

#====================================================================================#

def algo_panel(screen, width, height=None):
    panel_x = 250
    panel_y = 540
    panel_width = width - 2 * 270
    panel_height = 270

    panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel_width, panel_height), border_radius=50)
    screen.blit(panel, (panel_x, panel_y))

    return panel_x, panel_y, panel_width, panel_height

def algo_btn(screen, width, initial_state=None, goal_state=None, callback=None):
    panel_x, panel_y, _, _ = algo_panel(screen, width)

    uninformed_btn(screen, panel_x + 30, panel_y + 20, initial_state, goal_state, callback)
    informed_btn(screen, panel_x + 160, panel_y + 20, initial_state, goal_state, callback)
    local_btn(screen, panel_x + 290, panel_y + 20, initial_state, goal_state, callback)
    #complex_btn(screen, panel_x + 520, panel_y + 20, initial_state, goal_state, callback)
    #csp_btn(screen, panel_x + 650, panel_y + 20, initial_state, goal_state, callback)
    #rl_btn(screen, panel_x + 780, panel_y + 20, initial_state, goal_state, callback)
    
#====================================================================================#

def control_panel(screen, width, height=None):
    panel_x = 1000
    panel_y = 50
    panel_width = width - 1050
    panel_height = 280

    panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel_width, panel_height), border_radius=50)
    screen.blit(panel, (panel_x, panel_y))

    return panel_x, panel_y, panel_width, panel_height

def control_btn(screen, width):
    panel_x, panel_y, _, _ = control_panel(screen, width)
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

    ipuzzle = Puzzle(screen, x_offset=80, title="Initial State")
    gpuzzle = Puzzle(screen, x_offset=680, title="Goal State")
    x_middle = (ipuzzle.x_offset + gpuzzle.x_offset) // 2
    cpuzzle = Puzzle(screen, x_offset=x_middle, title="Current State")

    ipuzzle_nums = set()
    gpuzzle_nums = set()
    mode = "input"
    solution_path = None  # Khởi tạo biến này để tránh lỗi khi chưa có lời giải

    back_button = Intro_Button("Back", 150, 40, (width - 180, height - 70), 2)
    clock = pg.time.Clock()
    path_visualizer = PathVisualizer(screen, width, pg.font.SysFont('Montserrat', 24))

    def on_algo_click(algo_name, solution):
        nonlocal solution_path, mode, cpuzzle
        print(f"Bạn đã chọn: {algo_name}")
        if solution:
            solution_path = solution
            mode = "done"
            cpuzzle.state = ipuzzle.state.copy()
            cpuzzle.set_solution(solution_path)
            print(f"Lời giải với {len(solution_path) - 1} bước")
            for step_num, state in enumerate(solution_path):
                print(f"Step {step_num}: {state}")
        else:
            print("Không tìm thấy lời giải")
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

            elif event.type == pg.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pg.display.set_mode((width, height), pg.RESIZABLE)
                bg = pg.transform.scale(bg, (width, height))
                back_button = Intro_Button("Back", 150, 40, (width - 180, height - 70), 2)

            elif event.type == pg.MOUSEBUTTONDOWN and mode == "input":
                x, y = pg.mouse.get_pos()
                if len(ipuzzle_nums) < 9:
                    ipuzzle.handle_click(x, y, ipuzzle_nums)
                elif len(gpuzzle_nums) < 9:
                    gpuzzle.handle_click(x, y, gpuzzle_nums)
                if len(ipuzzle_nums) == 9 and len(gpuzzle_nums) == 9:
                    mode = "done"
                    cpuzzle.state = ipuzzle.state.copy()
                    print("Initial State:", ipuzzle.state)
                    print("Goal State:", gpuzzle.state)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cpuzzle.next_step()
                elif event.key == pg.K_LEFT:
                    cpuzzle.prev_step()
                elif event.key == pg.K_r:
                    cpuzzle.restart()
                elif event.key == pg.K_SPACE:
                    if cpuzzle.is_playing:
                        cpuzzle.pause()
                    else:
                        cpuzzle.play()

        screen.blit(bg, (0, 0))
        draw_name(screen)
        ipuzzle.draw()
        gpuzzle.draw()
        cpuzzle.draw_with_move_highlight()
        cpuzzle.update()
        algo_btn(screen, width, ipuzzle.state, gpuzzle.state, on_algo_click)
        control_panel(screen, width)
        control_btn(screen, width)

        back_button.draw(screen)
        if back_button.check_click(None):
            return "intro"
        last_update_time = 0
        update_interval = 1000
        current_time = pg.time.get_ticks()
        if cpuzzle.is_playing and current_time - last_update_time > update_interval:
            cpuzzle.next_step()
            last_update_time = current_time
            
        # Vẽ path_visualizer liên tục khi đã có lời giải
        if mode == "done" and solution_path:
            path_visualizer.draw(solution_path, cpuzzle.current_step, True)


        pg.display.flip()
        clock.tick(60)
    pg.quit()
