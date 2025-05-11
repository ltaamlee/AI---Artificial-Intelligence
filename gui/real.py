import pygame as pg
import pygame_gui as pgui
from assets.button import algo_btn, env_btn
from assets.color import *
from assets.puzzle import Puzzle
#====================================================================================#

def load_music():
    pg.mixer.init()
    pg.mixer.music.load(r'assets\wave.mp3')
    pg.mixer.music.play(loops=-1)

def draw_name(screen):
    font = pg.font.Font(None, 30)
    name_text = font.render("23110312 - Le Thi Thanh Tam", True, '#000000')
    screen.blit(name_text, (1000, 10))

def algo_panel(screen, width, height=None):
    panel = pg.Surface((width - 2 * 250, 270), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0,0, panel.get_width(), panel.get_height()), border_radius = 50)
    screen.blit(panel, (250, 570))
    
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

    ipuzzle = Puzzle(screen, x_offset = 100, title = "Initial State")
    gpuzzle = Puzzle(screen, x_offset = 700, title = "Goal State")
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
        algo_btn(screen)
        
        ipuzzle.draw()
        gpuzzle.draw()
        cpuzzle.draw()
        pg.display.flip()

    pg.quit()
