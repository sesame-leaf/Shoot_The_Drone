import sys
import pygame
from module.UI_Components import *

from UI_Surface_design import *

# constant settings
SCREEN_WIDTH = 1400
SCREEN_HEIHGT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIHGT)


# variables
# screen list: "lobby", "ingame"
current_screen_name = "lobby"
screens = dict({"lobby":pygame.Surface(SCREEN_SIZE), "ingame":pygame.Surface(SCREEN_SIZE)})


# initialize pygame
pygame.init()


# pygame settings
display = pygame.display
clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 60)

start_button = Button(start_button_surface, ((SCREEN_WIDTH-start_button_surface.get_width())//2, (SCREEN_HEIHGT-start_button_surface.get_height())//2))
to_lobby_button = Button(to_lobby_button_surface, (0, 0))


# screen & window settings
base_screen = display.set_mode(size=SCREEN_SIZE)


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
        
        # screen settings
        my_screen = screens["lobby"]
        
        # draw screen
        my_screen.fill("#ffffff")
        
        title = title_font.render("Shoot The Drone!", True, "#000000")
                
        
        # blit to screen
        my_screen.blit(title, ((my_screen.get_width()-title.get_width())//2, (my_screen.get_height()-title.get_height())//5))
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
        
        # screen settings
        my_screen = screens["ingame"]
        
        # draw screen
        my_screen.fill("#ffffff")
        
        # blit to screen
        to_lobby_button.draw(my_screen)
        
        screens["ingame"] = my_screen
    
    
    # screen update
    base_screen.blit(screens[current_screen_name], (0, 0))
    display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
