from microbit import*
import radio
import random

radio.on()
radio.config(length=20, queue=12, channel=19, power=6)

global totalRows
global totalCols
totalRows = 10
totalCols = 8

shape_Square = (22, 33, 55)
shape_Long = (444, 555)
shape_LeftUp = (299, 344, 555)
shape_RightUp = (992, 443, 555)
shape_MiddleUp = (929, 434, 555)
shape_UpSquiggle = (299, 342, 554, 995)

shapes_Rows = (3, 2, 3, 3, 3, 4)
shapes_Cols = (2, 3, 3, 3, 3, 3)

shapes_defaultMasks = ( shape_Square, 
                        shape_Long, 
                        shape_LeftUp, 
                        shape_RightUp, 
                        shape_MiddleUp, 
                        shape_UpSquiggle)

runInit = True

global board_blockLocations
board_blockLocations = []   

global shapes_CurrentShapeType
shapes_CurrentShapeType = 3

global shapes_CurrentShapeLocation
shapes_CurrentShapeLocation = [2, 3]        #   2 = row, 3 = col

global currentAnimationRow
currentAnimationRow = 0


def makeNewShape():
    global shapes_CurrentShapeType
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeType         = random.randint(0, 5)
    shapes_CurrentShapeLocation[0]  = 0
    shapes_CurrentShapeLocation[1]  = 0


def makeNextFrame():
    moveShapeDown()
    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
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
    for i in range(totalCols - shapes_CurrentShapeLocation[1] - shapes_Cols[shapes_CurrentShapeType]):
        strBuf  = strBuf  + "0"
    return strBuf


def moveShapeHorizontally(moveDir):
    global shapes_CurrentShapeLocation
    shapes_CurrentShapeLocation[1] = shapes_CurrentShapeLocation[1] + moveDir
    if(shapes_CurrentShapeLocation[1] <= 0):    shapes_CurrentShapeLocation[1] = 0
    if((shapes_CurrentShapeLocation[1] + shapes_Cols[shapes_CurrentShapeType]) >= totalCols):   
        shapes_CurrentShapeLocation[1] = (totalCols - shapes_Cols[shapes_CurrentShapeType])
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


def initialiseBlockArray(blockArray):
    for i in range(totalRows * totalCols):
        blockArray.append(0)

def checkForTetris(rowNum):
    global board_blockLocations
    for i in range(rowNum * totalCols, rowNum * totalCols + totalCols, 1):
        if(board_blockLocations[i] == 0): return False

    print("tX1220" + getPaddedRowRefStr(rowNum))
    for j in range(rowNum, 1, -1):
        board_blockLocations[j * totalCols : j * totalCols + totalCols] = board_blockLocations[(j-1) * totalCols : (j-1) * totalCols + totalCols]
    return True
    
def checkVerticalCollision():
    if( (shapes_CurrentShapeLocation[0] + shapes_Rows[shapes_CurrentShapeType] - 1) >= totalRows):        return True

    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
        for j in range(0, shapes_Cols[shapes_CurrentShapeType], 1):
            if(getCharAt(getShapeRowStr(i), j) == "5"):
                if(board_blockLocations[(i + shapes_CurrentShapeLocation[0]) * totalCols + shapes_CurrentShapeLocation[1] + j] == 1):
                    #boardCharLocation = (i + shapes_CurrentShapeLocation[0]) * totalCols + shapes_CurrentShapeLocation[1] + j
                    #boardCharStr = str(board_blockLocations[boardCharLocation])
                    #print("B-col:" + getShapeRowStr(i) + "Location:" + str(j) + "Ar ref: " + str(boardCharLocation) + "... board val = " + boardCharStr)
                    print("Buffer collision")
                    return True

    return False


def addShapeToBoard():  # shape has come to rest, now we need to add it to the Board Locations array:
    global board_blockLocations
    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
        for j in range(0, shapes_Cols[shapes_CurrentShapeType], 1):
            curChar = getCharAt(getShapeRowStr(i), j)
            if(not((curChar == "5") or (curChar == "9"))):
                board_blockLocations[((shapes_CurrentShapeLocation[0] + i) * totalCols) + (shapes_CurrentShapeLocation[1] + j)] = 1

def getShapeRowStr(rowNum):
    return str(shapes_defaultMasks[shapes_CurrentShapeType][rowNum])

def getCharAt(rowMask, colNum):
    return (rowMask[colNum])

def printBoard():
    for i in range(0, totalRows, 1):
        print("" + str(board_blockLocations[i * totalCols : i * totalCols + totalCols]))
    print("--------------------------------------------------")


while True:
    if(runInit): 
        makeNewShape()
        initialiseBlockArray(board_blockLocations)
        runInit = False
        print("init")

    makeNextFrame()
    sleep(10)
    
    if(button_a.was_pressed()):
        moveShapeHorizontally(-1)

    if(button_b.was_pressed()):
        moveShapeHorizontally(1)    