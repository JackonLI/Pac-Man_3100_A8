
"""
Project: Pac-Man A8 in CSCI3100, CUHK
Program: Generate homepage for user to choose mode
Main Contributors: ZHANGJuyuan
Created: March 28, 2023
Last Modified: May 6, 2023
Github Access: https://github.com/JackonLI/Pac-Man_3100_A8
Description: 
This program serves as the Start-code and database of the whole class. After the start command, the game will open the database and do identify part of user, then start game.
Dependencies:
- pygame and mysql
- homepage.py
How to use it:
# you can modify the database function according to the database instruction guide on the github website and then start the game with your local database.
Known issues:
Each time you want to enter the input, you should click the input box because of the function limition
If you can not type-in, you could check your inputting method, the input box only accept English
Acknowledgement and References: 
Bandai Namco Entertainment America Inc: https://www.bandainamcoent.com/games/pac-man
Github project: https://github.com/greyblue9/pacman-python
Github project: https://github.com/lylant/PacMan-Pygame
"""

import pygame
import pymysql
import sys
import homepage


pygame.init()
dic = {}
# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (151, 255, 255)
SCREEN_SIZE = (900, 500)

# Fond
FONT = pygame.font.Font('zig_____.ttf', 15)
font = pygame.font.Font('zig_____.ttf', 15)
# Database
db = pymysql.connect(host="localhost", user="root", password="vw#5y#ub", database="records", charset="utf8")
cursor = db.cursor()
cursor.execute("use records")
cursor.execute("CREATE TABLE IF NOT EXISTS proj_db(\
   name VARCHAR(100) NOT NULL,\
   password VARCHAR(100) NOT NULL,\
   score int,\
   PRIMARY KEY (name)\
)")
def starting_interface():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Login')
    screen.fill(BG_COLOR)
    while True:
        bg_image = pygame.image.load("back.png")
        bg_image = pygame.transform.scale(bg_image, (900, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    choose_start()
        screen.blit(bg_image, (0, 0))
        pygame.display.flip()

def choose_start():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Choose to start')
    screen.fill(BG_COLOR)
    choose = input_box(screen, "Type 1 for Login, 2 for Register", 200, 300, 1)
    if int(choose) == 1:
        Login()
    elif int(choose) == 2:
        Register()
    else:
        choose_start() 



def render_text1(text, font, color=(255, 0, 0)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def render_text2(text, font, color=(102, 156, 255)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def input_box(screen, prompt, x, y, c):
    bg_image = pygame.image.load("loginbg.png")
    bg_image = pygame.transform.scale(bg_image, (900, 500))
    input_rect = pygame.Rect(x, y, 200, 24)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    active = False
    text = ''


    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                
        if c == 1:
            screen.fill(BG_COLOR)
            prompt_surface, prompt_rect = render_text1(prompt, FONT)
            screen.blit(bg_image, (0, 0))
            prompt_rect.topleft = (x, y - 40)
            screen.blit(prompt_surface, prompt_rect)
            

            text_surface, text_rect = render_text1(text, FONT)
            text_rect.topleft = (x + 5, y + 5)
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (255, 0, 0), input_rect, 2)
            pygame.display.flip()
        else:
            screen.fill(BG_COLOR)
            prompt_surface, prompt_rect = render_text2(prompt, FONT)
            screen.blit(bg_image, (0, 0))
            prompt_rect.topleft = (x, y - 40)
            screen.blit(prompt_surface, prompt_rect)
            

            text_surface, text_rect = render_text2(text, FONT)
            text_rect.topleft = (x + 5, y + 5)
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (102, 156, 255), input_rect, 2)
            pygame.display.flip()

def Register():
    screen1 = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Register')
    screen1.fill(BG_COLOR)

    while True:
        name = input_box(screen1, "Please enter the username you want to register with:", 150, 300, 2)
        cursor.execute('SELECT * FROM proj_db WHERE name = %s' % repr(name))
        result = cursor.fetchall()
        if len(result) > 0:
            x = input_box(screen1, "The username already exists, 0 for register again ,1 for login", 150, 300, 2)
            if int(x) == 0 :
                Register()
            else:
                Login()
        else:
            pass1 = input_box(screen1, "Please input a password:", 200, 300, 2)
            pass2 = input_box(screen1, "Please confirm the password again:", 200, 300, 2)
            if pass1 == pass2 :
                dic[name] = (pass1, 0)
                Update_database(name)
                y = input_box(screen1, "Registration successful, type 1 log in! else register\n", 150, 300, 2)
                if y == "1":
                    Login()
                else:
                    Register()
                break

def Login():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Login')
    screen.fill(BG_COLOR)

    while True:
        user_name = input_box(screen, "Click the inputbox and enter your username:", 180, 300, 1)
        cursor.execute('SELECT * FROM proj_db WHERE name = %s' % repr(user_name))
        result = cursor.fetchall()
        if len(result) > 0:
            user_pass = input_box(screen, "Please input your password:", 200, 300, 1)
            cursor.execute('SELECT password FROM proj_db WHERE name = %s' % repr(user_name))
            pwd = cursor.fetchall()
            if user_pass == pwd[0][0]:
                dic[user_name] = (user_pass, 0)
                cont = input_box(screen, "Login successful!, type 1 to continue!(else login)", 150, 300, 1)
                cursor.execute('SELECT score FROM proj_db WHERE name = %s' % repr(user_name))
                score = cursor.fetchone()
                if cont == '1':
                    print(score[0])
                    newHomepage = homepage.Homepage(user_name, score[0], list(rank_list()))
                    screen = pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
                    newHomepage.main_menu()
                    newInfo = newHomepage.update_info()
                    score1 = newInfo[0]
                    score2 = newInfo[1]
                    score3 = newInfo[2]
                    Update_score(score1, score2, score3)
                    screen = pygame.display.set_mode((700, 500), flags=pygame.SHOWN)
                    result = []
                    screen = pygame.display.set_mode(SCREEN_SIZE)
                else:
                    Login()
            else:
                cont = input_box(screen, "Password error, logged out!, type 1 to login(else register)", 150, 300, 1)
                if cont == '1':
                    Login()
                else:
                    Register()
        elif len(result) == 0:
            #display_sentence(screen, "The user you entered does not exist!", 175, 200)
            YN = input_box(screen, "Do you need to register a user(if register,enter:1 login,enter:0): ", 70, 300, 2)
            if YN == '1':
                Register()
            else:
                Login()

def Update_database(user):
    cursor.execute("Delete from proj_db where name = %s" % (repr(user)))
    cursor.execute("insert into proj_db (name, password, score) VALUES (%s, %s, %s)" % (repr(user), repr(dic[user][0]), repr(dic[user][1])))
    db.commit()
    pass

def Update_score(user, score, flag):
    if flag == 0:
        cursor.execute("SELECT score FROM proj_db where name = %s" % (repr(user)))
        record = cursor.fetchone()

        if int(record[0]) >= int(score):
            pass
        else:
            cursor.execute("Delete from proj_db where name = %s" % (repr(user)))
            cursor.execute("insert into proj_db (name, password, score) VALUES (%s, %s, %s)" % (repr(user), repr(dic[user][0]), repr(score)))
    else:
        cursor.execute("Delete from proj_db where name = %s" % (repr(user)))
        cursor.execute("insert into proj_db (name, password, score) VALUES (%s, %s, %s)" % (repr(user), repr(dic[user][0]), repr(score)))
    db.commit()
# ... Other functions and database operations ...

def rank_list():
    cursor.execute('SELECT name, score FROM proj_db ORDER BY score DESC LIMIT 10')
    return cursor.fetchall()

starting_interface()
db.commit()
db.close()