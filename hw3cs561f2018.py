import time
import numpy as np
import math
from decimal import Decimal
from copy import deepcopy

obsCoords = []
startCoords = []
endCoords = []
utilityMatrixOfAll = []
rewardMatrixOfAll = []
policyMatrixOfAll = []

def getRewardMatrix(index):
    global rewardMatrixOfAll
    global endCoords
    global obsCoords
    goalCoords = endCoords[index].split(",")
    y = int(goalCoords[0])
    x = int(goalCoords[1])
    #check if assignment is possible else copy
    matrix = (rewardMatrixOfAll[index])
    matrix[x][y] = np.float64(99)
    for val in obsCoords:
        coords = val.split(",")
        y = int(coords[0])
        x = int(coords[1])
        matrix[x][y] = np.float64(-101)
    rewardMatrixOfAll[index] = (matrix)
    return matrix

def getNextCoordOnMove(move, curx, cury, size):
    nextCoords = {}
    if move == "north":
        if curx == 0:
            nextCoords["x"] = curx
            nextCoords["y"] = cury
        else:
            nextCoords["x"] = curx - 1
            nextCoords["y"] = cury
    if move == "south":
        if curx == size -1:
            nextCoords["x"] = curx
            nextCoords["y"] = cury
        else:
            nextCoords["x"] = curx + 1
            nextCoords["y"] = cury
    if move == "east":
        if cury == size-1:
            nextCoords["x"] = curx
            nextCoords["y"] = cury
        else:
            nextCoords["x"] =  curx
            nextCoords["y"] = cury + 1
    if move == "west":
        if cury == 0:
            nextCoords["x"] = curx
            nextCoords["y"] = cury
        else:
            nextCoords["x"] = curx
            nextCoords["y"] = cury-1
    return nextCoords


def getUtilityMatrix(index, size, gamma, epsilon):
    global rewardMatrixOfAll
    global endCoords
    global startCoords

    initialmatrix = [0] * size
    for i in range(size):
        initialmatrix[i] = [0] * size

    rewardmatrix = (rewardMatrixOfAll[index])
    for i in range(size):
        for j in range(size):
            initialmatrix[i][j] = rewardmatrix[i][j]

    #print "initial matrix"
    #print initialmatrix
    start = startCoords[index].split(",")
    starty = int(start[0])
    startx = int(start[1])
    #cnt = 0
    while(True):
        utilityupdated = [tmp[:] for tmp in initialmatrix]
        delta = 0
        #cnt += 1
        for i in xrange(size):
            for j in xrange(size):
                nextN = getNextCoordOnMove("north", i, j, size)
                nextS = getNextCoordOnMove("south", i, j, size)
                nextE = getNextCoordOnMove("east", i, j, size)
                nextW = getNextCoordOnMove("west", i, j, size)
                if initialmatrix[i][j] == np.float64(99):
                    utilityupdated[i][j] = np.float64(99)
                    continue

                prob70 = np.float64(0.7)
                prob10 = np.float64(0.1)
                northMove = prob70*initialmatrix[nextN["x"]][nextN["y"]] + prob10*(initialmatrix[nextE["x"]][nextE["y"]] + \
                                initialmatrix[nextW["x"]][nextW["y"]] + initialmatrix[nextS["x"]][nextS["y"]])

                southMove = prob70*initialmatrix[nextS["x"]][nextS["y"]] + prob10*(initialmatrix[nextN["x"]][nextN["y"]] + initialmatrix[nextE["x"]][nextE["y"]] + \
                                 initialmatrix[nextW["x"]][nextW["y"]])

                eastMove = prob70*initialmatrix[nextE["x"]][nextE["y"]] + prob10*(initialmatrix[nextN["x"]][nextN["y"]] + \
                                initialmatrix[nextW["x"]][nextW["y"]] + initialmatrix[nextS["x"]][nextS["y"]])

                westMove = prob70*initialmatrix[nextW["x"]][nextW["y"]] + prob10*(initialmatrix[nextN["x"]][nextN["y"]] +
                                initialmatrix[nextE["x"]][nextE["y"]] + initialmatrix[nextS["x"]][nextS["y"]])

                val = rewardmatrix[i][j] + gamma*max(northMove, southMove, eastMove, westMove)
                utilityupdated[i][j] = val
                #print "===="
                #print val
                delta = max(delta, abs(initialmatrix[i][j] - utilityupdated[i][j]))

        if delta < (epsilon * (1-gamma)/gamma):
            return initialmatrix
        initialmatrix = utilityupdated

    return initialmatrix

