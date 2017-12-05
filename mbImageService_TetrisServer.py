from microbit import*
import radio
import random

radio.on()
radio.config(length=20, queue=12, channel=19, power=6)

shape_Square = (22, 33, 55)
shape_Long = (444, 555)
shape_squiggel_S_NS = (944, 435, 559)


shapes_0deg =           (   shape_Square, shape_Long, (299, 344, 555), (992, 443, 555), (929, 434, 555), shape_squiggel_S_NS
                        )

shapes_90deg =          (   shape_Square, (2, 3 , 3, 5), (24, 35, 39, 59), (29, 39, 34 , 55), (29, 34, 35, 59), (49, 34, 53, 95)
                        )

shapes_180deg =         (   shape_Square, shape_Long, (444, 553, 995), (444, 535, 959), (444, 355, 599), shape_squiggel_S_NS
                        )

shapes_AllOrientations = (  shapes_0deg, shapes_90deg, shapes_180deg)

#shapes_270deg =         (   shape_Square, shape_Long
#                        )

global shapes_defaultMasks
shapes_defaultMasks = shapes_180deg

global shape_Orientation
shape_Orientation = 0

runInit = True

global board_blockLocations
board_blockLocations = []   

global shapes_CurrentShapeType

global shapes_TotalShapes 
shapes_TotalShapes = 6

global totalRows
global totalCols
totalRows = 12
totalCols = 10

isGameOver = False


global shapes_CurrentShapeLocation
shapes_CurrentShapeLocation = [0, 0]        #   2 = row, 3 = col

global currentAnimationRow


def makeNewShape():
    global shapes_CurrentShapeType
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeType         = random.randint(0, (shapes_TotalShapes - 1))
    #shapes_CurrentShapeType         = 7
    shapes_CurrentShapeLocation[0]  = 0
    shapes_CurrentShapeLocation[1]  = 0


def makeNextFrame():
    moveShapeDown()
    for i in range(len(shapes_defaultMasks[shapes_CurrentShapeType])):
        strBuf  = ("tX120" + str(currentAnimationRow) + getPaddedRowRefStr(shapes_CurrentShapeLocation[0] + i) + getRowMask(i))
        #radio.send("tX120" + str(currentAnimationRow) + getPaddedRowRefStr(shapes_CurrentShapeLocation[0] + i) + getRowMask(i))

    
def getPaddedRowRefStr(rowRef):
    if (rowRef < 10):   return "0" + str(rowRef)
    return str(rowRef)


def getRowMask(rowOfShape):        # each shape has several rows - we construct a new line for each row:
    strBuf = "_"
    for i in range(shapes_CurrentShapeLocation[1]):
        strBuf  = strBuf  + "0"
    strBuf  = strBuf  + str(shapes_defaultMasks[shapes_CurrentShapeType][rowOfShape])
    #for i in range(totalCols - shapes_CurrentShapeLocation[1] - shapes_Cols[shapes_CurrentShapeType]):
    for i in range(totalCols - shapes_CurrentShapeLocation[1] - getColsInCurrentShape()):
        strBuf  = strBuf  + "0"
    return strBuf


def moveShapeHorizontally(moveDir):
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeLocation[1] = shapes_CurrentShapeLocation[1] + moveDir
    if(shapes_CurrentShapeLocation[1] <= 0):    shapes_CurrentShapeLocation[1] = 0
    
    #if((shapes_CurrentShapeLocation[1] + shapes_Cols[shapes_CurrentShapeType]) >= totalCols):   
    if((shapes_CurrentShapeLocation[1] + getColsInCurrentShape()) >= totalCols):   
        #shapes_CurrentShapeLocation[1] = (totalCols - shapes_Cols[shapes_CurrentShapeType])
        shapes_CurrentShapeLocation[1] = (totalCols - getColsInCurrentShape())
    #print("--------------------------------------------------")
    #print("Direction = " + str(moveDir) +", width = " + str(shapes_Cols[shapes_CurrentShapeType]) + ", Pos = " + str(shapes_CurrentShapeLocation[1]))    


def moveShapeDown():
    global currentAnimationRow
    global shapes_CurrentShapeLocation
    currentAnimationRow = currentAnimationRow + 1
    if(currentAnimationRow == 5):
        currentAnimationRow = 0
        if(checkVerticalCollision()):
            addShapeToBoard()
            printBoard()
            for i in range(shapes_CurrentShapeLocation[0], totalRows, 1):
                if(checkForTetris(i)):  print("Tetris in row: " + str(i))
            makeNewShape()
        else:
            shapes_CurrentShapeLocation[0] = shapes_CurrentShapeLocation[0] + 1

