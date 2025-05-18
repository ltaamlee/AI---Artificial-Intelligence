import random
import pygame as pg
import pygame_gui as pgui
from assets.button import uninformed_btn, informed_btn, local_btn, complex_btn, csp_btn, rl_btn, Control_Button, Intro_Button
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

def algo_btn(screen, width, ip1, ip2, ip3):
    panel_x, panel_y, panel_width, panel_height = algo_panel(screen, width)

    uninformed_btn(screen, panel_x + 30, panel_y + 20, lambda: handle_algo_click("Uninformed", ip1.state, ip2.state, ip3.state))
    informed_btn(screen, panel_x + 170, panel_y + 20, lambda: handle_algo_click("Informed", ip1.state, ip2.state, ip3.state))
    local_btn(screen, panel_x + 310, panel_y + 20)#, lambda: handle_algo_click("Local", ip1.state, ip2.state, ip3.state))
    complex_btn(screen, panel_x + 540, panel_y + 20) #lambda: handle_algo_click("Complex", ip1.state, ip2.state, ip3.state))
    csp_btn(screen, panel_x + 670, panel_y + 20)#, lambda: handle_algo_click("CSP", ip1.state, ip2.state, ip3.state))
    rl_btn(screen, panel_x + 800, panel_y + 20)#, lambda: handle_algo_click("RL", ip1.state, ip2.state, ip3.state))

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
      
def handle_algo_click(algo_name, state1, state2, state3, solution=None):
    print(f"Đã chọn thuật toán: {algo_name}")
    print("Trạng thái 1:", state1)
    print("Trạng thái 2:", state2)
    print("Trạng thái 3:", state3)
    
    if solution:
        print("Giải thuật trả về:", solution)
    
    # TODO: gọi giải thuật tương ứng tại đây

#====================================================================================#
def base():
    pg.init()

    width = pg.display.Info().current_w
    height = pg.display.Info().current_h
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("8-Puzzle")

    bg = pg.image.load(r'assets\beach4.jpg').convert()
    bg = pg.transform.scale(bg, (width, height))

    ipuzzle1 = BPuzzle(screen, 100, 50, "Initial State")
    ipuzzle2 = BPuzzle(screen, 100, ipuzzle1.y_offset + 260)
    ipuzzle3 = BPuzzle(screen, 100, ipuzzle2.y_offset + 260)
    gpuzzle2 = Puzzle(screen, 700, "Goal State 2")
    x_middle = (ipuzzle1.x_offset + gpuzzle2.x_offset) // 2
    gpuzzle1 = Puzzle(screen, x_offset = x_middle, title="Goal State 1")

    gpuzzle1_nums = set()
    gpuzzle2_nums = set()
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
    clock = pg.time.Clock()
    path_visualizer = PathVisualizer(screen, width, pg.font.SysFont('Montserrat', 24))


    btn_prev = Control_Button('./assets/prev.png', 50, 50, (1050, 300), 2)
    btn_play = Control_Button('./assets/play.png', 50, 50, (1130, 300), 2)
    btn_pause = Control_Button('./assets/pause.png', 50, 50, (1210, 300), 2)
    btn_next = Control_Button('./assets/next.png', 50, 50, (1290, 300), 2)
    btn_restart = Control_Button('./assets/restart.png', 50, 50, (1370, 300), 2)

    buttons = [btn_prev, btn_play, btn_pause, btn_next, btn_restart]

            
    last_update_time = pg.time.get_ticks()
    update_interval = 1000
    algo_exec_time = None 
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
                if len(gpuzzle1_nums) < 9:
                    gpuzzle1.handle_click(x, y, gpuzzle1_nums)
                elif len(gpuzzle2_nums) < 9:
                    gpuzzle2.handle_click(x, y, gpuzzle2_nums)
                    
                elif len(gpuzzle1_nums) == 9 and len(gpuzzle2_nums) == 9:
                    mode = "done"
                    print("Initial State:", type(ipuzzle1.state))
                    print("Goal State:", type(gpuzzle1.state))



        screen.blit(bg, (0, 0))
        draw_name(screen)
        algo_panel(screen, width)
        algo_btn(screen, width, ipuzzle1, ipuzzle2, ipuzzle3)


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



        for btn in buttons:
            btn.draw(screen)

        # Xử lý sự kiện click nút điều khiển
        if btn_prev.check_click(screen):...


        if btn_next.check_click(screen):...


        if btn_play.check_click(screen):...
 

        if btn_pause.check_click(screen):...
           

        if btn_restart.check_click(screen):...
   
        # Xử lý click
        if back_button.check_click(None):
            return "intro"
        # Khởi tạo
        path_visualizer = PathVisualizer(screen, width - 350, pg.font.SysFont('Montserrat', 24), pos_x=400, pos_y=400)

        # Trong vòng lặp game hoặc hàm render
        path_visualizer.draw(solution, 1, True)
        pg.display.flip()

    pg.quit()
