import pygame
from random import randint
import time
import math

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("Calibri", 40)
court = pygame.image.load("images/Court.png")
stamina_bar = pygame.image.load("images/stamina_bar.png")

class Player():
    #1820 out of bounds line
    def __init__(self, characterX, characterY, image, horizontal_vel, vertical_vel, distance, stamina, possession, player_movement):
        self.x = characterX
        self.y = characterY
        self.Image = image
        self.reset_possession = False
        self.possession_change = False
        self.ballStopped = False
        self.possession = possession
        self.player_movement = player_movement
        self.horizontal_vel = horizontal_vel
        self.vertical_vel = vertical_vel
        self.distance = distance
        self.distance_net = math.sqrt((self.x - 870)**2 + (self.y - 540)**2)
        self.last_horizontal = "a"
        self.last_vertical = "w"
        self.stamina = stamina
        self.score = 0
        self.stamina_count = 0
        self.section = 3
        self.steal_action = 1
        self.crossover_timer = 1
        self.in_and_out_timer = 1
        self.spinmove_timer = 1
        self.crossover_action = False
        self.in_and_out1 = False
        self.in_and_out2 = False
        self.spinmove1 = False
        self.spinmove2 = False
        self.basketball_x = self.x + 50
        self.basketball_y = self.y - 25
        self.soundlist = [pygame.mixer.Sound("audio/Let's goo.wav"),
                         pygame.mixer.Sound("audio/Scottie.wav"),
                         pygame.mixer.Sound("audio/Pascal.wav"),
                         pygame.mixer.Sound("audio/Wooo.wav"),
                         pygame.mixer.Sound("audio/1.wav"),
                         pygame.mixer.Sound("audio/2.wav"),
                         pygame.mixer.Sound("audio/3.wav"),
                         pygame.mixer.Sound("audio/4.wav"),
                         pygame.mixer.Sound("audio/5.wav")]
                         
        self.is_it_in = pygame.mixer.Sound("audio/is it in.wav")
        self.its_good = pygame.mixer.Sound("audio/It's good.wav")
        self.its_not_in = pygame.mixer.Sound("audio/It's not in.wav")
        self.i = 0
    def draw(self, win):
        if self.i % 200 == 0:
            sound = self.soundlist[randint(0, len(self.soundlist)-1)]
            sound.set_volume(0.01)
            pygame.mixer.Sound.play(sound)
        self.i += 1
        win.blit(self.Image, (self.x, self.y))
        stamina_bar_value = self.stamina // 10
        if self.player_movement == 1:
            score_visual = str(self.score)
            title_font = pygame.font.SysFont("Cambria", 200)
            score_display = title_font.render(score_visual, False, (14, 209, 69))
            win.blit(score_display, (100, 280))
            win.blit(pygame.image.load("./images/p1.png"), (self.x + 20, self.y - 50))
            if self.possession == True:
                win.blit(pygame.image.load("./images/basketball.png"), (self.basketball_x, self.basketball_y))
            for i in range(0, stamina_bar_value):
                if(i == 0):
                    win.blit(stamina_bar, (50, 75))
                else:
                    add_stamina_bar = (20 + 5) * i + 50
                    win.blit(stamina_bar, (add_stamina_bar, 75))
        if self.player_movement == 2:
            score_visual = str(self.score)
            title_font = pygame.font.SysFont("Cambria", 200)
            score_display = title_font.render(score_visual, False, (90, 93, 218))
            win.blit(score_display, (100, 550))
            win.blit(pygame.image.load("./images/p2.png"), (self.x + 20, self.y - 50))
            if self.possession == True:
                win.blit(pygame.image.load("./images/basketball.png"), (self.basketball_x, self.basketball_y))
            for i in range(0, stamina_bar_value):
                if(i == 0):
                    win.blit(stamina_bar, (50, 975))
                else:
                    add_stamina_bar = (20 + 5) * i + 50
                    win.blit(stamina_bar, (add_stamina_bar, 975))
        win.blit(pygame.image.load("./images/untitled.png"), (1880, 1030))
    def move(self, win, opponent_x, opponent_y):
        
        if(self.stamina != 100):
            self.stamina_count += 1
        self.steal_action += 1
        self.crossover_timer += 1
        self.in_and_out_timer += 1
        self.spinmove_timer += 1

        if(self.stamina_count % 500 == 0 and self.stamina < 100):
            self.stamina += 10

        if self.y >= 920:
            self.section = 1
        if self.y >= 720 and self.y < 920:
            self.section = 2
        if self.y >= 360 and self.y < 720:
            self.section = 3
        if self.y >= 160 and self.y < 360:
            self.section = 4
        if self.y >= 0 and self.y < 160:
            self.section = 5

        keys = pygame.key.get_pressed()
        # movement for player 1
        if self.player_movement == 1:
            left = True
            down = True
            up = True
            right = True
            if(self.x >= opponent_x - 54 and self.x <= opponent_x + 54 and self.y >= opponent_y and self.y <= opponent_y + 54):
                up = False
            if(self.x <= opponent_x and self.x >= opponent_x - 54 and self.y >= opponent_y - 54 and self.y <= opponent_y + 54):
                right = False
            if(self.x >= opponent_x and self.x <= opponent_x + 54 and self.y >= opponent_y - 54 and self.y <= opponent_y + 54):
                left = False
            if(self.x >= opponent_x - 54 and self.x <= opponent_x + 54 and self.y <= opponent_y and self.y >= opponent_y - 54):
                down = False
            if keys[pygame.K_a] and self.x >= 340 and left and not self.ballStopped:
                self.x -= self.horizontal_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25
            if keys[pygame.K_d] and self.x <= 1766 and right and not self.ballStopped:
                self.x += self.horizontal_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25
            if keys[pygame.K_s] and self.y <= 1026 and down and not self.ballStopped:
                self.y += self.vertical_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y + 50
            if keys[pygame.K_w] and self.y >= 0 and up and not self.ballStopped:
                self.y -= self.vertical_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25
            if self.possession == True:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    pygame.mixer.Sound.play(self.is_it_in)
                    self.basketball_x = self.x
                    self.basketball_y = self.y
                    shot_percentage = 0
                    shot_percentage = randint(0, 100)
                    distance_net = math.sqrt((self.x - 1845)**2 + (self.y - 540)**2)
                    if self.distance > 200:
                        self.distance = 337
                    if distance_net > 1300:
                        distance_net = 1700
                    shot_probability = int(((100 - ((450 - self.distance)/6)) + (100 - distance_net/10))/2)
                    if shot_probability <= 0:
                        shot_probability = 2
                    if shot_probability >= 100:
                        shot_probability = 99
                    print(shot_probability, 100 - distance_net/12, 100 - (450 - self.distance)/6)
                    if(shot_percentage >= 0 and shot_percentage <= shot_probability):
                        if distance_net < 920:
                            self.score += 1
                        else:
                            self.score += 2
                        self.reset_possession = True
                        while self.basketball_x < 1790:
                            rise = (self.y - 520)/(self.x - 1790)
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 20, self.basketball_y + (20*rise)))
                            self.basketball_y = self.basketball_y + (20*rise)
                            self.basketball_x = self.basketball_x + 20
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        
                        pygame.mixer.Sound.play(self.its_good)
                    else:
                        self.possession_change = True
                        self.basketball_x = self.x
                        self.basketball_y = self.y
                        while self.basketball_x < 1790:
                            rise = (self.y - 520)/(self.x - 1790)
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 20, self.basketball_y + (20*rise)))
                            self.basketball_y = self.basketball_y + (20*rise)
                            self.basketball_x = self.basketball_x + 20
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        while self.basketball_x >= 1690:
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 10, self.basketball_y + 10))
                            self.basketball_y = self.basketball_y + 10
                            self.basketball_x = self.basketball_x - 10
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        pygame.mixer.Sound.play(self.its_not_in)
                    self.stamina -= 10
                    self.ballStopped = False
                    pygame.display.update()
                    pygame.display.flip()
                    time.sleep(1)
                elif not self.ballStopped:
                    # crossover

                    if keys[pygame.K_e] and self.crossover_timer % 40 == 0 and not self.crossover_action:
                        if self.section == 1:
                            self.x -= 60
                        elif self.section == 2:
                            self.x -= 60
                            self.y -= 60
                        elif self.section == 3:
                            self.y -= 60
                        elif self.section == 4:
                            self.x += 60
                            self.y -= 60
                        elif self.section == 5:
                            self.x += 60
                        self.basketball_y = self.y - 40
                        self.crossover_action = True
                    elif self.crossover_action == True and self.crossover_timer % 40 == 0:
                        if self.section == 1:
                            self.x += 100
                        elif self.section == 2:
                            self.x += 100
                            self.y += 100
                        elif self.section == 3:
                            self.y += 100
                        elif self.section == 4:
                            self.x -= 100
                            self.y += 100
                        elif self.section == 5:
                            self.x -= 100
                        self.basketball_y = self.y + 50
                        self.crossover_action = False

                    # stepback
                    if keys[pygame.K_q]:
                        if self.section == 1:
                            self.y += 60
                        elif self.section == 2:
                            self.x -= 40
                            self.y += 40
                        elif self.section == 3:
                            self.x -= 60
                        elif self.section == 4:
                            self.x -= 40
                            self.y -= 40
                        elif self.section == 5:
                            self.y -= 60 
                        self.ballStopped = True
                    # in and out
                    if keys[pygame.K_f] and self.in_and_out_timer % 40 == 0 and not self.in_and_out2 and not self.in_and_out1:
                        if self.section == 1:
                            self.x -= 50
                        elif self.section == 2:
                            self.x -= 50
                            self.y -= 50
                        elif self.section == 3:
                            self.y -= 50
                        elif self.section == 4:
                            self.x += 50
                            self.y -= 50
                        elif self.section == 5:
                            self.x += 50
                        self.in_and_out1 = True
                    elif self.in_and_out1:
                        if self.section == 1:
                            self.x += 85
                        elif self.section == 2:
                            self.x += 85
                            self.y += 85
                        elif self.section == 3:
                            self.y += 85
                        elif self.section == 4:
                            self.x -= 85
                            self.y += 85
                        elif self.section == 5:
                            self.x -= 85
                        self.in_and_out2 = True
                        self.in_and_out1 = False
                    elif self.in_and_out2:
                        if self.section == 1:
                            self.x += 50
                        elif self.section == 2:
                            self.x -= 50
                            self.y -= 50
                        elif self.section == 3:
                            self.y -= 50
                        elif self.section == 4:
                            self.x += 50
                            self.y -= 50
                        elif self.section == 5:
                            self.x += 50                    
                        self.in_and_out2 = False
                    # spinmove
                    if keys[pygame.K_x] and self.spinmove_timer % 40 == 0 and not self.spinmove2 and not self.spinmove1:
                        if self.section == 1:
                            self.x -= 6
                        elif self.section == 2:
                            self.x -= 6
                            self.y -= 6
                        elif self.section == 3:
                            self.y -= 6
                        elif self.section == 4:
                            self.x += 6
                            self.y -= 6
                        elif self.section == 5:
                            self.x += 6
                        self.spinmove1 = True
                    elif self.spinmove1:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x += 10
                            self.y += 10
                        elif self.section == 3:
                            self.y += 10
                        elif self.section == 4:
                            self.x -= 10
                            self.y += 10
                        elif self.section == 5:
                            self.x -= 10
                        self.spinmove2 = True
                        self.spinmove1 = False
                    elif self.spinmove2:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x -= 10
                            self.y -= 10
                        elif self.section == 3:
                            self.y -= 10
                        elif self.section == 4:
                            self.x += 10
                            self.y -= 10
                        elif self.section == 5:
                            self.x += 10
                        self.spinmove2 = False
                    self.basketball_x = self.x + 50
            elif self.possession == False: # Defensive Moves
                # steal mechanic
                    if keys[pygame.K_c]:
                    # check if the distance between the two players is close enough for the defender to attempt a steal
                    # check if the player has attempted a steal in the past second to avoid spamming of the steal button
                        if(self.distance <= 54 and self.steal_action % 60 == 0):
                            steal_percentage = 0
                            steal_percentage = randint(0, 100) # randomized percentage for successful steal
                            # depending on the stamina of the defender, the steal percentage is different
                            if(self.stamina >= 0 and self.stamina <= 20):
                                if(steal_percentage >= 0 and steal_percentage <= 5):
                                    self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                            if(self.stamina >= 21 and self.stamina <= 40):
                                if(steal_percentage >= 0 and steal_percentage <= 10):
                                    self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                            if(self.stamina >= 41 and self.stamina <= 60):
                                if(steal_percentage >= 0 and steal_percentage <= 15):
                                    self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                            if(self.stamina >= 61 and self.stamina <= 80):
                                if(steal_percentage >= 0 and steal_percentage <= 20):
                                    self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                            if(self.stamina >= 81 and self.stamina <= 100):
                                if(steal_percentage >= 0 and steal_percentage <= 25):
                                    self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                            self.stamina -= 10 # each steal causes the defender to lose 10 stamina


        # movement for the defender        
        
        if self.player_movement == 2:
            left = True
            down = True
            up = True
            right = True
            if(self.x >= opponent_x - 75 and self.x <= opponent_x + 75 and self.y >= opponent_y and self.y <= opponent_y + 75):
                up = False
            if(self.x <= opponent_x and self.x >= opponent_x - 75 and self.y >= opponent_y - 75 and self.y <= opponent_y + 75):
                right = False
            if(self.x >= opponent_x and self.x <= opponent_x + 75 and self.y >= opponent_y - 75 and self.y <= opponent_y + 75):
                left = False
            if(self.x >= opponent_x - 75 and self.x <= opponent_x + 75 and self.y <= opponent_y and self.y >= opponent_y - 75):
                down = False
            if keys[pygame.K_LEFT] and self.x >= 340 and left and not self.ballStopped:
                self.x -= self.horizontal_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25
            if keys[pygame.K_RIGHT] and self.x <= 1766 and right and not self.ballStopped:
                self.x += self.horizontal_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25
            if keys[pygame.K_DOWN] and self.y <= 1026 and down and not self.ballStopped:
                self.y += self.vertical_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y + 50
            if keys[pygame.K_UP] and self.y >= 0 and up and not self.ballStopped:
                self.y -= self.vertical_vel
                self.basketball_x = self.x + 50
                self.basketball_y = self.y - 25

            if self.possession == True: # Moves on Offense

  
                    
                if keys[pygame.K_SPACE]:
                    pygame.mixer.Sound.play(self.is_it_in)
                    pygame.display.update()
                    pygame.display.flip()
                    time.sleep(1)
                    shot_percentage = 0
                    shot_percentage = randint(0, 100)
                    distance_net = math.sqrt((self.x - 1845)**2 + (self.y - 540)**2)
                    shot_probability = int(75 + self.stamina/100 + self.distance/30 - distance_net/20)
                    print(shot_probability, distance_net, self.distance)
                    self.basketball_x = self.x
                    self.basketball_y = self.y 
                    if(shot_percentage >= 0 and shot_percentage <= shot_probability):
                        if distance_net < 920:
                            self.score += 1
                        else:
                            self.score += 2
                        self.reset_possession = True
                        while self.basketball_x < 1790:
                            rise = (self.y - 520)/(self.x - 1790)
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 20, self.basketball_y + (20*rise)))
                            self.basketball_y = self.basketball_y + (20*rise)
                            self.basketball_x = self.basketball_x + 20
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        
                        pygame.mixer.Sound.play(self.its_good)
                    else:
                        self.possession_change = True
                        self.basketball_x = self.x
                        self.basketball_y = self.y
                        while self.basketball_x < 1790:
                            rise = (self.y - 520)/(self.x - 1790)
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 20, self.basketball_y + (20*rise)))
                            self.basketball_y = self.basketball_y + (20*rise)
                            self.basketball_x = self.basketball_x + 20
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        while self.basketball_x >= 1690:
                            win.blit(court, (0, 0))
                            win.blit(pygame.image.load("images/basketball.png"), (self.basketball_x + 10, self.basketball_y + 10))
                            self.basketball_y = self.basketball_y + 10
                            self.basketball_x = self.basketball_x - 10
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(0.01)
                        pygame.mixer.Sound.play(self.its_not_in)
                    self.stamina -= 10
                    self.ballStopped = False
                    pygame.display.update()
                    pygame.display.flip()
                    time.sleep(1)

                if not self.ballStopped:
                    # crossover
                    self.basketball_x = self.x + 50
                    if keys[pygame.K_j] and self.crossover_timer % 40 == 0 and not self.crossover_action:
                        
                        if self.section == 1:
                            self.x -= 60
                        elif self.section == 2:
                            self.x -= 60
                            self.y -= 60
                        elif self.section == 3:
                            self.y -= 60
                        elif self.section == 4:
                            self.x += 60
                            self.y -= 60
                        elif self.section == 5:
                            self.x += 60
                        self.crossover_action = True
                        
                    elif self.crossover_action == True:
                        if self.section == 1:
                            self.x += 100
                        elif self.section == 2:
                            self.x += 100
                            self.y += 100
                        elif self.section == 3:
                            self.y += 100
                        elif self.section == 4:
                            self.x -= 100
                            self.y += 100
                        elif self.section == 5:
                            self.x -= 100
                        
                        self.crossover_action = False
                        
                    # stepback
                    if keys[pygame.K_k]:
                        if self.section == 1:
                            self.y += 60
                        elif self.section == 2:
                            self.x += 40
                            self.y -= 40
                        elif self.section == 3:
                            self.x -= 60
                        elif self.section == 4:
                            self.x -= 40
                            self.y -= 40
                        elif self.section == 5:
                            self.y -= 60
                        self.basketball_x = self.x + 50
                        self.ballStopped = True
                    # in and out
                    if keys[pygame.K_l] and self.in_and_out_timer % 40 == 0 and not self.in_and_out2 and not self.in_and_out1:
                        if self.section == 1:
                            self.x -= 6
                        elif self.section == 2:
                            self.x -= 6
                            self.y -= 6
                        elif self.section == 3:
                            self.y -= 6
                        elif self.section == 4:
                            self.x += 6
                            self.y -= 6
                        elif self.section == 5:
                            self.x += 6
                        self.in_and_out1 = True
                        
                    elif self.in_and_out1:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x += 10
                            self.y += 10
                        elif self.section == 3:
                            self.y += 10
                        elif self.section == 4:
                            self.x -= 10
                            self.y += 10
                        elif self.section == 5:
                            self.x -= 10
                        self.in_and_out2 = True
                        self.in_and_out1 = False
    
                    elif self.in_and_out2:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x -= 10
                            self.y -= 10
                        elif self.section == 3:
                            self.y -= 10
                        elif self.section == 4:
                            self.x += 10
                            self.y -= 10 
                        elif self.section == 5:
                            self.x += 10                    
                        self.in_and_out2 = False
                    # spinmove
                    if keys[pygame.K_p] and self.spinmove_timer % 40 == 0 and not self.spinmove2 and not self.spinmove1:
                        if self.section == 1:
                            self.x -= 6
                        elif self.section == 2:
                            self.x -= 6
                            self.y -= 6
                        elif self.section == 3:
                            self.y -= 6
                        elif self.section == 4:
                            self.x += 6
                            self.y -= 6
                        elif self.section == 5:
                            self.x += 6
                        self.spinmove1 = True
                        
                    elif self.spinmove1:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x += 10
                            self.y += 10
                        elif self.section == 3:
                            self.y += 10
                        elif self.section == 4:
                            self.x -= 10
                            self.y += 10
                        elif self.section == 5:
                            self.x -= 10
                        self.spinmove2 = True
                        self.spinmove1 = False
    
                    elif self.spinmove2:
                        if self.section == 1:
                            self.x += 10
                        elif self.section == 2:
                            self.x -= 10
                            self.y -= 10
                        elif self.section == 3:
                            self.y -= 10
                        elif self.section == 4:
                            self.x += 10
                            self.y -= 10
                        elif self.section == 5:
                            self.x += 10
                        self.spinmove2 = False

            elif self.possession == False: # Defensive Moves

                # steal mechanic
                if keys[pygame.K_SEMICOLON]:
                    # check if the distance between the two players is close enough for the defender to attempt a steal
                    # check if the player has attempted a steal in the past second to avoid spamming of the steal button
                    if(self.distance <= 75 and self.steal_action % 30 == 0):
                        steal_percentage = 0
                        steal_percentage = randint(0, 100) # randomized percentage for successful steal
                        # depending on the stamina of the defender, the steal percentage is different
                        if(self.stamina >= 0 and self.stamina <= 20):
                            if(steal_percentage >= 0 and steal_percentage <= 5):
                                self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                        if(self.stamina >= 21 and self.stamina <= 40):
                            if(steal_percentage >= 0 and steal_percentage <= 10):
                                self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                        if(self.stamina >= 41 and self.stamina <= 60):
                            if(steal_percentage >= 0 and steal_percentage <= 15):
                                self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                        if(self.stamina >= 61 and self.stamina <= 80):
                            if(steal_percentage >= 0 and steal_percentage <= 20):
                                self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                        if(self.stamina >= 81 and self.stamina <= 100):
                            if(steal_percentage >= 0 and steal_percentage <= 25):
                                self.reset_possession = True # if the steal is successful, the possession changes, and the defender gains possession of the ball
                        self.stamina -= 10 # each steal causes the defender to lose 10 stamina
                
