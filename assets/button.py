import pygame as pg, sys
import time
from assets.color import *
from algorithms import *
#====================================================================================#
class Intro_Button:
    def __init__(self, text, width, height, pos, shadow):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]
        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = beige
        
        # text 
        self.text = text
        self.text_surf = pg.font.SysFont('Montserrat', 25, bold=True).render(text, True, algo_text)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        
        # shadow btn
        self.bottom_rect = pg.Rect(pos, (width, shadow))
        self.bottom_color = SHADOW

    def draw(self,screen):
        self.top_rect.y = self.y_pos - self.dynamic_shadow
        self.text_rect.center = self.top_rect.center
        
        # shadow position
        shadow_offset = 5
        self.bottom_rect.midtop = (self.top_rect.midtop[0] + shadow_offset, self.top_rect.midtop[1] + shadow_offset )
        self.bottom_rect.height = self.top_rect.height + self.dynamic_shadow
        
        # draw shadow and button
        pg.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 50)
        pg.draw.rect(screen, self.top_color, self.top_rect, border_radius = 50)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, screen):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = beige
            self.text_surf = pg.font.SysFont('Montserrat', 25, bold=True).render(self.text, True, black)

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_shadow = 0
            else:
                self.dynamic_shadow = self.shadow
                if self.pressed:
                    self.pressed = False
                    return True
        else:
            self.top_color = cream
            self.text_surf = pg.font.SysFont('Montserrat', 25).render(self.text, True, ebony)
            self.dynamic_shadow = self.shadow

#====================================================================================#
class Algo_Button:
    def __init__(self, text, width, height, pos, shadow, algo_func=None):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]

        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = algo_color
        
        # text 
        self.text = text
        self.text_surf = pg.font.SysFont('Montserrat', 20, bold=True).render(text, True, algo_text)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        
        # shadow btn
        self.bottom_rect = pg.Rect(pos, (width, shadow))
        self.bottom_color = SHADOW
        
        # algo for btn
        self.algo_func = algo_func
        self.solution = None

    def draw(self,screen):
        self.top_rect.y = self.y_pos - self.dynamic_shadow
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        
        # shadow position
        shadow_offset = 5
        self.bottom_rect.midtop = (self.top_rect.midtop[0] + shadow_offset, self.top_rect.midtop[1] + shadow_offset )
        self.bottom_rect.height = self.top_rect.height + self.dynamic_shadow
        
        # draw shadow and button
        pg.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 50)
        pg.draw.rect(screen, self.top_color, self.top_rect, border_radius = 50)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, screen, initial_state=None, goal_state=None, callback=None):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]  # nút chuột trái
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = algo_top_click
            self.text_surf = pg.font.SysFont('Montserrat', 20, bold=True).render(self.text, True, algo_text_click)

            if mouse_pressed and not self.pressed:
                self.pressed = True # Tránh lặp

                start = time.perf_counter()

                
                if self.algo_func and initial_state is not None and goal_state is not None:
                    self.solution = self.algo_func(initial_state, goal_state)
                else:
                    self.solution = None
                end = time.perf_counter()
                elapsed = end - start
                
                
                global algo_exec_time
                algo_exec_time = elapsed
                
                if callback:
                    callback(self.text, self.solution, elapsed)

                self.dynamic_shadow = 0

            elif not mouse_pressed:
                self.pressed = False
                self.dynamic_shadow = self.shadow

        else:
            self.pressed = False
            self.top_color = algo_color
            self.text_surf = pg.font.SysFont('Montserrat', 20, bold=True).render(self.text, True, algo_text)
            self.dynamic_shadow = self.shadow


                                      
def uninformed_btn(screen, base_x, base_y, initial_state=None, goal_state=None, callback=None):
    buttons = [
        Algo_Button('BFS', 100, 40, (base_x, base_y), 2, algo_func=BFS),
        Algo_Button('DFS', 100, 40, (base_x, base_y + 60), 2, algo_func=DFS),
        Algo_Button('UCS', 100, 40, (base_x, base_y + 120), 2, algo_func=UCS),
        Algo_Button('IDS', 100, 40, (base_x, base_y + 180), 2, algo_func=IDS),
    ]
    for btn in buttons:
        btn.check_click(screen, initial_state, goal_state, callback)
        btn.draw(screen)

def informed_btn(screen, base_x, base_y, initial_state=None, goal_state=None, callback=None):
    buttons = [
        Algo_Button('GDS', 100, 40, (base_x, base_y), 2, algo_func=GDS),
        Algo_Button('A*', 100, 40, (base_x, base_y + 60), 2, algo_func=ASTAR),
        Algo_Button('IDA*', 100, 40, (base_x, base_y + 120), 2, algo_func=IDAS),
    ]
    for btn in buttons:
        btn.check_click(screen, initial_state, goal_state, callback)
        btn.draw(screen)
        
