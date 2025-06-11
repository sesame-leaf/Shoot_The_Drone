import sys
import pygame


pygame.init()


# lobby screen
start_button_surface = pygame.Surface((600, 100))
start_button_surface.fill("#ff0000")
__start_button_text = pygame.font.SysFont(None, 50).render("START", True, "#000000")
start_button_surface.blit(__start_button_text, ((start_button_surface.get_width()-__start_button_text.get_width())//2, (start_button_surface.get_height()-__start_button_text.get_height())//2))


# ingame screen
to_lobby_button_surface = pygame.Surface((80, 50))
to_lobby_button_surface.fill("#ff0000")
__to_lobby_button_text = pygame.font.SysFont(None, 20).render("To Lobby", True, "#000000")
to_lobby_button_surface.blit(__to_lobby_button_text, ((to_lobby_button_surface.get_width()-__to_lobby_button_text.get_width())//2, (to_lobby_button_surface.get_height()-__to_lobby_button_text.get_height())//2))
