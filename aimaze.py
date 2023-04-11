import os
from random import randint
import math
from vector import Vector2

class Maze(object):

    def __init__(self):
        #self.path: str = mazePath
        self.levelPelletRemaining = 0
        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(48)]
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(5)]
        self.movingObjectAI = movingObject("AI")
        self.levelObjectNamesBlocker = ["wall", "cage"]
        self.levelObjectNamesPassable = ["empty", "pellet", "power", "fruit0", "fruit1", "fruit2"]  # add in the future


    def load_maze(self, level):
        #if not self.path:
            #return
        pathCurrentDir = os.path.dirname(__file__)
        pathRelDir = "./resources/maze/level{}.txt".format(level)
        pathAbsDir = os.path.join(pathCurrentDir, pathRelDir)

        levelFile = open(pathAbsDir, encoding="utf-8")
        levelLineNo = 0

        for levelLine in levelFile.readlines():

            levelLineSplit = list(levelLine)  # split levelLine into characters

            # generate level objects
            for i in range(48):

                if levelLineSplit[i] == "_":  # passage
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":  # wall
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":  # ghost spawn point
                    self.levelObjects[i][levelLineNo].name = "cage"


                elif levelLineSplit[i] == ".":  # score pellet
                    self.levelObjects[i][levelLineNo].name = "pellet"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "*":  # power pellet
                    self.levelObjects[i][levelLineNo].name = "power"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "0":  # fruit, future we can have multiple fruits, so here can extend by 0, 1, 2, ...
                    self.levelObjects[i][levelLineNo].name = "fruit0"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        #self.levelPelletRemaining += 1
                        pass
                    else:
                        pass

                elif levelLineSplit[i] == "1":  # fruit, future we can have multiple fruits, so here can extend by 0, 1, 2, ...
                    self.levelObjects[i][levelLineNo].name = "fruit1"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        #self.levelPelletRemaining += 1
                        pass
                    else:
                        pass

                elif levelLineSplit[i] == "2":  # fruit, future we can have multiple fruits, so here can extend by 0, 1, 2, ...
                    self.levelObjects[i][levelLineNo].name = "fruit2"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        #self.levelPelletRemaining += 1
                        pass
                    else:
                        pass


                elif levelLineSplit[i] == "@":  # pacman
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # give the starting coordinate
                    self.movingObjectPacman.isActive = True
                    self.movingObjectPacman.isCaged = False
                    self.movingObjectPacman.coordinateRel[0] = i
                    self.movingObjectPacman.coordinateRel[1] = levelLineNo
                    self.movingObjectPacman.coordinateAbs[0] = i * 4
                    self.movingObjectPacman.coordinateAbs[1] = levelLineNo * 4


                elif levelLineSplit[i] == "&":  # free ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].isCaged = False
                            self.movingObjectGhosts[n].weakTimer = 0
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break  # break current loop (with generator 'n')


                elif levelLineSplit[i] == "%":  # caged ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].weakTimer = 0
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break  # break current loop (with generator 'n')

            levelLineNo += 1  # indicate which line we are

        levelFile.close()

    def encounterFixed(self, x, y):  # rel coord.
        return self.levelObjects[x][y].name

    def encounterMoving(self, x, y):  # abs coord.

        result = "alive"  # default

        for i in range(4):  # check if pacman encountered ghost
            m = self.movingObjectGhosts[i].coordinateAbs[0]
            n = self.movingObjectGhosts[i].coordinateAbs[1]

            if self.movingObjectGhosts[i].isActive == True and self.movingObjectGhosts[i].isCaged == False:
                if (m - 3 < x < m + 3) and (
                        n - 3 < y < n + 3):  # check x coord. and y coord. parallelly, this is little bit benign determine (we can use +-4)
                    if self.movingObjectGhosts[i].weakTimer == 0:
                        result = "dead"
                    else:
                        result = "eat{}".format(i)
                else:
                    pass
            else:
                pass

        return result

    def loopFunction(self):
        self.movingObjectPacman.dirNext = self.movingObjectPacman.MoveNextAI(self, self.movingObjectPacman.dirCurrent)
        self.movingObjectPacman.MoveNext(self)
        self.movingObjectPacman.MoveCurrent(self)

        if self.movingObjectGhosts[4].isActive == True:
            self.movingObjectGhosts[4].dirNext = self.movingObjectGhosts[4].MoveNextAI(self,self.movingObjectGhosts[4].dirCurrent)
            self.movingObjectGhosts[4].MoveNext(self)
            self.movingObjectGhosts[4].MoveCurrent(self)

        else:
            pass
        for i in range(4):
            if self.movingObjectGhosts[i].isActive == True:
                self.movingObjectGhosts[i].dirNext = self.movingObjectGhosts[i].MoveNextGhost(self,
                                                                                              self.movingObjectGhosts[
                                                                                                  i].dirCurrent)
                self.movingObjectGhosts[i].MoveNext(self)
                self.movingObjectGhosts[i].MoveCurrent(self)

            else:
                pass


