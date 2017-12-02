from microbit import*
import radio
import random
# rem - use random.choice(shapes)

radio.on()
radio.config(length=20, queue=12, channel=19, power=6)

global totalRows
global totalCols
totalRows = 10
totalCols = 8


shape_Square = (22, 33, 55)
shape_Long = (444, 555)
shape_LeftUp = (255, 344, 555)
shape_RightUp = (552, 443, 555)
shape_MiddleUp = (525, 434, 555)
shape_UpSquiggle = (255, 342, 554, 995)

shapes_Rows = (3, 2, 3, 3, 3, 4)
shapes_Cols = (2, 3, 3, 3, 3, 3)

shapes_defaultMasks = ( shape_Square, 
                        shape_Long, 
                        shape_LeftUp, 
                        shape_RightUp, 
                        shape_MiddleUp, 
                        shape_UpSquiggle)

runInit = True

global board_blockLocations     # NB - we only keep info on settled blocks, not those that are moving.
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
    shapes_CurrentShapeType         = random.randint(0, len(shapes_defaultMasks) - 1)
    arbInt = totalCols - shapes_Cols[shapes_CurrentShapeType]
    shapes_CurrentShapeLocation[0]  = 0
    shapes_CurrentShapeLocation[1]  = arbInt
    #shapes_CurrentShapeLocation[1]  = random.randint(0, totalCols - shapes_Cols[shapes_CurrentShapeType])
    #print("Shape type = " + str(shapes_CurrentShapeType) + " - (" + str(shapes_CurrentShapeLocation) + ")")




def makeNextFrame():
    #startTime = 
    moveShapeDown()
    # if animation frame = 0 clear the row above... build a generic clear row function and rem to parametise whether row is being 
    # cleared cos block has shifted or cos of a tetris... in the case of the latter an animation is triggered in the node. 
    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
        strBuf = makeNextRowCommand(i)
        #print(makeNextRowCommand(i))
    #print("----------------------------")


def makeNextRowCommand(currentShapeRow):
    return ("tX120" + str(currentAnimationRow) + getPaddedRowRefStr(shapes_CurrentShapeLocation[0] + currentShapeRow) + getRowMask(currentShapeRow))

    
def getPaddedRowRefStr(rowRef):
    if (rowRef < 10):   return "0" + str(rowRef)
    return str(rowRef)


def getRowMask(rowOfShape):        # each shape has several rows - we construct a new line for each row:
    strBuf = "_"
    for i in range(0, shapes_CurrentShapeLocation[1], 1):   strBuf  = strBuf  + "0"
        
    strBuf  = strBuf  + str(shapes_defaultMasks[shapes_CurrentShapeType][rowOfShape])
    
    remainingChars = totalCols - shapes_CurrentShapeLocation[1] - shapes_Cols[shapes_CurrentShapeType]
    for i in range(0, remainingChars, 1):
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
    #print("Move shape down")
    currentAnimationRow = currentAnimationRow + 1
    if(currentAnimationRow == 5):
        currentAnimationRow = 0
        if(checkVerticalCollision()):
            printBoard()
            makeNewShape()
        else:
            shapes_CurrentShapeLocation[0] = shapes_CurrentShapeLocation[0] + 1

def clearRow(rowNum):
    #print("tX1210" + getPaddedRowRefStr(rowNum))
    for i in range(0, totalCols, 1):
        setBoardBlockLocation(rowNum, i, 0)

def setBoardBlockLocation(rowNum, colNum, val):
    global board_blockLocations
    insertPoint = (rowNum * totalCols) + colNum
    #print("insert point = " + str(insertPoint))
    board_blockLocations[insertPoint] = val


def isBlockAt(rowNum, colNum):
    rowMaskBuf = board_blockLocations[rowNum]
    if(rowMaskBuf == 0): return False
    return True

def initialiseBlockArray(blockArray):
    for i in range(0, (totalRows * totalCols), 1):
        blockArray.append(0)

def printBoard():
    intBuf = 0
    strBuf = ""
    for i in range(0, totalRows, 1):
        intBuf = (i * totalCols)
        strBuf = str(i) + ":"
        for j in range(0, totalCols, 1):
            strBuf = strBuf + str(board_blockLocations[intBuf + j]) 
        print(strBuf) 
    print("--------------------------------------------------")

def checkVerticalCollision():
    isColliding = False
    # lets firstly see if the shape has just reached the bottom:
    if( (shapes_CurrentShapeLocation[0] + shapes_Rows[shapes_CurrentShapeType] - 1) >= totalRows):
        addShapeToBoard()
        return True
        
    return isColliding
    #   step 1 is find the buffer (5) blocks in the current shape:
    

def addShapeToBoard():  # shape has come to rest, now we need to add it to the Board Locations array:
    global board_blockLocations
    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
        strBuf = str(shapes_defaultMasks[shapes_CurrentShapeType][i])

        for j in range(0, shapes_Cols[shapes_CurrentShapeType], 1):
            if(not((strBuf[j] == "5") or (strBuf[j] == "9"))):
                setBoardBlockLocation(shapes_CurrentShapeLocation[0] + i, shapes_CurrentShapeLocation[1] + j, 1)


while True:
    if(runInit): 
        makeNewShape()
        initialiseBlockArray(board_blockLocations)
        runInit = False
        print("init")

    makeNextFrame()
    sleep(100)
    
    
    if(button_a.was_pressed()):
        moveShapeHorizontally(-1)

    if(button_b.was_pressed()):
        moveShapeHorizontally(1)    