from microbit import*
import radio
radio.on()
radio.config(length=25, queue=20, channel=19, power=6)

global totalRows
global totalCols
totalRows = 10
totalCols = 8

shape_Square = [22, 33, 55]
shape_Long = [444, 555]
shape_LeftUp = [255, 344, 555]
shape_RightUp = [552, 443, 555]
shape_MiddleUp = [525, 434, 555]
shape_UpSquiggle = [255, 342, 554, 995]

shapes_Rows = [3, 2, 3, 3, 3, 4]
shapes_Cols = [2, 1, 3, 3, 3, 3]

shapes_defaultMasks = [ shape_Square, 
                        shape_Long, 
                        shape_LeftUp, 
                        shape_RightUp, 
                        shape_MiddleUp, 
                        shape_UpSquiggle]

global shapes_CurrentShapeType
shapes_CurrentShapeType = 5

global shapes_CurrentShapeLocation
shapes_CurrentShapeLocation = [2, 3]        #   2 = row, 3 = col

global currentAnimationRow
currentAnimationRow = 0


def makeNextFrame():
    #startTime = 
    moveShapeDown()
    # if animation frame = 0 clear the row above... build a generic clear row function and rem to parametise whether row is being 
    # cleared cos block has shifted or cos of a tetris... in the case of the latter an animation is triggered in the node.
    for i in range(0, shapes_Rows[shapes_CurrentShapeType], 1):
        print(makeNextRowCommand(i))
    print("----------------------------")


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
    currentAnimationRow = currentAnimationRow + 1
    if(currentAnimationRow == 5):
        currentAnimationRow = 0
        clearRow(shapes_CurrentShapeLocation[0])
        shapes_CurrentShapeLocation[0] = shapes_CurrentShapeLocation[0] + 1

def clearRow(rowNum):
    print("tX1210" + getPaddedRowRefStr(rowNum))


while True:
        
    makeNextFrame()
    sleep(1000)
    
    if(button_a.was_pressed()):
        moveShapeHorizontally(-1)

    if(button_b.was_pressed()):
        moveShapeHorizontally(1)    