def checkForTetris(rowNum):
    global board_blockLocations
    for i in range(rowNum * totalCols, rowNum * totalCols + totalCols, 1):
        if(board_blockLocations[i] == 0): return False

    #print("tX1220" + getPaddedRowRefStr(rowNum))
    for j in range(rowNum, 1, -1):
        board_blockLocations[j * totalCols : j * totalCols + totalCols] = board_blockLocations[(j-1) * totalCols : (j-1) * totalCols + totalCols]
    return True
    
def checkVerticalCollision():
    if( (shapes_CurrentShapeLocation[0] + len(shapes_defaultMasks[shapes_CurrentShapeType]) - 1) >= totalRows):        return True
    
    for i in range(len(shapes_defaultMasks[shapes_CurrentShapeType])):
        #for j in range(shapes_Cols[shapes_CurrentShapeType]):
        for j in range(getColsInCurrentShape()):
            #if(getShapeRowStr(i)[j] == "5"):
            if((str(shapes_defaultMasks[shapes_CurrentShapeType][i]))[j] == "5"):    
                if(board_blockLocations[(i + shapes_CurrentShapeLocation[0]) * totalCols + shapes_CurrentShapeLocation[1] + j] == 1):
                    #boardCharLocation = (i + shapes_CurrentShapeLocation[0]) * totalCols + shapes_CurrentShapeLocation[1] + j
                    #boardCharStr = str(board_blockLocations[boardCharLocation])
                    #print("B-col:" + getShapeRowStr(i) + "Location:" + str(j) + "Ar ref: " + str(boardCharLocation) + "... board val = " + boardCharStr)
                    #print("Buffer collision")
                    return True

    return False


def addShapeToBoard():  # shape has come to rest, now we need to add it to the Board Locations array:
    global board_blockLocations
    for i in range(len(shapes_defaultMasks[shapes_CurrentShapeType])):
        #for j in range(shapes_Cols[shapes_CurrentShapeType]):
        for j in range(getColsInCurrentShape()):
            curChar = (str(shapes_defaultMasks[shapes_CurrentShapeType][i]))[j]
            if(not((curChar == "5") or (curChar == "9"))):
                board_blockLocations[((shapes_CurrentShapeLocation[0] + i) * totalCols) + (shapes_CurrentShapeLocation[1] + j)] = 1


def getColsInCurrentShape():
    if(shapes_defaultMasks[shapes_CurrentShapeType][0] < 10): return 1
    if(shapes_defaultMasks[shapes_CurrentShapeType][0] < 100): return 2
    return 3


def printBoard():
    for i in range(totalRows):
        print("" + str(board_blockLocations[i * totalCols : i * totalCols + totalCols]))
    print("--------------------------------------------------")


#def checkGameOver():
#    for i in range(totalCols):
#        if(board_blockLocations[i + totalCols] == 1): return True
#    return False

#def changeShapeOrientation(rotateDir):
#    global shapes_defaultMasks
#    global shape_Orientation

#    shape_Orientation = (shape_Orientation + rotateDir) % 3
#    shapes_defaultMasks = shapes_AllOrientations[shape_Orientation]
        
        
while True:
    if(runInit): 
        makeNewShape()
        for i in range(totalRows * totalCols):        board_blockLocations.append(0)
        currentAnimationRow = 0
        runInit = False
        print("init")
    if(not(isGameOver)):
        #isGameOver = checkGameOver()
        for i in range(totalCols):
            if(board_blockLocations[i + totalCols] == 1): isGameOver = True
        
        if (isGameOver):
            print("GAME OVER")
        else:
            timeBeforeMakeFrame = running_time()
            makeNextFrame()
            while(  (running_time() - timeBeforeMakeFrame) < 100):
                if(button_a.was_pressed()):             moveShapeHorizontally(-1)
                if(button_b.was_pressed()):             moveShapeHorizontally(1)    
                #if(accelerometer.was_gesture('right')): changeShapeOrientation(1)
                #if(accelerometer.was_gesture('left')): changeShapeOrientation(-1)
                #    print("Execution time = " + str(running_time() - timeBeforeMakeFrame))