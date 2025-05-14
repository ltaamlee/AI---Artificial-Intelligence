import pygame as pg
import pygame_gui as pgui
from assets.button import uninformed_btn, informed_btn, local_btn, complex_btn, csp_btn, rl_btn, ctrl_btn
from assets.color import *
from assets.puzzle import Puzzle
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
    panel_y = 560
    panel_width = width - 2 * 270
    panel_height = 270

    panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel_width, panel_height), border_radius=50)
    screen.blit(panel, (panel_x, panel_y))

    return panel_x, panel_y, panel_width, panel_height

def algo_btn(screen, width):
    panel_x, panel_y, panel_width, panel_height = algo_panel(screen, width)

    uninformed_btn(screen, panel_x + 30, panel_y + 20)
    informed_btn(screen, panel_x + 160, panel_y + 20)
    local_btn(screen, panel_x + 290, panel_y + 20)
    complex_btn(screen, panel_x + 520, panel_y + 20)
    csp_btn(screen, panel_x + 650, panel_y + 20)
    rl_btn(screen, panel_x + 780, panel_y + 20)

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

    bg = pg.image.load(r'assets\LOCK.png').convert()
    bg = pg.transform.scale(bg, (width, height))

    ipuzzle = Puzzle(screen, x_offset = 80, title = "Initial State")
    gpuzzle = Puzzle(screen, x_offset = 680, title = "Goal State")
    x_middle = (ipuzzle.x_offset + gpuzzle.x_offset) // 2
    cpuzzle = Puzzle(screen, x_offset = x_middle, title = "Current State")

    ipuzzle_nums = set()
    gpuzzle_nums = set()
    mode = "input"  

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

            if event.type == pg.MOUSEBUTTONDOWN and mode == "input":
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

        screen.blit(bg, (0, 0))
        draw_name(screen)
        algo_panel(screen, width)
        algo_btn(screen, width)
        
        
        control_panel(screen, width)
        control_btn(screen, width)
        ipuzzle.draw()
        gpuzzle.draw()
        cpuzzle.draw()
        pg.display.flip()

    pg.quit()
