import pygame as pg, sys
import pygame_gui as pgui
from assets.color import *
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
        self.text_surf = pg.font.SysFont('Montserrat', 25, bold=True).render(text, True, ALGO_TEXT_COLOR)
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
            self.top_color = tan
            self.text_surf = pg.font.SysFont('Montserrat', 25, bold=True).render(self.text, True, white)

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_shadow = 0
            else:
                self.dynamic_shadow = self.shadow
                if self.pressed == True:
                    print('click')
                    self.pressed = False
        else:
            self.top_color = cream
            self.text_surf = pg.font.SysFont('Montserrat', 25).render(self.text, True, ebony)
            self.dynamic_shadow = self.shadow

def intro_btn(screen):
    btn_real_env = Intro_Button('Real Environment', 280, 50, (720, 280), 2)
    btn_complex_env = Intro_Button('Complex Environment', 320, 50, (700, 350), 2)
    btn_csp = Intro_Button('Constraint Satisfaction Problem', 500, 50, (620, 420), 2)
    
    btn_real_env.check_click(screen), btn_complex_env.check_click(screen), btn_csp.check_click(screen)
    btn_real_env.draw(screen), btn_complex_env.draw(screen), btn_csp.draw(screen)

#====================================================================================#
class Algo_Button:
    def __init__(self, text, width, height, pos, shadow):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]
        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = ALGO_TOP_COLOR
        
        # text 
        self.text = text
        self.text_surf = pg.font.SysFont('Montserrat', 25).render(text, True, ALGO_TEXT_COLOR)
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
            self.top_color = ALGO_TOP_COLOR_CLICK
            self.text_surf = pg.font.Font(None, 25).render(self.text, True, ALGO_TEXT_CLICK)

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_shadow = 0
            else:
                self.dynamic_shadow = self.shadow
                if self.pressed == True:
                    print('click')
                    self.pressed = False
        else:
            self.top_color = ALGO_TOP_COLOR
            self.text_surf = pg.font.Font(None, 25).render(self.text, True, ALGO_TEXT_COLOR)
            self.dynamic_shadow = self.shadow
                           
def uninformed_btn(screen):
    btn_bfs = Algo_Button('BFS', 100, 40, (300, 600), 2)
    btn_dfs = Algo_Button('DFS', 100, 40, (300, 660), 2)
    btn_ucs = Algo_Button('UCS', 100, 40, (300, 720), 2)
    btn_ids = Algo_Button('IDS', 100, 40, (300, 780), 2)
    
    btn_bfs.check_click(screen), btn_dfs.check_click(screen), btn_ucs.check_click(screen), btn_ids.check_click(screen)
    btn_bfs.draw(screen), btn_dfs.draw(screen), btn_ucs.draw(screen), btn_ids.draw(screen)

def informed_btn(screen):
    btn_gds = Algo_Button('GDS', 100, 40, (450, 600), 2)
    btn_astar = Algo_Button('A*', 100, 40, (450, 660), 2)
    btn_ida = Algo_Button('IDA*', 100, 40, (450, 720), 2)
    
    btn_gds.check_click(screen), btn_astar.check_click(screen), btn_ida.check_click(screen)
    btn_gds.draw(screen), btn_astar.draw(screen), btn_ida.draw(screen)

def local_btn(screen):
    btn_shc = Algo_Button('SHC', 100, 40, (590, 600), 2)
    btn_sahc = Algo_Button('SAHC', 100, 40, (590, 660), 2)
    btn_stohc = Algo_Button('STOHC', 100, 40, (590, 720), 2)
    btn_sa = Algo_Button('SA', 100, 40, (590, 780), 2)
    btn_ga = Algo_Button('GA', 100, 40, (700, 600), 2)
    btn_bs = Algo_Button('BS', 100, 40, (700, 660), 2)
    
    btn_shc.check_click(screen), btn_sahc.check_click(screen), btn_stohc.check_click(screen), btn_sa.check_click(screen)
    btn_ga.check_click(screen), btn_bs.check_click(screen)
    
    btn_shc.draw(screen), btn_sahc.draw(screen), btn_stohc.draw(screen), btn_sa.draw(screen)
    btn_ga.draw(screen), btn_bs.draw(screen)              
          
def complex_btn(screen):
    btn_andor = Algo_Button('AND-OR', 100, 40, (850, 600), 2)       

    btn_andor.check_click(screen)
    btn_andor.draw(screen)
    
#Constraint Satisfaction Problem
def csp_btn(screen):
    btn_bt = Algo_Button('BT', 100, 40, (990, 600), 2)
    btn_fc = Algo_Button('FC', 100, 40, (990, 660), 2)
    btn_ac_3 = Algo_Button('AC-3', 100, 40, (990, 720), 2)
    
    btn_bt.check_click(screen), btn_fc.check_click(screen), btn_ac_3.check_click(screen)
    btn_bt.draw(screen), btn_fc.draw(screen), btn_ac_3.draw(screen)

#reinforcement learning
def rl_btn(screen):
    btn_q_learning = Algo_Button('Q-Learning',130, 40, (1130, 600), 2)
    
    btn_q_learning.check_click(screen)
    btn_q_learning.draw(screen)

def algo_btn(screen):
    uninformed_btn(screen)
    informed_btn(screen)
    local_btn(screen)
    complex_btn(screen)
    csp_btn(screen)
    rl_btn(screen)
    
#====================================================================================#
class Env_Button:
    def __init__(self, text, width, height, pos, shadow):
        self.pressed = False
        self.shadow = shadow
        self.dynamic_shadow = shadow
        self.y_pos = pos[1]
        
        # surface btn
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = ENV_TOP_COLOR
        
        # text 
        self.text = text
        self.text_surf = pg.font.Font(None, 25).render(text, True, ENV_TEXT_COLOR)
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
            self.top_color = ENV_TOP_COLOR
            self.text_surf = pg.font.Font(None, 25).render(self.text, True, ENV_TEXT_COLOR)

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