def getPolicyMatrix(utilitymatrix, size):
    policymatrix = [0]*size
    for i in range(size):
        policymatrix[i] = [0]*size
    for i in range(size):
        for j in range(size):
            if utilitymatrix[i][j] == np.float64(99):
                policymatrix[i][j] = "goal"
                continue
            northCoord = getNextCoordOnMove("north", i, j, size)
            utilityN = utilitymatrix[northCoord["x"]][northCoord["y"]]

            southCoord = getNextCoordOnMove("south", i, j, size)
            utilityS = utilitymatrix[southCoord["x"]][southCoord["y"]]

            eastCoord = getNextCoordOnMove("east", i, j, size)
            utilityE = utilitymatrix[eastCoord["x"]][eastCoord["y"]]

            westCoord = getNextCoordOnMove("west", i, j, size)
            utilityW = utilitymatrix[westCoord["x"]][westCoord["y"]]

            maxVal = max(utilityN, utilityS, utilityE, utilityW)

            if (maxVal) == (utilityN):
                policymatrix[i][j] = "north"
            elif (maxVal) == (utilityS):
                policymatrix[i][j] = "south"
            elif (maxVal) == (utilityE):
                policymatrix[i][j] = "east"
            else:
                policymatrix[i][j] = "west"

    return policymatrix


def turn_left(curmove):
    move = ""
    if curmove == "north":
        move = "west"
    elif curmove == "west":
        move = "south"
    elif curmove == "south":
        move = "east"
    elif curmove == "east":
        move = "north"
    return move

def turn_right(curmove):
    move = ""
    if curmove == "north":
        move = "east"
    elif curmove == "west":
        move = "north"
    elif curmove == "south":
        move = "west"
    elif curmove == "east":
        move = "south"
    return move


def main():
    global obsCoords
    global startCoords
    global endCoords
    global utilityMatrix
    global rewardMatrix
    global policyMatrix

    rewardOfCars = []
    start = time.time()
    fp = open('input.txt', 'r')
    lines = fp.read().splitlines()
    fp.close()
    gridSize = int(lines[0])
    noOfCars = int(lines[1])
    noOfObstacles = int(lines[2])
    i,j,k = 0,0,0

    k = 3
    cnt = 0
    while (cnt != noOfObstacles):
        obsCoords.append(lines[k])
        cnt += 1
        k = k+1

    cnt = 0
    j = k
    while (cnt != noOfCars):
        startCoords.append(lines[j])
        cnt += 1
        j = j+1

    cnt = 0
    i = j
    while (cnt != noOfCars):
        endCoords.append(lines[i])
        cnt += 1
        i = i+1

    for j in range(0,noOfCars):
        rewardMatrix = [np.float64(-1)]*gridSize
        for i in range(0, gridSize):
            rewardMatrix[i] = [np.float64(-1)]*gridSize
        rewardMatrixOfAll.append(rewardMatrix)


    for i in range(noOfCars):
        rewardMatrixOfThisCar = getRewardMatrix(i)
        utilityMatrix = getUtilityMatrix(i, gridSize, gamma=np.float64(0.9), epsilon=np.float64(0.1))
        #print "Utility matrix"
        #print utilityMatrix
        policyMatrix = getPolicyMatrix(utilityMatrix, gridSize)
        utilityMatrixOfAll.append(utilityMatrix)
        policyMatrixOfAll.append(policyMatrix)
        #print policyMatrix

    for i in range(noOfCars):

        sumOfReward = 0

        for j in range(10):
            #print "start"

            pos1 = startCoords[i].split(",")
            ycoord =  int(pos1[0])
            xcoord = int(pos1[1])

            pos2 = endCoords[i].split(",")
            ycoordEnd = int(pos2[0])
            xcoordEnd = int(pos2[1])

            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            reward = np.float64(0)
            #print "____________________"
            if xcoord == xcoordEnd and ycoord == ycoordEnd:
                reward = np.float64(100)

            while (not(xcoord == xcoordEnd and ycoord == ycoordEnd)):
                move = policyMatrixOfAll[i][xcoord][ycoord]

                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = turn_right(turn_right(move))
                        else:
                            move = turn_right(move)
                    else:
                        move = turn_left(move)
                k += 1

                next = getNextCoordOnMove(move, xcoord, ycoord, gridSize)
                xcoord = next["x"]
                ycoord = next["y"]
                reward += rewardMatrixOfAll[i][xcoord][ycoord]
            #print("reward")
            #print reward

            sumOfReward += reward
        #print sumOfReward
        rewardOfCars.append(str(int(math.floor(sumOfReward / 10.0))))

    fp = open("output.txt", 'w')
    for k in rewardOfCars:
        fp.write(str(k))
        fp.write("\n")
    fp.close()
    #print "reward of cars"
    #print rewardOfCars
    #print time.time() - start


    #print rewardMatrixOfAll
    '''print gridSize
    print noOfCars
    print noOfObstacles
    print "Obstacles are"
    print obsCoords
    print "start coords are"
    print startCoords
    print "end coords are"
    print endCoords'''

if __name__ == "__main__":
    main()
