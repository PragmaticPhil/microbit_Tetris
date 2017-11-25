from microbit import*
import radio
radio.on()
radio.config(length=50, queue=11, channel=11, power=6)

global totalRows
global totalCols
totalRows = 10
totalCols = 8


shape_AtRest_Square_2x2 = [67, 34]
shape_AtRest_Long_1x3 = [627]
shape_AtRest_LeftUp_2x3 = [800, 314]
shape_AtRest_RightUp_2x3 = [008, 314]
shape_AtRest_MiddleUp_2x3 = [080, 314]

shape_Square_2x2 = [11, 11]
shape_Long_1x3 = [111]
shape_LeftUp_2x3 = [100, 111]
shape_RightUp_2x3 = [001, 111]
shape_MiddleUp_2x3 = [010, 111]



shapes_Rows = [2, 1, 2, 2, 2]                          #   [22, 13, 23, 23, 23]
shapes_Cols = [2, 1, 3, 3, 3]

shapes_defaultMasks = [ shape_Square_2x2, 
                        shape_Long_1x3, 
                        shape_LeftUp_2x3, 
                        shape_RightUp_2x3, 
                        shape_MiddleUp_2x3]


global shapes_CurrentShapeType
shapes_CurrentShapeType = 2

global shapes_CurrentShapeLocation
shapes_CurrentShapeLocation = [2, 3]

global currentAnimationRow
currentAnimationRow = 0


def increaseAnimationRow():
    global currentAnimationRow
    currentAnimationRow = (currentAnimationRow + 1) % 5
    

def makeNextRowCommand(rowRef):
    return ("tX120" + getPaddedRowRefStr(rowRef) + makeRowMask(rowRef))
    
def getPaddedRowRefStr(rowRef):
    if (rowRef < 10):   return "0" + str(rowRef)
    return str(rowRef)


def makeRowMask(rowRef):
    strBuf = "_"
    for i in range(0, shapes_CurrentShapeLocation[1], 1):   strBuf  = strBuf  + "0"
        
    strBuf  = strBuf  + str(shapes_defaultMasks[shapes_CurrentShapeType][rowRef])
    
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
    print("--------------------------------------------------")
    print("Direction = " + str(moveDir) +", width = " + str(shapes_Cols[shapes_CurrentShapeType]) + ", Pos = " + str(shapes_CurrentShapeLocation[1]))    


def moveShapeDown():
    global currentAnimationRow
    global shapes_CurrentShapeLocation
    currentAnimationRow = currentAnimationRow + 1
    if(currentAnimationRow == 5):
        currentAnimationRow = 0
        shapes_CurrentShapeLocation[0] = shapes_CurrentShapeLocation[0] + 1



while True:
    print(makeNextRowCommand(1))
    sleep(1000)
    
    if(button_a.was_pressed()):
        moveShapeHorizontally(-1)

    if(button_b.was_pressed()):
        moveShapeHorizontally(1)    