class levelObject(object):

    def __init__(self, name):
        self.reset(name)

    def reset(self, name):
        self.name = name
        self.isDestroyed = False


# The following needs to be rewritten here for reference only
class movingObject(object):

    def __init__(self, name):
        self.reset(name)

    def reset(self, name):
        self.name = name
        self.isActive = False  # check this object is an active ghost (not used for pacman)
        self.isCaged = True  # check this object is caged (only for ghost)
        self.dirCurrent = "Left"  # current direction, if cannot move w/ dirNext, the object will proceed this direction
        self.dirNext = "Left"  # the object will move this direction if it can
        self.dirOpposite = "Right"  # opposite direction to current direction, used for ghost movement determine
        self.dirEdgePassed = False  # check the object passed one of field edges
        self.coordinateRel = [0, 0]  # Relative Coordinate, check can the object move given direction
        self.coordinateAbs = [0, 0]  # Absolute Coordinate, use for widget(image) and object encounters
        self.weakTimer = 0  #Timer for weak ghost

    def MoveNextAI(self,Maze,dirCur):
        # this function will determine AI's direction
        # if ghost reaches a grid coordinate, this will check all directions from the ghost's current location
        # Use MiniMax algorithm
        # we should get DOF here and will determine how we manage ghost's direction
        # DOF == 1 ... opposite direction
        # DOF == 2 ... current direction
        # DOF == 3 ... choose a direction
        # DOF == 4 ... choose a direction
        if self.isCaged == True:  # if ghost is caged, prevent the movement
            pass

        elif self.coordinateAbs[0] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        else:
            dirIndex = ['Left', 'Right', 'Up', 'Down']  # [0]: Left, [1]: Right, [2]: Up, [3]: Down
            dirAvailable = []
            dirDOF = 0

            # find the opposite direction
            if dirCur == 'Left':
                self.dirOpposite = 'Right'
            elif dirCur == 'Right':
                self.dirOpposite = 'Left'
            elif dirCur == 'Up':
                self.dirOpposite = 'Down'
            elif dirCur == 'Down':
                self.dirOpposite = 'Up'
            else:  # dirCur == 'Stop'
                pass

            # checking all directions
            try:
                for i in range(4):

                    if i == 0:
                        nextObject = Maze.levelObjects[self.coordinateRel[0] - 1][
                            self.coordinateRel[1]]  # levelObject on the left
                    elif i == 1:
                        nextObject = Maze.levelObjects[self.coordinateRel[0] + 1][
                            self.coordinateRel[1]]  # levelObject on the right
                    elif i == 2:
                        nextObject = Maze.levelObjects[self.coordinateRel[0]][
                            self.coordinateRel[1] - 1]  # levelObject on the up
                    elif i == 3:
                        nextObject = Maze.levelObjects[self.coordinateRel[0]][
                            self.coordinateRel[1] + 1]  # levelObject on the down

                    if nextObject.name in Maze.levelObjectNamesPassable:
                        dirDOF += 1
                        dirAvailable.append(dirIndex[i])  # append available direction to the list
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass


            except IndexError:  # in case of edge teleport
                dirDOF = 2
                dirAvailable.append(dirCur)

            if Maze.movingObjectGhosts[0].weakTimer <= 20:  # Ghost Not weak
                try:
                    if dirDOF == 1:  # to opposite direction, in this case, dirAvailable only have one item (which is opposite dir)
                        return dirAvailable[
                            0]  # this might not use dirOpp as if the object is stopped, dirOpp is not binded properly


                    elif dirDOF == 2:  # advance toward current direction
                        if dirCur in dirAvailable:  # straight
                            return dirCur
                        elif dirCur == 'Stop':  # somehow this object stopped at straight way
                            return dirAvailable[0]
                        else:  # curved
                            dirAvailable.remove(self.dirOpposite)
                            return dirAvailable[0]


                    elif dirDOF == 3 or dirDOF == 4:

                        distances0 = []

                        SQ = 0
                        score = 0
                        for dir in dirAvailable:
                            SQ = 0
                            score = 0
                            for i in range(4):
                                if Maze.movingObjectGhosts[i].isCaged==False:
                                    if dir == 'Left':
                                        SQ += (self.coordinateRel[0] - Maze.movingObjectGhosts[i].coordinateRel[0]) ** 2 + (
                                                self.coordinateRel[1] - 1 - Maze.movingObjectGhosts[i].coordinateRel[1]) ** 2
                                    elif dir == 'Right':
                                        SQ += (self.coordinateRel[0] - Maze.movingObjectGhosts[i].coordinateRel[0]) ** 2 + (
                                                self.coordinateRel[1] + 1 - Maze.movingObjectGhosts[i].coordinateRel[1]) ** 2
                                    elif dir == 'Up':
                                        SQ += (self.coordinateRel[0] - 1 - Maze.movingObjectGhosts[i].coordinateRel[0]) ** 2 + (
                                                self.coordinateRel[1] - Maze.movingObjectGhosts[i].coordinateRel[1]) ** 2
                                    else:
                                        SQ += (self.coordinateRel[0] + 1 - Maze.movingObjectGhosts[i].coordinateRel[0]) ** 2 + (
                                                self.coordinateRel[1] - Maze.movingObjectGhosts[i].coordinateRel[1]) ** 2
                                    score += SQ
                            score=math.floor(score)
                            distances0.append(score)
                        if min(distances0)>240:
                            dirAvailable.remove(self.dirOpposite)  # except the opposite direction

                            randNo = randint(0,dirDOF - 2)  # generate a random number, selection of degree of freedom (except the opposite dir)

                            return dirAvailable[randNo]
                        else:
                            index = distances0.index(min(distances0))
                            return dirAvailable[index]


                except ValueError:  # prevent the first loop error (default values would cause ValueError)
                    pass

            elif Maze.movingObjectGhosts[0].weakTimer > 0:  # Ghost weak
                try:
                    if dirDOF == 1:  # to opposite direction, in this case, dirAvailable only have one item (which is opposite dir)
                        return dirAvailable[
                            0]  # this might not use dirOpp as if the object is stopped, dirOpp is not binded properly

                    elif dirDOF == 2:  # advance toward current direction
                        if dirCur in dirAvailable:  # straight
                            return dirCur
                        elif dirCur == 'Stop':  # somehow this object stopped at straight way
                            return dirAvailable[0]
                        else:  # curved
                            dirAvailable.remove(self.dirOpposite)
                            return dirAvailable[0]




                    elif dirDOF == 3 or dirDOF == 4:

                        if dirCur == 'Stop':

                            randNo = randint(0, dirDOF - 1)  # generate a random number, selection of degree of freedom

                            return dirAvailable[randNo]

                        else:

                            dirAvailable.remove(self.dirOpposite)  # except the opposite direction

                            randNo = randint(0,

                                             dirDOF - 2)  # generate a random number, selection of degree of freedom (except the opposite dir)

                            return dirAvailable[randNo]




                except ValueError:  # prevent the first loop error (default values would cause ValueError)
                    pass

    def MoveNextGhost(self, Maze, dirCur):
        ## this function will determine ghost's direction
        # if ghost reaches a grid coordinate, this will check all directions from the ghost's current location
        # we should get DOF here and will determine how we manage ghost's direction
        # DOF == 1 ... opposite direction
        # DOF == 2 ... current direction
        # DOF == 3 ... random direction (except opposite dir)
        # DOF == 4 ... random direction (except opposite dir)

        if self.isCaged == True:  # if ghost is caged, prevent the movement
            pass

        elif self.coordinateAbs[0] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        else:
            dirIndex = ['Left', 'Right', 'Up', 'Down']  # [0]: Left, [1]: Right, [2]: Up, [3]: Down
            dirAvailable = []
            dirDOF = 0

            # find the opposite direction
            if dirCur == 'Left':
                self.dirOpposite = 'Right'
            elif dirCur == 'Right':
                self.dirOpposite = 'Left'
            elif dirCur == 'Up':
                self.dirOpposite = 'Down'
            elif dirCur == 'Down':
                self.dirOpposite = 'Up'
            else:  # dirCur == 'Stop'
                pass

            # checking all directions
            try:
                for i in range(4):

                    if i == 0:
                        nextObject = Maze.levelObjects[self.coordinateRel[0] - 1][
                            self.coordinateRel[1]]  # levelObject on the left
                    elif i == 1:
                        nextObject = Maze.levelObjects[self.coordinateRel[0] + 1][
                            self.coordinateRel[1]]  # levelObject on the right
                    elif i == 2:
                        nextObject = Maze.levelObjects[self.coordinateRel[0]][
                            self.coordinateRel[1] - 1]  # levelObject on the up
                    elif i == 3:
                        nextObject = Maze.levelObjects[self.coordinateRel[0]][
                            self.coordinateRel[1] + 1]  # levelObject on the down

                    if nextObject.name in Maze.levelObjectNamesPassable:
                        dirDOF += 1
                        dirAvailable.append(dirIndex[i])  # append available direction to the list
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass

            except IndexError:  # in case of edge teleport
                dirDOF = 2
                dirAvailable.append(dirCur)

            if self.weakTimer<=2: # Ghost Not weak
                try:
                    if dirDOF == 1:  # to opposite direction, in this case, dirAvailable only have one item (which is opposite dir)
                        return dirAvailable[
                            0]  # this might not use dirOpp as if the object is stopped, dirOpp is not binded properly


                    elif dirDOF == 2:  # advance toward current direction
                        if dirCur in dirAvailable:  # straight
                            return dirCur
                        elif dirCur == 'Stop':  # somehow this object stopped at straight way
                            return dirAvailable[0]
                        else:  # curved
                            dirAvailable.remove(self.dirOpposite)
                            return dirAvailable[0]


                    elif dirDOF == 3 or dirDOF == 4:
                        if dirCur == 'Stop':
                            randNo = randint(0, dirDOF - 1)  # generate a random number, selection of degree of freedom
                            return dirAvailable[randNo]
                        else:
                            dirAvailable.remove(self.dirOpposite)  # except the opposite direction
                            randNo = randint(0,
                                             dirDOF - 2)  # generate a random number, selection of degree of freedom (except the opposite dir)
                            return dirAvailable[randNo]


                except ValueError:  # prevent the first loop error (default values would cause ValueError)
                    pass

            elif self.weakTimer>0:# Ghost weak
                try:
                    if dirDOF == 1:  # to opposite direction, in this case, dirAvailable only have one item (which is opposite dir)
                        return dirAvailable[
                            0]  # this might not use dirOpp as if the object is stopped, dirOpp is not binded properly

                    elif dirDOF == 2:  # advance toward current direction
                        if dirCur in dirAvailable:  # straight
                            return dirCur
                        elif dirCur == 'Stop':  # somehow this object stopped at straight way
                            return dirAvailable[0]
                        else:  # curved
                            dirAvailable.remove(self.dirOpposite)
                            return dirAvailable[0]



                    elif dirDOF == 3 or dirDOF == 4:
                        distances0 = []

                        SQ=0
                        for dir in dirAvailable:
                            if dir == 'Left':
                                SQ = (self.coordinateRel[0] - Maze.movingObjectPacman.coordinateRel[0]) ** 2 + (
                                        self.coordinateRel[1] -1- Maze.movingObjectPacman.coordinateRel[1]) ** 2
                            elif dir == 'Right':
                                SQ = (self.coordinateRel[0] - Maze.movingObjectPacman.coordinateRel[0]) ** 2 + (
                                        self.coordinateRel[1] + 1 - Maze.movingObjectPacman.coordinateRel[1]) ** 2
                            elif dir == 'Up':
                                SQ = (self.coordinateRel[0] -1- Maze.movingObjectPacman.coordinateRel[0]) ** 2 + (
                                        self.coordinateRel[1]- Maze.movingObjectPacman.coordinateRel[1]) ** 2
                            else:
                                SQ = (self.coordinateRel[0] +1- Maze.movingObjectPacman.coordinateRel[0]) ** 2 + (
                                        self.coordinateRel[1] - Maze.movingObjectPacman.coordinateRel[1]) ** 2

                            distances0.append(SQ)
                        index = distances0.index(min(distances0))



                        return dirAvailable[index]




                except ValueError:  # prevent the first loop error (default values would cause ValueError)
                    pass

    def MoveNext(self, Maze):
        ## this function will determine pacman can move with given direction or not

        if self.dirNext == self.dirCurrent:  # in this case, no action is required
            pass

        elif self.coordinateAbs[0] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0:  # if the object is moving, prevent to change its direction
            pass

        else:
            if self.dirNext == "Left":  # check the direction first

                if self.coordinateRel[
                    0] == 0:  # at left edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Left"

                else:
                    nextObject = Maze.levelObjects[self.coordinateRel[0] - 1][
                        self.coordinateRel[1]]  # levelObject placed left of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in Maze.levelObjectNamesPassable:
                        self.dirCurrent = "Left"
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Right":

                if self.coordinateRel[
                    0] == 47:  # at right edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Right"

                else:
                    nextObject = Maze.levelObjects[self.coordinateRel[0] + 1][
                        self.coordinateRel[1]]  # levelObject placed right of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in Maze.levelObjectNamesPassable:
                        self.dirCurrent = "Right"
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Down":

                if self.coordinateRel[
                    1] == 31:  # at bottom edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Down"

                else:
                    nextObject = Maze.levelObjects[self.coordinateRel[0]][
                        self.coordinateRel[1] + 1]  # levelObject placed down of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in Maze.levelObjectNamesPassable:
                        self.dirCurrent = "Down"
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Up":

                if self.coordinateRel[
                    1] == 0:  # at top edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Up"

                else:
                    nextObject = Maze.levelObjects[self.coordinateRel[0]][
                        self.coordinateRel[1] - 1]  # levelObject placed up of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in Maze.levelObjectNamesPassable:
                        self.dirCurrent = "Up"
                    elif nextObject.name in Maze.levelObjectNamesBlocker:
                        pass

    def MoveCurrent(self, Maze):

        if self.dirCurrent == "Left":

            if self.coordinateAbs[0] == 0:  # at left edge, move to right edge
                self.coordinateAbs[0] = 47 * 4 + 3
                self.coordinateRel[0] = 48
                self.dirEdgePassed = True

            else:
                nextObject = Maze.levelObjects[self.coordinateRel[0] - 1][
                    self.coordinateRel[1]]  # levelObject placed left of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in Maze.levelObjectNamesPassable:
                    self.coordinateAbs[0] -= 1  # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0:  # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] -= 1

                elif nextObject.name in Maze.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Right":

            if self.coordinateAbs[0] == 47 * 4:  # at right edge, move to left edge
                self.coordinateAbs[0] = -3
                self.coordinateRel[0] = -1
                self.dirEdgePassed = True

            else:
                nextObject = Maze.levelObjects[self.coordinateRel[0] + 1][
                    self.coordinateRel[1]]  # levelObject placed right of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in Maze.levelObjectNamesPassable:
                    self.coordinateAbs[0] += 1  # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0:  # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] += 1

                elif nextObject.name in Maze.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Down":

            if self.coordinateAbs[1] == 31 * 4:  # at bottom edge, move to top edge
                self.coordinateAbs[1] = -3
                self.coordinateRel[1] = -1
                self.dirEdgePassed = True

            else:
                nextObject = Maze.levelObjects[self.coordinateRel[0]][
                    self.coordinateRel[1] + 1]  # levelObject placed down of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in Maze.levelObjectNamesPassable:
                    self.coordinateAbs[1] += 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0:  # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] += 1

                elif nextObject.name in Maze.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Up":

            if self.coordinateAbs[1] == 0:  # at top edge, move to bottom edge
                self.coordinateAbs[1] = 31 * 4 + 3
                self.coordinateRel[1] = 32
                self.dirEdgePassed = True

            else:
                nextObject = Maze.levelObjects[self.coordinateRel[0]][
                    self.coordinateRel[1] - 1]  # levelObject placed up of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in Maze.levelObjectNamesPassable:
                    self.coordinateAbs[1] -= 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0:  # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] -= 1

                elif nextObject.name in Maze.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Stop":
            pass


newMaze = Maze()
