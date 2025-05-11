import pygame as pg
import pygame_gui as pgui
from assets.button import algo_btn, env_btn
from assets.color import *
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

    # Load and scale image
    bg = pg.image.load(r'assets\LOCK.png').convert()
    bg = pg.transform.scale(bg, (width, height))
    

    # blur = pg.Surface((width, height), pg.SRCALPHA)
    # blur.fill((255, 255, 255, 160))  

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

        screen.blit(bg, (0, 0))
        draw_name(screen)
        algo_panel(screen, width)
        algo_btn(screen)
        env_btn(screen)
        # screen.blit(blur, (0, 0))  
        pg.display.flip()

    pg.quit()

