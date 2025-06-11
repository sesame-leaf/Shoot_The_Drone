import sys
import pygame


class Button:
    def __init__(self, Surface:pygame.Surface, top_left:tuple[int, int]):
        self.__surface = Surface
        self.__top_left = top_left
        self.__rect = self.__surface.get_rect(topleft=self.__top_left)
        
    def draw(self, screen:pygame.Surface):
        pygame.draw.rect(screen, "#00000000", self.__rect)
        screen.blit(self.__surface, self.__top_left)
        
    def is_clicked(self, event:pygame.event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.__rect.collidepoint(event.pos)

