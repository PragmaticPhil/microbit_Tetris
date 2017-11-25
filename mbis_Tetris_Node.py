from microbit import*
import radio
radio.on()
radio.config(length=50, queue=11, channel=11, power=6)

nodeID = 19

global totalRows
global totalCols
totalRows = 1
totalCols = nodeID + 1

image_SpecialPreset_Full = "99999:99999:99999:99999:99999"
image_SpecialPreset_Null = "00000:00000:00000:00000:00000"

image_BorderPresets =       [   image_SpecialPreset_Null, 
                                image_SpecialPreset_Full, 
                                "55555:99999:99999:99999:99999", 
                                "59999:59999:59999:59999:59999",
                                "99995:99995:99995:99995:99995",
                                "59995:59995:59995:59995:59995",
                                "55555:59999:59999:59999:59999",
                                "55555:99995:99995:99995:99995",
                                "55555:59995:59995:59995:59995"
                            ]

image_AnimationPresets =    [   image_SpecialPreset_Full,
                                "09999:09999:09999:09999:09999",
                                "00999:00999:00999:00999:00999",
                                "00099:00099:00099:00099:00099",
                                "00009:00009:00009:00009:00009",
                                image_SpecialPreset_Null
                            ]

global updateScreen
updateScreen = False

def getServerMessage():
    try:        return str(radio.receive())
    except:     return "X"


def processServerMessage(rawMsg):
    global updateScreen
    
    if(len(rawMsg) < 5):                return
    if(not(rawMsg[0 : 2] == "tX")):     return

    if(rawMsg[2 : 3] == "0"):                                               processServerInstruction(rawMsg)
    if((rawMsg[2 : 3] == "1") and (int(rawMsg[5 : 7]) == getRowRef())):     processImageMessage(rawMsg)


def processImageMessage(rawMsg):                                    #   tX12005100101 = tX12005  +  100101
    rawMsgRef = 7 + getColRef()                                     #   take pos of node in row (col ref) and displaces it 7 chars to right
    newDisplayImageRef = int(rawMsg[rawMsgRef : (rawMsgRef+ 1) ])   #   gets the bit that corresponds to the position of the node in this row   
    display.show(Image(imagePresets[newDisplayImageRef]))
 
def processServerInstruction(rawMsg):
    instructionType = int(rawMsg[3 : 5])
    #print(str(instructionType))
    if(instructionType == 99): reset()
    if(instructionType == 60): setMatrixDimensions(rawMsg[5 : 7], rawMsg[7 : 9]) 


def setMatrixDimensions(rowStr, colStr):
    global totalRows
    global totalCols
    totalRows = int(rowStr)
    totalCols = int(colStr)

def getColRef():
    return(int(nodeID % totalCols))

def getRowRef():
    return int((nodeID - getColRef()) / totalCols)



while True:
    sleep(10)
    processServerMessage(getServerMessage())
