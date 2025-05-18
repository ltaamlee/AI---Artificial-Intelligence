import pygame as pg
from assets.color import *
from assets.button import Intro_Button

#====================================================================================#

def title(screen):
    text = "8 Puzzle"
    font_size = 130
    font = pg.font.SysFont('Montserrat', font_size, bold=True)

    main_color = baby_blue  
    glow_color = cream 

    text_surface = font.render(text, True, main_color)

    for offset in range(1, 6):
        glow_surface = font.render(text, True, glow_color)
        glow_surface.set_alpha(30)  
        screen.blit(glow_surface, (300 - offset, 50 - offset))
        screen.blit(glow_surface, (300 + offset, 50 - offset))
        screen.blit(glow_surface, (300 - offset, 50 + offset))
        screen.blit(glow_surface, (300 + offset, 50 - offset))

    shadow_surface = font.render(text, True, (0, 0, 0))
    shadow_surface.set_alpha(80)
    screen.blit(shadow_surface, (303, 53))

    screen.blit(text_surface, (300, 50))

def load_music():
    pg.mixer.init()
    pg.mixer.music.load(r'assets\wave.mp3')
    pg.mixer.music.play(loops=-1)

def intro_panel(screen, width, height=None):
    panel = pg.Surface((width - 2 * 330, 330), pg.SRCALPHA)
    pg.draw.rect(panel, color_algo_panel, (0, 0, panel.get_width(), panel.get_height()), border_radius=50)
    
    font = pg.font.SysFont('Montserrat', 28, bold=True)
    info_lines = [
        "ID: 23110312",
        "Name: Lê Thị Thanh Tâm",
        "ARIN330585_04",
        "Mentor: Phan Thị Huyền Trang"
    ]
    
    for i, line in enumerate(info_lines):
        text = font.render(line, True, '#000000')
        screen.blit(text, (100, 280 + i * 50))

    screen.blit(panel, (600, 220))

#====================================================================================#

def intro():
    pg.init()
     
    load_music()
    
    width = 1200
    height = 600
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("8-Puzzle")

    # Load and scale background
    bg = pg.image.load(r'assets\beach3.png').convert()
    bg = pg.transform.scale(bg, (width, height))
    
    # Buttons
    btn_real_env = Intro_Button('Real Environment', 280, 50, (720, 250), 2)
    btn_complex_env = Intro_Button('Complex Environment', 320, 50, (700, 320), 2)
    btn_csp = Intro_Button('Constraint Satisfaction Problem', 500, 50, (620, 390), 2)
    btn_rl = Intro_Button('Reinforcement Learning', 460, 50, (650, 460), 2)
    btn_quit = Intro_Button('Quit', 150, 50, (100, height - 80), 2)

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
        title(screen)
        intro_panel(screen, width)


        btn_real_env.draw(screen)
        btn_complex_env.draw(screen)
        btn_csp.draw(screen)
        btn_rl.draw(screen)
        btn_quit.draw(screen)

        # Kiểm tra click
        if btn_real_env.check_click(None):
            from gui.real import base
            base()
        elif btn_complex_env.check_click(None):
            from gui.belief import base
            base()
        elif btn_csp.check_click(None):
            from gui.csp import base
            base()
        elif btn_quit.check_click(None):
            running = False

        pg.display.flip()
    
    pg.quit()

intro()