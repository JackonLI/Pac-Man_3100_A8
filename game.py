from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END, Canvas
from threading import Timer
from random import *
import maze
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
        self.statusRecord = highscore  # record
        self.statusLife = 3  # life
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
            'lives': PhotoImage(file="resources/graphics/pacmanR-0.png")
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
        self.wGameCanvLives = [self.wGameCanv.create_image(0, 0, image=None) for j in range(5)]
        self.wGameCanv.config(background="black")
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0, 0, image=None) for n in
                                       range(5)]  # 0: pacman, 1-4: ghosts

        # key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft)
        self.root.bind('a', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight)
        self.root.bind('d', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp)
        self.root.bind('w', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown)
        self.root.bind('s', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)
        self.root.bind('<Return>', self.inputResponseReturn)

        # execute the game
        # self.root.mainloop()

        # call the next phase of initialization: level initialization
        maze.newMaze.randomFlag = randint(1, 2)
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
        maze.newMaze.load_maze(level)  # generate selected/passed level
        #self.wGameCanvObjects = [[self.wGameCanv.create_image(0, 0, image=None) for j in range(32)] for i in range(48)]

        self.wSprites.update({'wall': PhotoImage(file="resources/graphics/wall{}.png".format(self.randomFlag))})
        self.wGameLabelLife.configure(text=("Level: {}        Life: ".format(self.currentLv) + str(self.statusLife)))

        # check the name of the object and bind the sprite, adjust their coordinate
        for j in range(32):
            for i in range(48):

                #print("row: {}, col: {}, name: {}".format(j, i, maze.newMaze.levelObjects[i][j].name))
                if maze.newMaze.levelObjects[i][j].name == "empty":
                    pass
                elif maze.newMaze.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                elif maze.newMaze.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['cage'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                elif maze.newMaze.levelObjects[i][j].name == "pellet":
                    if maze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['pellet'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif maze.newMaze.levelObjects[i][j].name == "power":
                    if maze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['powerpellet'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif maze.newMaze.levelObjects[i][j].name == "fruit0":
                    if maze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit0'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif maze.newMaze.levelObjects[i][j].name == "fruit1":
                    if maze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit1'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass
                elif maze.newMaze.levelObjects[i][j].name == "fruit2":
                    if maze.newMaze.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['fruit2'],
                                                  state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3 + i * 17 + 8, 30 + j * 17 + 8)
                    else:
                        pass

        for i in range(5):
            if i <= self.statusLife and i > 0:
                self.wGameCanv.itemconfig(self.wGameCanvLives[i], image=self.wSprites['lives'],
                                          state='normal')
                self.wGameCanv.coords(self.wGameCanvLives[i], 3 + i * 17 + 8, 30 + 32 * 17 + 8)

        # bind the sprite and give it current coord. for pacman
        self.wGameCanv.coords(self.wGameCanvMovingObjects[0],
                              3 + maze.newMaze.movingObjectPacman.coordinateRel[0] * 17 + 8,
                              30 + maze.newMaze.movingObjectPacman.coordinateRel[1] * 17 + 8)
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'], state='normal')

        # bind the sprite give them current coord. for ghosts
        for i in range(4):
            if maze.newMaze.movingObjectGhosts[i].isActive == True:
                self.wGameCanv.coords(self.wGameCanvMovingObjects[i + 1],
                                      3 + maze.newMaze.movingObjectGhosts[i].coordinateRel[0] * 17 + 8,
                                      30 + maze.newMaze.movingObjectGhosts[i].coordinateRel[1] * 17 + 8)
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
        maze.newMaze.movingObjectPacman.dirNext = "Left"

    def inputResponseRight(self, event):
        maze.newMaze.movingObjectPacman.dirNext = "Right"

    def inputResponseUp(self, event):
        maze.newMaze.movingObjectPacman.dirNext = "Up"

    def inputResponseDown(self, event):
        maze.newMaze.movingObjectPacman.dirNext = "Down"

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
        maze.newMaze.movingObjectPacman.dirNext = "Left"

        # ghost sound as music
        pygame.mixer.music.stop()
        self.randomFlagBGM = randint(1, 4)
        pygame.mixer.music.load("resources/audio/bgm{}.wav".format(self.randomFlagBGM+1))
        pygame.mixer.music.play(-1)

        self.timerLoop = PerpetualTimer(0.045, self.loopFunction)
        self.timerLoop.start()

    def loopFunction(self):

        maze.newMaze.loopFunction()

        coordGhosts = {}

        for i in range(4):
            coordGhosts['RelG{}'.format(i + 1)] = maze.newMaze.movingObjectGhosts[
                i].coordinateRel  # ghosts relative coordinate
            coordGhosts['AbsG{}'.format(i + 1)] = maze.newMaze.movingObjectGhosts[
                i].coordinateAbs  # ghosts absolute coordinate

        self.spritePacman(maze.newMaze.movingObjectPacman.coordinateRel,
                          maze.newMaze.movingObjectPacman.coordinateAbs)
        self.spriteGhost(coordGhosts)
        self.encounterEvent(maze.newMaze.movingObjectPacman.coordinateRel,
                            maze.newMaze.movingObjectPacman.coordinateAbs)

    def spritePacman(self, coordRelP, coordAbsP):
        ## pacman sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        if maze.newMaze.movingObjectPacman.dirCurrent == "Left":

            # check the object passed maze edges
            if maze.newMaze.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 17 * 47 + 17,
                                    0)  # notice this will move the sprite 17*27+17 (not 17*27+12) as the sprite will move once again below
                maze.newMaze.movingObjectPacman.dirEdgePassed = False
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


        elif maze.newMaze.movingObjectPacman.dirCurrent == "Right":

            # check the object passed maze edges
            if maze.newMaze.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -(17 * 47 + 17), 0)
                maze.newMaze.movingObjectPacman.dirEdgePassed = False
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


        elif maze.newMaze.movingObjectPacman.dirCurrent == "Up":

            # check the object passed maze edges
            if maze.newMaze.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 17 * 31 + 17)
                maze.newMaze.movingObjectPacman.dirEdgePassed = False
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


        elif maze.newMaze.movingObjectPacman.dirCurrent == "Down":

            # check the object passed maze edges
            if maze.newMaze.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -(17 * 31 + 17))
                maze.newMaze.movingObjectPacman.dirEdgePassed = False
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

    def spriteGhost(self, coordGhosts):
        ## ghosts sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        for ghostNo in range(4):
            if maze.newMaze.movingObjectGhosts[ghostNo].isActive == True:  # only active ghost will be shown
                # normal state
                if maze.newMaze.movingObjectGhosts[ghostNo].weakTimer == 0:
                    if maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Left":

                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 17 * 47 + 17, 0)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Right":

                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -(17 * 47 + 17), 0)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Up":

                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 17 * 31 + 17)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Down":

                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -(17 * 31 + 17))
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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
                    if maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Left":
                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 17 * 47 + 17, 0)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Right":
                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], -(17 * 47 + 17), 0)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Up":
                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, 17 * 31 + 17)
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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


                    elif maze.newMaze.movingObjectGhosts[ghostNo].dirCurrent == "Down":
                        # check the object passed maze edges
                        if maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                            self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo + 1], 0, -(17 * 31 + 17))
                            maze.newMaze.movingObjectGhosts[ghostNo].dirEdgePassed = False
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

                    maze.newMaze.movingObjectGhosts[ghostNo].weakTimer -= 1
            else:  # inactive ghost
                pass

    def encounterEvent(self, coordRelP, coordAbsP):
        ## encounter features

        encounterMov = maze.newMaze.encounterMoving(coordAbsP[0],
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
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(text=("New Record: " + str(self.statusRecord)))  # showing on the board

                    # reset the ghost
                    delta_y = self.rebirthIndex[self.currentLv - 1][1] - \
                              maze.newMaze.movingObjectGhosts[i].coordinateRel[1]
                    delta_x = self.rebirthIndex[self.currentLv - 1][0] - \
                              maze.newMaze.movingObjectGhosts[i].coordinateRel[0]
                    # adjust current coordinate
                    maze.newMaze.movingObjectGhosts[i].coordinateRel[0] = self.rebirthIndex[self.currentLv - 1][0]
                    maze.newMaze.movingObjectGhosts[i].coordinateRel[1] = self.rebirthIndex[self.currentLv - 1][1]
                    maze.newMaze.movingObjectGhosts[i].coordinateAbs[0] = self.rebirthIndex[self.currentLv - 1][0]*4
                    maze.newMaze.movingObjectGhosts[i].coordinateAbs[1] = self.rebirthIndex[self.currentLv - 1][1]*4

                    self.wGameCanv.coords(self.wGameCanvMovingObjects[i+1], 3 + self.rebirthIndex[self.currentLv - 1][0] * 17 + 8, 30 + self.rebirthIndex[self.currentLv - 1][1] * 17 + 8)
                    maze.newMaze.movingObjectGhosts[i].weakTimer = 5

        # check the object reaches grid coordinate
        if coordAbsP[0] % 4 == 0 and coordAbsP[1] % 4 == 0:
            encounterFix = maze.newMaze.encounterFixed(coordRelP[0], coordRelP[1])  # call encounterEvent function

            if encounterFix == "empty":
                pass
            elif encounterFix == "pellet":
                if maze.newMaze.levelObjects[coordRelP[0]][
                    coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    maze.newMaze.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True  # destroy the pellet
                    self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                 state='hidden')  # remove from the canvas

                    # play the sound (wa, ka, wa, ka, ...)
                    if self.statusScore % 20 == 0:
                        self.wSounds['chomp1'].play(loops=0)
                    else:
                        self.wSounds['chomp2'].play(loops=0)

                    self.statusScore += 10  # adjust the score
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(
                            text=("New Record: " + str(self.statusRecord)))  # showing on the board
                    maze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                    if maze.newMaze.levelPelletRemaining == 0:
                        self.encounterEventLevelClear()  # level clear
                    else:
                        pass
                else:  # the pellet is already taken
                    pass

            elif encounterFix == "power":
                if maze.newMaze.levelObjects[coordRelP[0]][
                    coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    maze.newMaze.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True  # destroy the pellet
                    self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                 state='hidden')  # remove from the canvas

                    # play the sound
                    self.wSounds['eat_power'].play(loops=0)

                    self.statusScore += 50  # adjust the score
                    if self.statusScore > self.statusRecord:
                        self.statusRecord = self.statusScore
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore)))  # showing on the board
                    if self.statusRecord == self.statusScore:
                        self.wGameLabelRecord.configure(
                            text=("New Record: " + str(self.statusRecord)))  # showing on the board
                    maze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                    if maze.newMaze.levelPelletRemaining == 0:
                        self.encounterEventLevelClear()  # level clear
                    else:
                        pass

                    # ghosts become weak for a certain time
                    for i in range(4):
                        if maze.newMaze.movingObjectGhosts[i].isActive == True:
                            maze.newMaze.movingObjectGhosts[i].weakTimer = 200

                else:  # the pellet is already taken
                    pass

            else:
                for i in range(3):
                    if encounterFix == "fruit{}".format(i):
                        if maze.newMaze.levelObjects[coordRelP[0]][
                            coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                            maze.newMaze.levelObjects[coordRelP[0]][
                                coordRelP[1]].isDestroyed = True  # destroy the pellet
                            self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]],
                                                         state='hidden')  # remove from the canvas

                            # play the sound
                            self.wSounds['eat_fruit'].play(loops=0)

                            self.statusScore += 50 + i * 10  # adjust the score
                            if self.statusScore > self.statusRecord:
                                self.statusRecord = self.statusScore
                            self.wGameLabelScore.configure(
                                text=("Score: " + str(self.statusScore)))  # showing on the board
                            if self.statusRecord == self.statusScore:
                                self.wGameLabelRecord.configure(
                                    text=("New Record: " + str(self.statusRecord)))  # showing on the board
                            # maze.newMaze.levelPelletRemaining -= 1  # adjust the remaining pellet numbers

                            if maze.newMaze.levelPelletRemaining == 0:
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

        for i in range(5):  # hide the moving objects' sprite
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
                        if maze.newMaze.levelObjects[i][j].name == "wall":
                            self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                        else:
                            pass
            else:
                self.wSprites.update({'wall': PhotoImage(file="resources/graphics/wall1.png")})
                for j in range(32):
                    for i in range(48):
                        if maze.newMaze.levelObjects[i][j].name == "wall":
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
                maze.newMaze.levelObjects[i][j].reset('')
                self.wGameCanv.itemconfigure(self.wGameCanvObjects[i][j], state='hidden')

        maze.newMaze.movingObjectPacman.reset('Pacman')

        for n in range(4):
            maze.newMaze.movingObjectGhosts[n].reset('Ghost')

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
            maze.newMaze.randomFlag = randint(1, 2)
            self.__initLevel(self.currentLv)

    def encounterEventDead(self):

        self.wGameCanv.itemconfig(self.wGameCanvLives[self.statusLife], image=self.wSprites['lives'],
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
                maze.newMaze.movingObjectGhosts[i].isActive = False
                maze.newMaze.movingObjectGhosts[i].isCaged = True

        elif 6 < self.statusDeadTimer <= 17:  # animate the death sprite
            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0],
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
            maze.newMaze.levelPelletRemaining = 0  # Pellet count reset (will be re-counted in __initLevel)
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