def local_btn(screen, base_x, base_y, initial_state=None, goal_state=None, callback=None):
    buttons = [
        Algo_Button('SHC', 100, 40, (base_x, base_y), 2, algo_func=SHC),
        Algo_Button('SAHC', 100, 40, (base_x, base_y + 60), 2, algo_func= SAHC),
        Algo_Button('STOHC', 100, 40, (base_x, base_y + 120), 2, algo_func=Stochastic),
        Algo_Button('SA', 100, 40, (base_x, base_y + 180), 2, algo_func=SA),
        Algo_Button('GA', 100, 40, (base_x + 110, base_y), 2, algo_func=GEN),
        Algo_Button('BS', 100, 40, (base_x + 110, base_y + 60), 2, algo_func=BS),
    ]
    for btn in buttons:
        btn.check_click(screen, initial_state, goal_state, callback)
        btn.draw(screen)   
    
def complex_btn(screen, base_x, base_y, initial_state=None, goal_state=None, callback=None):
    btn = Algo_Button('AND-OR', 100, 40, (base_x, base_y), 2, algo_func=ANDOR)
    btn.check_click(screen, initial_state, goal_state, callback)
    btn.draw(screen) 
    
#Constraint Satisfaction Problem
def csp_btn(screen, base_x, base_y):
    buttons = [
        Algo_Button('BT', 100, 40, (base_x, base_y), 2),
        Algo_Button('FC', 100, 40, (base_x, base_y + 60), 2),
        Algo_Button('AC-3', 100, 40, (base_x, base_y + 120), 2),
    ]
    for btn in buttons:
        btn.check_click(screen)
        btn.draw(screen)
        
#reinforcement learning
def rl_btn(screen, base_x, base_y):
    btn = Algo_Button('Q-Learning', 130, 40, (base_x, base_y), 2)
    btn.check_click(screen)
    btn.draw(screen)
    
#====================================================================================#
class Env_Button:
    def __init__(self, text, width, height, pos, shadow):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]
        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = yellow
        
        # text 
        self.text = text
        self.text_surf = pg.font.Font(None, 25).render(text, True, red)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        
        # shadow btn
        self.bottom_rect = pg.Rect(pos, (width, shadow))
        self.bottom_color = SHADOW

    def draw(self,screen):
        self.top_rect.y = self.y_pos - self.dynamic_shadow
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        
        # shadow position
        shadow_offset = 5
        self.bottom_rect.midtop = (self.top_rect.midtop[0] + shadow_offset, self.top_rect.midtop[1] + shadow_offset )
        self.bottom_rect.height = self.top_rect.height + self.dynamic_shadow
        
        # draw shadow and button
        pg.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 50)
        pg.draw.rect(screen, self.top_color, self.top_rect, border_radius = 50)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, screen):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = yellow
            self.text_surf = pg.font.Font(None, 25).render(self.text, True, red)

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                if self.text == "Belief":  
                    current_screen = "belief_screen" 
                self.dynamic_shadow = 0
            else:
                self.dynamic_shadow = self.shadow
                if self.pressed == True:
                    
                    self.pressed = False
        else:
            self.dynamic_shadow = self.shadow
        
def env_btn(screen):
    btn_real = Env_Button('Real', 80, 40, (1300, 780), 2)
    btn_belief = Env_Button('Belief', 80, 40, (1400, 780), 2)
    
    btn_real.check_click(screen), btn_belief.check_click(screen)
    btn_real.draw(screen), btn_belief.draw(screen)
    
#====================================================================================#
class Control_Button:
    def __init__(self, icon_path, width, height, pos, shadow):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]
        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = yellow
        
        # icon 
        self.icon = pg.image.load(icon_path).convert_alpha()
        self.icon = pg.transform.scale(self.icon, (25, 25))  
        self.icon_rect = self.icon.get_rect(center=self.top_rect.center)
        
        # shadow btn
        self.bottom_rect = pg.Rect(pos, (width, shadow))
        self.bottom_color = SHADOW

    def draw(self,screen):
        self.top_rect.y = self.y_pos - self.dynamic_shadow
        self.icon_rect = self.icon.get_rect(center=self.top_rect.center)
        
        # shadow position
        shadow_offset = 5
        self.bottom_rect.midtop = (self.top_rect.midtop[0] + shadow_offset, self.top_rect.midtop[1] + shadow_offset )
        self.bottom_rect.height = self.top_rect.height + self.dynamic_shadow
        
        # draw shadow and button
        pg.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 50)
        pg.draw.rect(screen, self.top_color, self.top_rect, border_radius = 50)
        screen.blit(self.icon, self.icon_rect)

    def check_click(self, screen):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = yellow

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_shadow = 0
            else:
                self.dynamic_shadow = self.shadow
                if self.pressed:
                    self.pressed = False
                    return True
        else:
            self.top_color = yellow
            self.dynamic_shadow = self.shadow


# def ctrl_btn(screen, base_x, base_y):
#     btn_prev = Control_Button('./assets/prev.png', 50, 50, (base_x, 300), 2)
#     btn_play = Control_Button('./assets/play.png', 50, 50, (base_x + 80, 300), 2)
#     btn_pause = Control_Button('./assets/pause.png', 50, 50, (base_x + 160, 300), 2)
#     btn_next = Control_Button('./assets/next.png', 50, 50, (base_x + 240, 300), 2)
#     btn_restart = Control_Button('./assets/restart.png', 50, 50, (base_x + 320, 300), 2)

#     buttons = [btn_prev, btn_play, btn_pause, btn_next, btn_restart]
#     for btn in buttons:
#         btn.draw(screen)

#     return btn_prev, btn_play, btn_pause, btn_next, btn_restart
