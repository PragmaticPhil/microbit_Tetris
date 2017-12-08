from microbit import*
import random

shape_Square = (22, 33, 55)
shape_Long = (444, 555)
shape_squiggel_S_NS = (944, 435, 559)
shape_squiggel_S_EW = (49, 34, 53, 95)
shape_Tall = (2, 3 , 3, 5)

shapes_0deg =           (   shape_Square, shape_Long, (299, 344, 555), (992, 443, 555), (929, 434, 555), shape_squiggel_S_NS
                        )

shapes_90deg =          (   shape_Square, shape_Tall, (24, 35, 39, 59), (29, 39, 34 , 55), (29, 34, 35, 59), shape_squiggel_S_EW
                        )

shapes_180deg =         (   shape_Square, shape_Long, (444, 553, 995), (444, 355, 959), (444, 535, 599), shape_squiggel_S_NS
                        )

shapes_270deg =         (   shape_Square, shape_Tall, (94, 93, 43, 55), (94, 93, 53, 95), (44, 53, 93, 95), shape_squiggel_S_EW
                        )

shapes_AllOrientations = (  shapes_0deg, shapes_90deg, shapes_180deg, shapes_270deg)

global shapes_defaultMasks
shapes_defaultMasks = shapes_180deg

global shape_Orientation
shape_Orientation = 0

runInit = True

global board_blockLocations
board_blockLocations = []   

global shapes_CurrentShapeType


global totalRows
global totalCols
totalRows = 15
totalCols = 12

isGameOver = False


global shapes_CurrentShapeLocation
shapes_CurrentShapeLocation = [0, 0]        #   2 = row, 3 = col

global currentAnimationRow


def makeNewShape():
    global shapes_CurrentShapeType
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeType         = random.randint(0, 5)
    #shapes_CurrentShapeType         = 7
    shapes_CurrentShapeLocation[0]  = 0
    shapes_CurrentShapeLocation[1]  = 0


def moveShapeHorizontally(moveDir):
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeLocation[1] = shapes_CurrentShapeLocation[1] + moveDir
    if(shapes_CurrentShapeLocation[1] <= 0):    shapes_CurrentShapeLocation[1] = 0

    if((shapes_CurrentShapeLocation[1] + getColsInCurrentShape()) >= totalCols):
        shapes_CurrentShapeLocation[1] = (totalCols - getColsInCurrentShape())


def moveShapeDown():
    global currentAnimationRow
    global shapes_CurrentShapeLocation
    currentAnimationRow = currentAnimationRow + 1
    if(currentAnimationRow == 5):
        currentAnimationRow = 0
        printBoard()
        if(checkVerticalCollision()):
            addShapeToBoard(1)
            #printBoard()
            for i in range(shapes_CurrentShapeLocation[0], totalRows, 1):
                if(checkForTetris(i)):  print("Tetris in row: " + str(i))
            makeNewShape()
        else:
            shapes_CurrentShapeLocation[0] = shapes_CurrentShapeLocation[0] + 1

def checkForTetris(rowNum):
    global board_blockLocations
    for i in range(rowNum * totalCols, rowNum * totalCols + totalCols, 1):
        if(board_blockLocations[i] == 0): return False

    for j in range(rowNum, 1, -1):
        board_blockLocations[j * totalCols : j * totalCols + totalCols] = board_blockLocations[(j-1) * totalCols : (j-1) * totalCols + totalCols]
    return True
    
def checkVerticalCollision():
    if( (shapes_CurrentShapeLocation[0] + len(shapes_defaultMasks[shapes_CurrentShapeType]) - 1) >= totalRows):        return True
    
    for i in range(len(shapes_defaultMasks[shapes_CurrentShapeType])):
        for j in range(getColsInCurrentShape()):
            if((str(shapes_defaultMasks[shapes_CurrentShapeType][i]))[j] == "5"):    
                if(board_blockLocations[(i + shapes_CurrentShapeLocation[0]) * totalCols + shapes_CurrentShapeLocation[1] + j] == 1):
                    return True

    return False


def addShapeToBoard(intVal):  # shape has come to rest, now we need to add it to the Board Locations array:
    global board_blockLocations
    try:
        for i in range(len(shapes_defaultMasks[shapes_CurrentShapeType])):
            for j in range(getColsInCurrentShape()):
                curChar = (str(shapes_defaultMasks[shapes_CurrentShapeType][i]))[j]
                if(not((curChar == "5") or (curChar == "9"))):
                    board_blockLocations[((shapes_CurrentShapeLocation[0] + i) * totalCols) + (shapes_CurrentShapeLocation[1] + j)] = intVal
    except:
        return

def getColsInCurrentShape():
    return len(str(shapes_defaultMasks[shapes_CurrentShapeType][0]))
#    if(shapes_defaultMasks[shapes_CurrentShapeType][0] < 10): return 1
#    if(shapes_defaultMasks[shapes_CurrentShapeType][0] < 100): return 2
#    return 3


def printBoard():
    addShapeToBoard(7)
    for i in range(totalRows):
        print("" + str(board_blockLocations[i * totalCols : i * totalCols + totalCols]))
    print("--------------------------------------------------")
    addShapeToBoard(0)

#def checkGameOver():
#    for i in range(totalCols):
#        if(board_blockLocations[i + totalCols] == 1): return True
#    return False

def changeShapeOrientation(rotateDir):
    global shapes_defaultMasks
    global shape_Orientation

    shape_Orientation = (shape_Orientation + rotateDir) % 4
    shapes_defaultMasks = shapes_AllOrientations[shape_Orientation]
        
        
while True:
    spinDir = 0
    if(runInit): 
        makeNewShape()
        for i in range(totalRows * totalCols):        board_blockLocations.append(0)
        currentAnimationRow = 0
        runInit = False
        print("init")
    if(not(isGameOver)):
        #isGameOver = checkGameOver()
        for i in range(totalCols):
            if(board_blockLocations[i + totalCols] == 1): isGameOver =  True
        if (isGameOver):
            print("GAME OVER")
        else:
            timeBeforeMakeFrame = running_time()

            moveShapeDown()
            while(  (running_time() - timeBeforeMakeFrame) < 150):
                if(button_b.was_pressed()):             moveShapeHorizontally(1)
                if(button_a.was_pressed()):             moveShapeHorizontally(-1)
                if(accelerometer.was_gesture('right')): spinDir = 1
                if(accelerometer.was_gesture('left')):  spinDir = -1
                #    print("Execution time = " + str(running_time() - timeBeforeMakeFrame))
            changeShapeOrientation(spinDir)