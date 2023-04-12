from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END, Canvas
from threading import Timer
from random import *
import multiplayermaze
import os
import pygame
import time


class Game(object):

    def __init__(self, highscore = 0):

        # initialize tkinter window parameters
        self.root = Tk()
        self.root.title("Pac-Man-A8")
        self.root.geometry("800x640")
        self.root.resizable(0, 0)

        # initialize some engine variables
        self.currentLv = 1  # start from level 1
        self.maxLv = 6  # max number of levels
        self.isLevelGenerated = False  # check the level (map) is generated or not
        self.isPlaying = False  # check the game is actually started (moving) or not
        self.statusStartingTimer = 0  # countdown timer for 'get ready' feature
        self.statusDeadTimer = 0  # countdown timer for dead event
        self.statusFinishTimer = 0  # countdown timer for clear event
        self.statusScore = 0  # score
        self.statusScore1 = 0  # player1 score
        self.statusScore2 = 0  # player1 score
        self.statusRecord = highscore  # record
        self.statusLife = 4  # shared life
        self.rebirthIndex = [(23, 13), (23, 13), (23, 13), (23, 13),
                             (23, 13)]  # relative coord of rebirth location for ghost
        self.randomFlag = randint(1, 5)
        self.gameOverFlag = False


    def run(self):
    # call the next phase of initialization: loading resources
        self.__initResource()
        #print("Record: {}".format(self.statusRecord))
        return self.statusRecord

    def __initResource(self):
        ## read the sprite files
        # all sprites will saved in this dictionary
        self.randomFlag = randint(1, 5)
        self.wSprites = {
            'getready': PhotoImage(file="resources/graphics/get_ready.png"),
            'gameover': PhotoImage(file="resources/graphics/game_over.png"),
            'win': PhotoImage(file="resources/graphics/youwin.png"),
            'wall': PhotoImage(file="resources/graphics/wall{}.png".format(self.randomFlag)),
            'cage': PhotoImage(file="resources/graphics/cage.png"),
            'pellet': PhotoImage(file="resources/graphics/pellet.png"),
            'powerpellet': PhotoImage(file="resources/graphics/powerpoint.png"),
            'fruit0': PhotoImage(file="resources/graphics/fruit-0.png"),
            'fruit1': PhotoImage(file="resources/graphics/fruit-1.png"),
            'fruit2': PhotoImage(file="resources/graphics/fruit-2.png"),
            'lives1': PhotoImage(file="resources/graphics/pacmanR-0.png"),
            'lives2': PhotoImage(file="resources/graphics/pacmanSL-0.png")
        }

        # bind sprites for moving objects
        for i in range(4):
            # pacman: pacman(direction)(index)
            if i == 3:
                pass
            else:
                self.wSprites['pacmanL{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanL-{}.png".format(i))
                self.wSprites['pacmanR{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanR-{}.png".format(i))
                self.wSprites['pacmanU{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanU-{}.png".format(i))
                self.wSprites['pacmanD{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanD-{}.png".format(i))
            # ghosts: ghost(index1)(direction)(index2)
            self.wSprites['ghost{}L1'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-0.png".format(i + 1))
            self.wSprites['ghost{}L2'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-1.png".format(i + 1))
            self.wSprites['ghost{}R1'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-0.png".format(i + 1))
            self.wSprites['ghost{}R2'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-1.png".format(i + 1))
            self.wSprites['ghost{}U1'.format(i + 1)] = PhotoImage(file="resources/graphics/ghost{}-0.png".format(i + 1))
            self.wSprites['ghost{}U2'.format(i + 1)] = PhotoImage(file="resources/graphics/ghost{}-1.png".format(i + 1))
            self.wSprites['ghost{}D1'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-0.png".format(i + 1))
            self.wSprites['ghost{}D2'.format(i + 1)] = PhotoImage(
                file="resources/graphics/ghost{}-1.png".format(i + 1))

        # for player 2
        for i in range(4):
            # pacman2: pacman(direction)(index)
            if i == 3:
                pass
            else:
                self.wSprites['pacmanSL{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanSL-{}.png".format(i))
                self.wSprites['pacmanSR{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanSR-{}.png".format(i))
                self.wSprites['pacmanSU{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanSU-{}.png".format(i))
                self.wSprites['pacmanSD{}'.format(i + 1)] = PhotoImage(
                    file="resources/graphics/pacmanSD-{}.png".format(i))


        for i in range(11):
            self.wSprites['pacmanDeath{}'.format(i + 1)] = PhotoImage(
                file="resources/graphics/pacman_death{}.png".format(i + 1))

        # weak ghost
        self.wSprites['ghostWeak1'] = PhotoImage(
            file="resources/graphics/ghostWeak-0.png")
        self.wSprites['ghostWeak2'] = PhotoImage(
            file="resources/graphics/ghostWeak-1.png")

        self.wSounds = {
            'chomp1': pygame.mixer.Sound(file="resources/audio/click1.wav"),
            'chomp2': pygame.mixer.Sound(file="resources/audio/click4.wav"),
            'eat_power': pygame.mixer.Sound(file="resources/audio/click3.wav"),
            'eat_fruit': pygame.mixer.Sound(file="resources/audio/click2.wav"),
            'eat_ghost': pygame.mixer.Sound(file="resources/audio/eat_ghost.wav")
        }

        # call the next phase of initialization: generate widgets
        self.__initWidgets()

    def __initWidgets(self):
        # initialize widgets for level selection
        # self.wLvLabel = Label(self.root, text="Select the level.")
        # self.wLvEntry = Entry(self.root)
        # self.wLvBtn = Button(self.root, text="Select", command=self.lvSelect, width=5, height=1)

        # initialize widgets for the game
        self.wGameLabelScore = Label(self.root, text=("Current Score: " + str(self.statusScore)))
        self.wGameLabelLife = Label(self.root, text=("Level: {}        Life: ".format(self.currentLv) + str(self.statusLife)))
        self.wGameLabelRecord = Label(self.root, text=("Record: " + str(self.statusRecord)))
        self.wGameCanv = Canvas(width=800, height=600)
        self.wGameCanvLabelGetReady = self.wGameCanv.create_image(405, 327, image=None)
        self.wGameCanvLabelGameOver = self.wGameCanv.create_image(410, 327, image=None)
        self.wGameCanvLabelWin = self.wGameCanv.create_image(400, 300, image=None)
        self.wGameCanvObjects = [[self.wGameCanv.create_image(0, 0, image=None) for j in range(32)] for i in range(48)]
        self.wGameCanvLives = [self.wGameCanv.create_image(0, 0, image=None) for j in range(7)]
        self.wGameCanv.config(background="black")
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0, 0, image=None) for n in
                                       range(6)]  # 0: pacman, 1-4: ghosts, 5: pacman2

        # key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft2)
        self.root.bind('a', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight2)
        self.root.bind('d', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp2)
        self.root.bind('w', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown2)
        self.root.bind('s', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)
        self.root.bind('<Return>', self.inputResponseReturn)

        # execute the game
        # self.root.mainloop()

        # call the next phase of initialization: level initialization
        multiplayermaze.newMaze.randomFlag = randint(1, 2)
        self.__initLevelOnce(self.currentLv)
        self.root.mainloop()

    def __initLevelSelect(self):
        # level selection, showing all relevant widgets
        # self.wLvLabel.pack()
        # self.wLvEntry.pack()
        # self.wLvBtn.pack()

        # execute the game
        self.root.mainloop()

    def lvSelect(self):
        try:
            self.__initLevelOnce(1)

        except ValueError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")

        except FileNotFoundError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")

    def __initLevelOnce(self, level):
        ## this function will be called only once

        self.randomFlag = randint(1, 5)
        self.__initLevel(level)

        # removing level selection features
        # self.wLvLabel.destroy()
        # self.wLvEntry.destroy()
        # self.wLvBtn.destroy()
        # place the canvas and set isPlaying True
        self.wGameCanv.place(x=0, y=30)
        self.wGameLabelScore.place(x=10, y=5)
        self.wGameLabelRecord.place(x=350, y=5)
        self.wGameLabelLife.place(x=680, y=5)

    def __initLevel(self, level):

        self.currentLv = int(level)
        multiplayermaze.newMaze.load_maze(level)  # generate selected/passed level
        #self.wGameCanvObjects = [[self.wGameCanv.create_image(0, 0, image=None) for j in range(32)] for i in range(48)]

        self.wSprites.update({'wall': PhotoImage(file="resources/graphics/wall{}.png".format(self.randomFlag))})
        self.wGameLabelLife.configure(text=("Level: {}        Life: ".format(self.currentLv) + str(self.statusLife)))

        # check the name of the object and bind the sprite, adjust their coordinate
        for j in range(32):
            for i in range(48):

                #print("row: {}, col: {}, name: {}".format(j, i, multiplayermaze.newMaze.levelObjects[i][j].name))
                if multiplayermaze.newMaze.levelObjects[i][j].name == "empty":
                    pass
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['cage'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "pellet":
                    if multiplayermaze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['pellet'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "power":
                    if multiplayermaze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['powerpellet'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "fruit0":
                    if multiplayermaze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit0'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "fruit1":
                    if multiplayermaze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit1'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif multiplayermaze.newMaze.levelObjects[i][j].name == "fruit2":
                    if multiplayermaze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit2'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass

        for i in range(7):
            if i <= self.statusLife and i > 0:
                if i %2 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvLives[i], image=self.wSprites['lives2'],
                                          state='normal')
                elif i %2 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvLives[i], image=self.wSprites['lives1'],
                                          state='normal')
                self.wGameCanv.coords(self.wGameCanvLives[i], 3 + i * 17 + 8, 30 + 32 * 17 + 8)

        # bind the sprite and give it current coord. for pacman
        self.wGameCanv.coords(self.wGameCanvMovingObjects[0],
                              3 + multiplayermaze.newMaze.movingObjectPacman[0].coordinateRel[0] * 17 + 8,
                              30 + multiplayermaze.newMaze.movingObjectPacman[0].coordinateRel[1] * 17 + 8)
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'], state='normal')

        # bind the sprite and give it current coord. for pacman2
        self.wGameCanv.coords(self.wGameCanvMovingObjects[5],
                              3 + multiplayermaze.newMaze.movingObjectPacman[1].coordinateRel[0] * 17 + 8,
                              30 + multiplayermaze.newMaze.movingObjectPacman[1].coordinateRel[1] * 17 + 8)
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSR1'], state='normal')
        multiplayermaze.newMaze.movingObjectPacman[1].dirCurrent = "Right"

        # bind the sprite give them current coord. for ghosts
        for i in range(4):
            if multiplayermaze.newMaze.movingObjectGhosts[i].isActive == True:
                self.wGameCanv.coords(self.wGameCanvMovingObjects[i + 1],
                                      3 + multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[0] * 17 + 8,
                                      30 + multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[1] * 17 + 8)
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[i + 1],
                                          image=self.wSprites['ghost{}L1'.format(i + 1)], state='normal')

        # advance to next phase: get ready!
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/audio/sound_intro.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
        self.isLevelGenerated = True
        self.timerReady = PerpetualTimer(0.55, self.__initLevelStarting)
        self.timerReady.start()

    def inputResponseLeft(self, event):
        multiplayermaze.newMaze.movingObjectPacman[0].dirNext = "Left"

    def inputResponseRight(self, event):
        multiplayermaze.newMaze.movingObjectPacman[0].dirNext = "Right"

    def inputResponseUp(self, event):
        multiplayermaze.newMaze.movingObjectPacman[0].dirNext = "Up"

    def inputResponseDown(self, event):
        multiplayermaze.newMaze.movingObjectPacman[0].dirNext = "Down"

    def inputResponseLeft2(self, event):
        multiplayermaze.newMaze.movingObjectPacman[1].dirNext = "Left"

    def inputResponseRight2(self, event):
        multiplayermaze.newMaze.movingObjectPacman[1].dirNext = "Right"

    def inputResponseUp2(self, event):
        multiplayermaze.newMaze.movingObjectPacman[1].dirNext = "Up"

    def inputResponseDown2(self, event):
        multiplayermaze.newMaze.movingObjectPacman[1].dirNext = "Down"

    def inputResponseEsc(self, event):
        self.timerLoop.stop()
        pygame.mixer.music.stop()
        messagebox.showinfo("Game Over!", "You hit the escape key!\nWill quit after click")
        time.sleep(5)
        self.root.quit()

    def inputResponseReturn(self, event):
        # return to homepage
        if self.gameOverFlag == True:
            self.root.quit()
        else:
            pass

    def __initLevelStarting(self):
        self.statusStartingTimer += 1  # countdown timer for this function

        # bind the sprite for the widget
        self.wGameCanv.itemconfig(self.wGameCanvLabelGetReady, image=self.wSprites['getready'])

        if self.statusStartingTimer < 10:
            # blinking function
            if self.statusStartingTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')

        else:  # after 10 loop, the main game will be started with loopFunction
            self.gameStartingTrigger()

    def gameStartingTrigger(self):
        ## stop to print out 'get ready' and start the game
        self.timerReady.stop()
        self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')
        self.statusStartingTimer = 0
        self.isPlaying = True
        multiplayermaze.newMaze.movingObjectPacman[0].dirNext = "Left"
        multiplayermaze.newMaze.movingObjectPacman[1].dirNext = "Right"

        # ghost sound as music
        pygame.mixer.music.stop()
        self.randomFlagBGM = randint(1, 4)
        pygame.mixer.music.load("resources/audio/bgm{}.wav".format(self.randomFlagBGM+1))
        pygame.mixer.music.play(-1)

        self.timerLoop = PerpetualTimer(0.045, self.loopFunction)
        self.timerLoop.start()

    def loopFunction(self):

        multiplayermaze.newMaze.loopFunction()

        coordGhosts = {}

        for i in range(4):
            coordGhosts['RelG{}'.format(i + 1)] = multiplayermaze.newMaze.movingObjectGhosts[
                i].coordinateRel  # ghosts relative coordinate
            coordGhosts['AbsG{}'.format(i + 1)] = multiplayermaze.newMaze.movingObjectGhosts[
                i].coordinateAbs  # ghosts absolute coordinate

        self.spritePacman(multiplayermaze.newMaze.movingObjectPacman[0].coordinateRel,
                          multiplayermaze.newMaze.movingObjectPacman[0].coordinateAbs, 0)
        self.spritePacman(multiplayermaze.newMaze.movingObjectPacman[1].coordinateRel,
                          multiplayermaze.newMaze.movingObjectPacman[1].coordinateAbs, 1)
        self.spriteGhost(coordGhosts)
        self.encounterEvent(multiplayermaze.newMaze.movingObjectPacman[0].coordinateRel,
                            multiplayermaze.newMaze.movingObjectPacman[0].coordinateAbs, 0)
        self.encounterEvent(multiplayermaze.newMaze.movingObjectPacman[1].coordinateRel,
                            multiplayermaze.newMaze.movingObjectPacman[1].coordinateAbs, 1)

    def spritePacman(self, coordRelP, coordAbsP, pacman_num):
        ## pacman sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        if pacman_num == 0:
            if multiplayermaze.newMaze.movingObjectPacman[0].dirCurrent == "Left":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 17 * 47 + 17,
                                        0)  # notice this will move the sprite 17*27+17 (not 17*27+12) as the sprite will move once again below
                    multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[0] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
                elif coordAbsP[0] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
                elif coordAbsP[0] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
                elif coordAbsP[0] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], -5, 0)


            elif multiplayermaze.newMaze.movingObjectPacman[0].dirCurrent == "Right":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], -(17 * 47 + 17), 0)
                    multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[0] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
                elif coordAbsP[0] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
                elif coordAbsP[0] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
                elif coordAbsP[0] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 5, 0)


            elif multiplayermaze.newMaze.movingObjectPacman[0].dirCurrent == "Up":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 17 * 31 + 17)
                    multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[1] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
                elif coordAbsP[1] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
                elif coordAbsP[1] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
                elif coordAbsP[1] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -5)


            elif multiplayermaze.newMaze.movingObjectPacman[0].dirCurrent == "Down":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -(17 * 31 + 17))
                    multiplayermaze.newMaze.movingObjectPacman[0].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[1] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
                elif coordAbsP[1] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
                elif coordAbsP[1] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
                elif coordAbsP[1] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 5)
            pass

        # pacman2
        else:
            if multiplayermaze.newMaze.movingObjectPacman[1].dirCurrent == "Left":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 17 * 47 + 17,
                                        0)  # notice this will move the sprite 17*27+17 (not 17*27+12) as the sprite will move once again below
                    multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[0] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSL2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], -4, 0)
                elif coordAbsP[0] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSL3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], -4, 0)
                elif coordAbsP[0] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSL2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], -4, 0)
                elif coordAbsP[0] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSL1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], -5, 0)


            elif multiplayermaze.newMaze.movingObjectPacman[1].dirCurrent == "Right":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], -(17 * 47 + 17), 0)
                    multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[0] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSR2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 4, 0)
                elif coordAbsP[0] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSR3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 4, 0)
                elif coordAbsP[0] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSR2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 4, 0)
                elif coordAbsP[0] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSR1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 5, 0)


            elif multiplayermaze.newMaze.movingObjectPacman[1].dirCurrent == "Up":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, 17 * 31 + 17)
                    multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[1] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSU2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, -4)
                elif coordAbsP[1] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSU3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, -4)
                elif coordAbsP[1] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSU2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, -4)
                elif coordAbsP[1] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSU1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, -5)


            elif multiplayermaze.newMaze.movingObjectPacman[1].dirCurrent == "Down":

                # check the object passed multiplayermaze edges
                if multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed == True:
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, -(17 * 31 + 17))
                    multiplayermaze.newMaze.movingObjectPacman[1].dirEdgePassed = False
                else:
                    pass

                if coordAbsP[1] % 4 == 0:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSD2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, 4)
                elif coordAbsP[1] % 4 == 1:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSD3'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, 4)
                elif coordAbsP[1] % 4 == 2:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSD2'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, 4)
                elif coordAbsP[1] % 4 == 3:
                    self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5], image=self.wSprites['pacmanSD1'])
                    self.wGameCanv.move(self.wGameCanvMovingObjects[5], 0, 5)
            pass


    def spriteGhost(self, coordGhosts):
        ## ghosts sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        for ghostNo in range(4):
            if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].isActive == True:  # only active ghost will be shown
                # normal state
                if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].weakTimer == 0:
                    if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Left":

                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 17 * 47 + 17, 0)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}L1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}L1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}L2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}L2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -5, 0)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Right":

                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -(17 * 47 + 17), 0)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}R1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}R1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}R2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}R2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 5, 0)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Up":

                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 17 * 31 + 17)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}U1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}U1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}U2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}U2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -5)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Down":

                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -(17 * 31 + 17))
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}D1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}D1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}D2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghost{}D2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 5)

                # weak state
                else:
                    if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Left":
                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 17 * 47 + 17, 0)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -5, 0)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Right":
                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -(17 * 47 + 17), 0)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 4, 0)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][0] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 5, 0)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Up":
                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 17 * 31 + 17)
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -5)


                    elif multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Down":
                        # check the object passed multiplayermaze edges
                        if multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -(17 * 31 + 17))
                            multiplayermaze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
                        else:
                            pass

                        if coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 0:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 1:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak1'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 2:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 4)
                        elif coordGhosts['AbsG{}'.format(ghostNo + 1)][1] % 4 == 3:
                            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo + 1],
                                                      image=self.wSprites['ghostWeak2'.format(ghostNo + 1)])
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 5)

                    multiplayermaze.newMaze.movingObjectGhosts[ghostNo].weakTimer -= 1
            else:  # inactive ghost
                pass

    def encounterEvent(self, coordRelP, coordAbsP, pacman_num):
        ## encounter features

        encounterMov = multiplayermaze.newMaze.encounterMoving(coordAbsP[0],
                                                    coordAbsP[1])  # call encounterEvent for moving objects

        if encounterMov == 'dead':
            self.encounterEventDead()
        else:
            for i in range(4):
                if encounterMov == 'eat{}'.format(i):
                    # play the sound
                    self.wSounds['eat_ghost'].play(loops=0)

                    # get plenty of score
                    self.statusScore += 100  # adjust the score
                    if pacman_num == 0:
                        self.statusScore1 += 100
                    elif pacman_num == 1:
                        self.statusScore2 += 100
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=("Total Score: {}   P1 Score: {}   P2 Score: {}".format(self.statusScore, self.statusScore1, self.statusScore2)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(text=("New Record: " + str(self.statusRecord)))  # showing on the board

                    # reset the ghost
                    delta_y = self.rebirthIndex[self.currentLv - 1][1] - \
                              multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[1]
                    delta_x = self.rebirthIndex[self.currentLv - 1][0] - \
                              multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[0]
                    # adjust current coordinate
                    multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[0] = self.rebirthIndex[self.currentLv - 1][0]
                    multiplayermaze.newMaze.movingObjectGhosts[i].coordinateRel[1] = self.rebirthIndex[self.currentLv - 1][1]
                    multiplayermaze.newMaze.movingObjectGhosts[i].coordinateAbs[0] = self.rebirthIndex[self.currentLv - 1][0]*4
                    multiplayermaze.newMaze.movingObjectGhosts[i].coordinateAbs[1] = self.rebirthIndex[self.currentLv - 1][1]*4

                    self.wGameCanv.coords(self.wGameCanvMovingObjects[i+1], 3 + self.rebirthIndex[self.currentLv - 1][0] * 17 + 8, 30 + self.rebirthIndex[self.currentLv - 1][1] * 17 + 8)
                    multiplayermaze.newMaze.movingObjectGhosts[i].weakTimer = 5

        # check the object reaches grid coordinate
        if coordAbsP[0] % 4 == 0 and coordAbsP[1] % 4 == 0:
            encounterFix = multiplayermaze.newMaze.encounterFixed(coordRelP[0], coordRelP[1])  # call encounterEvent function

            if encounterFix == "empty":
                pass
            elif encounterFix == "pellet":
                if multiplayermaze.newMaze.levelObjects[coordRelP[0]][
                    coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    multiplayermaze.newMaze.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True  # destroy the pellet
                    self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                 state='hidden')  # remove from the canvas

                    # play the sound (wa, ka, wa, ka, ...)
                    if self.statusScore % 20 == 0:
                        self.wSounds['chomp1'].play(loops=0)
                    else:
                        self.wSounds['chomp2'].play(loops=0)

                    self.statusScore += 10
                    if pacman_num == 0:
                        self.statusScore1 += 10
                    elif pacman_num == 1:
                        self.statusScore2 += 10
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=(
                        "Total Score: {}   P1 Score: {}   P2 Score: {}".format(self.statusScore, self.statusScore1,
                                                                             self.statusScore2)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(
                            text=("New Record: " + str(self.statusRecord)))  # showing on the board
                    multiplayermaze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                    if multiplayermaze.newMaze.levelPelletRemaining == 0:
                        self.encounterEventLevelClear()  # level clear
                    else:
                        pass
                else:  # the pellet is already taken
                    pass

            elif encounterFix == "power":
                if multiplayermaze.newMaze.levelObjects[coordRelP[0]][
                    coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    multiplayermaze.newMaze.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True  # destroy the pellet
                    self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                 state='hidden')  # remove from the canvas

                    # play the sound
                    self.wSounds['eat_power'].play(loops=0)

                    self.statusScore += 50  # adjust the score
                    if pacman_num == 0:
                        self.statusScore1 += 50
                    elif pacman_num == 1:
                        self.statusScore2 += 50
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=(
                        "Total Score: {}  P1 Score: {}  P2 Score: {}".format(self.statusScore, self.statusScore1,
                                                                             self.statusScore2)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(
                            text=("New Record: " + str(self.statusRecord)))  # showing on the board
                    multiplayermaze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                    if multiplayermaze.newMaze.levelPelletRemaining == 0:
                        self.encounterEventLevelClear()  # level clear
                    else:
                        pass

                    # ghosts become weak for a certain time
                    for i in range(4):
                        if multiplayermaze.newMaze.movingObjectGhosts[i].isActive == True:
                            multiplayermaze.newMaze.movingObjectGhosts[i].weakTimer = 200

                else:  # the pellet is already taken
                    pass

            else:
                for i in range(3):
                    if encounterFix == "fruit{}".format(i):
                        if multiplayermaze.newMaze.levelObjects[coordRelP[0]][
                            coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                            multiplayermaze.newMaze.levelObjects[coordRelP[0]][
                                coordRelP[1]].isDestroyed = True  # destroy the pellet
                            self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                         state='hidden')  # remove from the canvas

                            # play the sound
                            self.wSounds['eat_fruit'].play(loops=0)

                            self.statusScore += 50 + i * 10  # adjust the score
                            if pacman_num == 0:
                                self.statusScore1 += 50+i*10
                            elif pacman_num == 1:
                                self.statusScore2 += 50+i*10
                            if self.statusScore > self.statusRecord:
                                self.statusRecord = self.statusScore
                            self.wGameLabelScore.configure(text=(
                                "Total Score: {}   P1 Score: {}   P2 Score: {}".format(self.statusScore,
                                                                                     self.statusScore1,
                                                                                     self.statusScore2)))  # showing on the board
                            if self.statusRecord == self.statusScore:
                                self.wGameLabelRecord.configure(
                                    text=("New Record: " + str(self.statusRecord)))  # showing on the board
                            # multiplayermaze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                            if multiplayermaze.newMaze.levelPelletRemaining == 0:
                                self.encounterEventLevelClear()  # level clear
                            else:
                                pass
                        else:  # the pellet is already taken
                            pass

        else:  # pacman is not on grid coordinate
            pass

    def encounterEventLevelClear(self):
        # pause the game
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/audio/level_clear.wav")
        pygame.mixer.music.play(loops=0, start=0.0)
        self.timerLoop.stop()
        self.isPlaying = False

        for i in range(6):  # hide the moving objects' sprite
            self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[i], state='hidden')

        self.timerClear = PerpetualTimer(0.4, self.encounterEventLevelClearLoop)
        self.timerClear.start()

    def encounterEventLevelClearLoop(self):
        self.statusFinishTimer += 1  # countdown timer for this function

        if self.statusFinishTimer < 9:
            # wall blinking function
            if self.statusFinishTimer % 2 == 1:
                self.wSprites.update({'wall': PhotoImage(file="resources/graphics/wall7.png")})
                for j in range(32):
                    for i in range(48):
                        if multiplayermaze.newMaze.levelObjects[i][j].name == "wall":
                            self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                        else:
                            pass
            else:
                self.wSprites.update({'wall': PhotoImage(file="resources/graphics/wall1.png")})
                for j in range(32):
                    for i in range(48):
                        if multiplayermaze.newMaze.levelObjects[i][j].name == "wall":
                            self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                        else:
                            pass

        else:  # after 11 loop, the level clear process will be continued
            self.encounterEventLevelClearFinish()

    def encounterEventLevelClearFinish(self):
        self.timerClear.stop()
        self.statusFinishTimer = 0

        # reset all values and hide the sprite (or level generate process will be shown)
        for j in range(32):
            for i in range(48):
                multiplayermaze.newMaze.levelObjects[i][j].reset('')
                self.wGameCanv.itemconfigure(self.wGameCanvObjects[i][j], state='hidden')

        multiplayermaze.newMaze.movingObjectPacman[0].reset('Pacman')
        multiplayermaze.newMaze.movingObjectPacman[1].reset('Pacman')

        for n in range(4):
            multiplayermaze.newMaze.movingObjectGhosts[n].reset('Ghost')

        self.currentLv += 1
        if self.currentLv > self.maxLv:
            # win finally
            self.statusWinTimer = 0
            self.winTimer = PerpetualTimer(0.55, self.encounterEventWin)
            self.winTimer.start()
        else:
            self.isLevelGenerated = False
            self.randomFlag = randint(1, 5)
            self.wGameCanvObjects = [[self.wGameCanv.create_image(0, 0, image=None) for j in range(32)] for i in
                                     range(48)]
            multiplayermaze.newMaze.randomFlag = randint(1, 2)
            self.__initLevel(self.currentLv)

    def encounterEventDead(self):

        self.wGameCanv.itemconfig(self.wGameCanvLives[self.statusLife], image=self.wSprites['lives1'],
                                  state='hidden')
        self.statusLife -= 1  # subtract remaining life

        if self.statusLife >= 0:
            self.wGameLabelLife.configure(text=("Level: {}        Life: ".format(self.currentLv) + str(self.statusLife)))  # showing on the board
        else:  # prevent showing minus life (will be game over anyway)
            pass

        # pause the game
        self.isPlaying = False
        pygame.mixer.music.stop()
        self.timerLoop.stop()

        # call the death loop
        self.timerDeath = PerpetualTimer(0.10, self.encounterEventDeadLoop)
        self.timerDeath.start()

    def encounterEventDeadLoop(self):

        self.statusDeadTimer += 1  # countdown timer for this function

        if self.statusDeadTimer <= 5:  # waiting for a while
            pass

        elif self.statusDeadTimer == 6:
            # sound effect
            pygame.mixer.music.load("resources/audio/lose2.wav")
            pygame.mixer.music.play(loops=0, start=0.0)
            for i in range(4):  # hide the ghost sprite and initialize their status
                self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[i + 1], state='hidden')
                multiplayermaze.newMaze.movingObjectGhosts[i].isActive = False
                multiplayermaze.newMaze.movingObjectGhosts[i].isCaged = True

        elif 6 < self.statusDeadTimer <= 17:  # animate the death sprite
            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0],
                                      image=self.wSprites['pacmanDeath{}'.format(self.statusDeadTimer - 6)])
            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[5],
                                      image=self.wSprites['pacmanDeath{}'.format(self.statusDeadTimer - 6)])

        elif self.statusDeadTimer == 18:  # blink!
            self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[0], state='hidden')

        elif 18 < self.statusDeadTimer <= 22:  # waiting for a while
            pass

        else:
            self.encounterEventDeadRestart()

    def encounterEventDeadRestart(self):
        ## stop the death event and restart the game
        if self.statusLife >= 0:
            self.statusDeadTimer = 0  # reset the countdown timer
            self.timerDeath.stop()  # stopping the timer for death event
            self.isPlaying = False  # isPlaying flag check
            multiplayermaze.newMaze.levelPelletRemaining = 0  # Pellet count reset (will be re-counted in __initLevel)
            self.__initLevel(self.currentLv)

        else:  # game over
            self.statusDeadTimer = 0
            self.timerDeath.stop()
            self.gameOverTimer = PerpetualTimer(0.55, self.encounterEventDeadGameOver)
            self.gameOverTimer.start()

    def encounterEventDeadGameOver(self):
        self.statusDeadTimer += 1
        self.wGameCanv.itemconfig(self.wGameCanvLabelGameOver, image=self.wSprites['gameover'])

        if self.statusDeadTimer < 8:
            # blinking function
            if self.statusDeadTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGameOver, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGameOver, state='hidden')

        else:  # after 8 loop, the game is completely finished
            self.gameOverTimer.stop()
            self.gameOverFlag = True

    def encounterEventWin(self):
        self.statusWinTimer += 1
        self.wGameCanv.itemconfig(self.wGameCanvLabelWin, image=self.wSprites['win'])

        if self.statusWinTimer < 8:
            # blinking function
            if self.statusWinTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelWin, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelWin, state='hidden')

        else:  # after 8 loop, the game is completely finished
            self.winTimer.stop()
            self.gameOverFlag = True


class PerpetualTimer(object):

    def __init__(self, interval, function, *args):
        self.thread = None
        self.interval = interval
        self.function = function
        self.args = args
        self.isRunning = False

    def _handleFunction(self):
        self.isRunning = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.isRunning:
            self.thread = Timer(self.interval, self._handleFunction)
            self.thread.start()
            self.isRunning = True

    def stop(self):
        self.thread.cancel()
        self.isRunning = False


# initialize pygame for sound effects
pygame.mixer.init(22050, -16, 2, 64)
pygame.init()

# start the game
newGame = Game(500)
print("Game over! Your record: {}".format(newGame.run()))
print("Your score: {}".format(newGame.statusScore))
