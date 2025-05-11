import pygame as pg
from gui.real import base
from assets.color import *

def title(screen):
    font = font = pg.font.SysFont('Montserrat', 130, bold=True)
    name_text = font.render("8 Puzzle", True, '#277E31')
    screen.blit(name_text, (120, 50))


def load_music():
    pg.mixer.init()
    pg.mixer.music.load(r'assets\wave.mp3')
    pg.mixer.music.play(loops=-1)

def intro_panel(screen, width, height=None):
    panel = pg.Surface((width - 2 * 150, 270), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0,0, panel.get_width(), panel.get_height()), border_radius = 50)
    screen.blit(panel, (150, 270))

def intro():
    pg.init()
     
    load_music()
    
    width = 800
    height = 600
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("8-Puzzle")

    # Load and scale image
    bg = pg.image.load(r'assets\LOCK.png').convert()
    bg = pg.transform.scale(bg, (width, height))
    

    blur = pg.Surface((width, height), pg.SRCALPHA)
    blur.fill((255, 255, 255, 160))  

    belief_screen = False   
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

        blur = pg.Surface((width, height), pg.SRCALPHA)
        blur.fill((255, 255, 255, 160))  
        screen.blit(bg, (0, 0))
        screen.blit(blur, (0, 0)) 
        title(screen)
        intro_panel(screen,width)
        pg.display.flip()

    pg.quit()

base()