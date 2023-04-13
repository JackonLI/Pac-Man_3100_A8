import os
import pygame, sys, random
import game
mainClock = pygame.time.Clock()
from pygame.locals import *

GREY = (240, 248, 255)
PURPLE = (153, 102, 204)
SCREENSIZE = [700, 500]


class Homepage(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
    def update_info(self):
        return self.name, self.score
 
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def main_menu(self):
        pygame.init()
        pygame.display.set_caption('Homepage')
        screen = pygame.display.set_mode((700, 500),0)
        SIZE = (700, 500)
        font = pygame.font.SysFont(None, 30)
            
            
        scores = [("Alice", 100), ("Bob", 200), ("Charlie", 150), ("David", 50), ("David", 50), ("David", 50), ("David", 50), ("David", 50), ("David", 50), ("David", 50)]
        snow_list = []
        for i in range(200):
            x = random.randrange(0, SIZE[0])
            y = random.randrange(0, SIZE[1])
            sx = random.randint(0, 1)
            sy = random.randint(3, 6)
            snow_list.append([x, y, sx, sy])

        clock = pygame.time.Clock()
        click = False
        while True:
    
            screen.fill((151,255,255))
            self.draw_text('Main Menu', font, (0,0,0), screen, 300, 40)
    
            mx, my = pygame.mouse.get_pos()

            #creating buttons
            button_1 = pygame.Rect(260, 80, 180, 50)
            button_2 = pygame.Rect(260, 150, 180, 50)
            button_3 = pygame.Rect(260, 220, 180, 50)
            button_4 = pygame.Rect(260, 290, 180, 50)
            button_5 = pygame.Rect(260, 360, 180, 50)
            button_6 = pygame.Rect(260, 430, 180, 50)
            
            
            #defining functions when a certain button is pressed
            if button_1.collidepoint((mx, my)):
                if click:
                    self.game()
            if button_2.collidepoint((mx, my)):
                if click:
                    self.game()
            if button_3.collidepoint((mx, my)):
                if click:
                    self.rankList(scores)
            if button_4.collidepoint((mx, my)):
                if click:
                    self.setting()
            if button_5.collidepoint((mx, my)):
                if click:
                    help()
            if button_6.collidepoint((mx, my)):
                if click:
                    Login()
            pygame.draw.rect(screen, (151,255,255), button_1)
            pygame.draw.rect(screen, (151,255,255), button_2)
            pygame.draw.rect(screen, (151,255,255), button_3)
            pygame.draw.rect(screen, (151,255,255), button_4)
            pygame.draw.rect(screen, (151,255,255), button_5)
            pygame.draw.rect(screen, (151,255,255), button_6)
            
            
    
            #writing text on top of button
            self.draw_text('BASIC GAME', font, (255,105,180), screen, 284, 98)
            self.draw_text('AI GAME', font, (255,110,180), screen, 305, 168)
            self.draw_text('RANK LIST', font, (238,106,167), screen, 295, 238)
            self.draw_text('SETTING', font, (205,96,144), screen, 305, 308)
            self.draw_text('HELP', font, (139,58,98), screen, 322, 378)
            self.draw_text('BACK TO LOGOUT', font, (205,92,92), screen, 260, 448)
            
            
            for i in range(len(snow_list)):
            # 绘制雪花，颜色、位置、大小
                pygame.draw.circle(screen, (255, 255, 255), snow_list[i][:2], snow_list[i][3]-3)
    
            # 移动雪花位置（下一次循环起效）
                snow_list[i][0] += snow_list[i][2]
                snow_list[i][1] += snow_list[i][3]
    
            # 如果雪花落出屏幕，重设位置
                if snow_list[i][1] > SIZE[1]:
                    snow_list[i][1] = random.randrange(-50, -10)
                    snow_list[i][0] = random.randrange(0, SIZE[0])
            
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
            pygame.display.flip()
            mainClock.tick(60)
            clock.tick(20)
    
    """
    This function is called when the "PLAY" button is clicked.
    """
    def game(self):
        newGame = game.Game(500)
        #pygame.display.iconify()
        screen = pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
        newGame.run()
        print("Score: {}".format(newGame.statusScore))
        print("New high score: {}".format(newGame.statusRecord))
        newGame.close()
        screen = pygame.display.set_mode((700, 500), flags=pygame.SHOWN)
        #newHomepage.main_menu()

    def rankList(self, scores):
        pygame.init()
        screen = pygame.display.set_mode((700, 500))
        screen.fill((255,228,196))
        pygame.display.set_caption('RANK LIST')

        # Define the font and font size
        font = pygame.font.SysFont(None, 30)
        click = False
        # Loop through the array and render each element to the screen
        for i, (name, score) in enumerate(scores):
            text = f"{i+1}: {name} - {score}"
            rendered_text = font.render(text, True, (255,127,0))
            rect = rendered_text.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.y = i * 40 + 50
            screen.blit(rendered_text, rect)

        # Update the Pygame display

        # Run the Pygame event loop
        while True:
            button_1 = pygame.Rect(500, 430, 180, 50)
            mx, my = pygame.mouse.get_pos()
            if button_1.collidepoint((mx, my)):
                if click:
                    self.main_menu()
            pygame.draw.rect(screen, (255,228,196), button_1)
            self.draw_text('BACK TO MENU', font, (255,106,106), screen, 520, 442)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.flip()
            
    def setting(self):
        pygame.init()
        pygame.display.set_caption('SETTING')
        # Set up the display
        screen = pygame.display.set_mode((700, 500))

        # Load the initial background music
        initial_bg_music = "bg_music.mp3"
        pygame.mixer.music.load(initial_bg_music)
        pygame.mixer.music.play()

        # Set up the font
        font = pygame.font.SysFont(None, 32)

        # Set up the initial volume
        volume = 0.5
        pygame.mixer.music.set_volume(volume)

        # Set up the input box
        input_box = pygame.Rect(180, 300, 200, 32)
        input_text = ""

        # Set up the warning message timer
        warning_timer = 0

        # Set up the current music file variable
        current_music_file = initial_bg_music

        # Main game loop
        running = True
        click = False
        while running:
            screen.fill((255,228,196))
            button_1 = pygame.Rect(250, 420, 200, 60)
            mx, my = pygame.mouse.get_pos()
            if button_1.collidepoint((mx, my)):
                if click:
                    self.main_menu()
            pygame.draw.rect(screen, (255,228,196), button_1)
            self.draw_text('BACK TO MENU', font, (255,106,106), screen, 265, 442)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        # Check if the input text is a valid music file name
                        if input_text.endswith(".mp3") and os.path.isfile(input_text):
                            # Change the background music to the user's input
                            try:
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load(input_text)
                                pygame.mixer.music.play()
                                current_music_file = input_text  # Update the current music file variable
                                warning_timer = 0
                            except pygame.error:
                                print("Error: Could not load music file.")
                            else:
                                print("Music file changed to:", input_text)
                        else:
                            print("Invalid music file name.")
                            warning_text = font.render("Invalid file name!", True, (255, 0, 0))
                            warning_timer = 120  # Set the warning timer to 120 frames (2 seconds)
                        
                        # Clear the input box
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character from the input text
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_UP:
                        # Increase the volume by a small amount
                        volume = min(volume + 0.05, 1.0)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_DOWN:
                        # Decrease the volume by a small amount
                        volume = max(volume - 0.05, 0.0)
                        pygame.mixer.music.set_volume(volume)
                    else:
                        # Add the pressed character to the input text
                        input_text += event.unicode
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # Draw the current state of the music player
            music_text = font.render("Music file: {}".format(os.path.basename(current_music_file)), True, (0, 0, 0))
            screen.blit(music_text, (180, 140))
            volume_text = font.render("Volume: {:.0%}".format(volume), True, (0, 0, 0))
            screen.blit(volume_text, (180, 180))
            volume_hint_text = font.render("Use arrow keys to adjust volume", True, (0, 0, 0))
            screen.blit(volume_hint_text, (180, 220))

            # Draw the input box and text
            input_hint_text = font.render("Enter a music file name (e.g. music1.mp3)", True, (0, 0, 0))
            screen.blit(input_hint_text, (180, 260))
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            input_text_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(input_text_surface, (input_box.x + 5, input_box.y + 5))

            # Draw the warning message if necessary
            if warning_timer > 0:
                warning_text = font.render("Invalid file name!", True, (255, 0, 0))
                screen.blit(warning_text, (180, 340))
                warning_timer -= 1
            elif 'warning_text' in locals():
                del warning_text

            # Update the screen
            pygame.display.flip()


    def help(self):
        screen = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption('HELP')
        clock = pygame.time.Clock()
        tickspeed = 60
        running = True
        content = [line.strip('\n')
                for line in open('text.txt', 'r').readlines()]
        font = pygame.font.SysFont(None, 20)
        font_regular = pygame.font.SysFont(None, 30)
        click = False
        while running:
            screen.fill(GREY)
            button_1 = pygame.Rect(250, 420, 200, 60)
            mx, my = pygame.mouse.get_pos()
            if button_1.collidepoint((mx, my)):
                if click:
                    self.main_menu()
            pygame.draw.rect(screen, GREY, button_1)
            self.draw_text('BACK TO MENU', font_regular, (255,106,106), screen, 270, 442)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            for n, line in enumerate(content):
                text = font.render(line, 1, PURPLE)
                text_rect = text.get_rect()
                text_rect.centerx = SCREENSIZE[0]//2
                text_rect.centery = n*25 + 50
                screen.blit(text, text_rect)
            pygame.display.flip()
            mainClock.tick(60)

newHomepage = Homepage(123, 456)
newHomepage.main_menu()

