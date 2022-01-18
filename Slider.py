import pygame

pygame.init()
pygame.font.init()

button_font = pygame.font.SysFont("Cambria", 20)

class Slider():

    def __init__(self, start_x, start_y, end_x, end_y, click, hover):
        self.start_x = start_x
        self.og_start = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.click = click
        self.hover = hover
        self.volume = 0
        self.speaker = pygame.image.load("images/volume.png")
    def on_hover(self):
        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()
        if(mouse_location_x >= self.start_x - 7 and mouse_location_y >= self.start_y - 7 and mouse_location_x <= self.end_x and mouse_location_y <= self.end_y):
                self.hover = True
    def on_click(self):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()
        if left_click == True:
            if(self.hover):
                self.click = True
        else:
            self.click = False
        if self.click:
            if mouse_location_x < 1105 and mouse_location_x >= 920:
                self.end_x = mouse_location_x + 10
                self.start_x = mouse_location_x
        self.volume = (self.start_x - 920)/10
        if (mouse_location_x < 900 and mouse_location_x > 870 and mouse_location_y > 50 and mouse_location_y < 65 and left_click) or self.volume == 0:
            self.speaker = pygame.image.load("images/volume mute.png")
            self.volume = 0
        if self.volume > 0:
            self.speaker = pygame.image.load("images/volume.png")

    def draw(self, win):
        win.blit(pygame.image.load("images/slider.png"), (920, 50))
        win.blit(pygame.image.load("images/sliderball.png"), (self.start_x, self.start_y))
        win.blit(self.speaker, (870, 50))
        pygame.display.update()
        pygame.display.flip()