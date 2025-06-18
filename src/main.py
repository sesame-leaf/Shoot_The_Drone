import random
import sys
import pygame
import time

from module.UI_Components import *
from UI_Surface_design import *
from entity import *


# constant settings
SCREEN_WIDTH = 1400
SCREEN_HEIHGT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIHGT)


# variables
# screen list: "lobby", "ingame"
current_screen_name = "lobby"
screens = dict({"lobby":pygame.Surface(SCREEN_SIZE), "ingame":pygame.Surface(SCREEN_SIZE), "game_over":pygame.Surface(SCREEN_SIZE)})


# initialize pygame
pygame.init()


# pygame settings
display = pygame.display
clock = pygame.time.Clock()


# screen & window settings
base_screen = display.set_mode(size=SCREEN_SIZE)

title_label = pygame.font.SysFont(None, 60).render("Shoot The Drone!", True, "#000000")

start_button = Button(start_button_surface, ((SCREEN_WIDTH-start_button_surface.get_width())//2, (SCREEN_HEIHGT-start_button_surface.get_height())//2))
to_lobby_button = Button(to_lobby_button_surface, (0, 0))


# ingame objects
player = Person((150, 550), 8)
bullets = list([])
drone = Drone((1200, 150), (50, 30))
score = 0
start_time = None
time_limit = 60


# run game
game_running = True
while game_running:
    
    if current_screen_name == "lobby":
        
        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            
            # check start button pressed
            if start_button.is_clicked(event):
                current_screen_name = "ingame"
                start_time = int(time.time())
                score = 0
        
        # screen settings
        my_screen = screens["lobby"]
        
        # draw screen
        my_screen.fill("#ffffff")
        
        # blit to screen
        my_screen.blit(title_label, ((my_screen.get_width()-title_label.get_width())//2, (my_screen.get_height()-title_label.get_height())//5))
        start_button.draw(my_screen)
        
        screens["lobby"] = my_screen
    
    
    elif current_screen_name == "ingame":
        
        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                
            # check to_lobby_button pressed
            if to_lobby_button.is_clicked(event):
                current_screen_name = "lobby"
                
            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                bullets.append(Bullet(player.get_hand_pos(), player.get_arm_angle(), 30))
        
        # screen settings
        my_screen = screens["ingame"]
        
        # draw screen
        my_screen.fill("#00bfff")
        
        # ground graphic
        ground = pygame.Surface((SCREEN_WIDTH, 100))
        ground.fill("#8b4513")
        my_screen.blit(ground, (0, SCREEN_HEIHGT-ground.get_height()))
        
        # score board text
        score_board_text = pygame.font.SysFont(None, 30).render(f"SCORE: {score}", True, "#000000")
        my_screen.blit(score_board_text, (90, 5))
        
        # left time text
        elapse_time = int(time.time()) - start_time
        left_time_text = pygame.font.SysFont(None, 30).render(f"TIME_LEFT: {time_limit-elapse_time}", True, "#000000")
        my_screen.blit(left_time_text, (90, score_board_text.get_height()+5))
        
        # objects update
        player.move_arm_pos(pygame.mouse.get_pos())
        player.draw(my_screen)
        drone.draw(my_screen)
        
        # draw bullet
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(my_screen)
            
            # 화면 밖으로 나가면 총알 제거
            pos = bullet.get_position()
            if (pos[0] < 0 or pos[0] > SCREEN_WIDTH) or pos[1] > SCREEN_HEIHGT-ground.get_height():
                bullets.remove(bullet)
                continue
                
            # 충돌 감지
            if drone.is_active() and bullet.is_active() and drone.check_collision(pos, bullet.get_radius()):
                drone.hit()
                bullet.deactivate()
                
                score += 1
                
                new_drone_x = random.randint(500, SCREEN_WIDTH-drone.get_width()-1)
                new_drone_y = random.randint(0, SCREEN_HEIHGT-ground.get_height()-drone.get_height()-1)
                drone = Drone((new_drone_x, new_drone_y), (50, 30))
        
        if time_limit <= elapse_time:
            current_screen_name = "game_over"
        
        # blit to screen
        to_lobby_button.draw(my_screen)
        
        screens["ingame"] = my_screen
    
    
    elif current_screen_name == "game_over":
        
        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                
            # check to_lobby_button pressed
            if to_lobby_button.is_clicked(event):
                current_screen_name = "lobby"
        
        # screen settings
        my_screen = screens["game_over"]
        
        # draw screen
        my_screen.fill("#ffffff")
        
        # show score
        final_score_text = pygame.font.SysFont(None, 100).render(f"SCORE: {score}", True, "#000000")
        my_screen.blit(final_score_text, ((SCREEN_WIDTH-final_score_text.get_width())//2, (SCREEN_HEIHGT-final_score_text.get_height())//2))
        
        # blit to screen
        to_lobby_button.draw(my_screen)
        
        screens["game_over"] = my_screen
    
    
    # screen update
    display.set_caption(f"{current_screen_name} mouse:{pygame.mouse.get_pos()}")
    base_screen.blit(screens[current_screen_name], (0, 0))
    display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
