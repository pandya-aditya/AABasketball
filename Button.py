import pygame

pygame.init()
pygame.font.init()

button_font = pygame.font.SysFont("Cambria", 20)

class Button():

    def __init__(self, start_x, start_y, end_x, end_y, click):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.click = click

    def on_click(self):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()
        if left_click == True:
            if(mouse_location_x >= self.start_x and mouse_location_y >= self.start_y and mouse_location_x <= self.end_x and mouse_location_y <= self.end_y):
                self.click = True
        else:
            self.click = False

    def draw(self, win):

        pygame.display.update()
        pygame.display.flip()