from microbit import*
import radio

radio.on()
radio.config(length=25, queue=20, channel=19, power=6)

nodeID = 35

global totalRows
global totalCols
totalRows = 10
totalCols = 10

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

image_AnimationPresets_FadeOut =    [   "00000:99999:99999:99999:99999",
                                        "00000:00000:99999:99999:99999",
                                        "00000:00000:00000:99999:99999",
                                        "00000:00000:00000:00000:99999",
                                        image_SpecialPreset_Null
                                        ]


image_AnimationPresets_FadeIn =     [   "99999:00000:00000:00000:00000",
                                        "99999:99999:00000:00000:00000",
                                        "99999:99999:99999:00000:00000",
                                        "99999:99999:99999:99999:00000",
                                        image_SpecialPreset_Full
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

    print("Message is from server.  Target row = + " +rawMsg[6 : 8] + " - rowRef = " + str(getRowRef()))

    if(rawMsg[2 : 3] == "0"):   processServerInstruction(rawMsg)
    
    if( (rawMsg[2 : 3] == "1") and (int(rawMsg[6 : 8]) == getRowRef()) ):
            if(rawMsg[3 : 5] == "20"): processImageMessage(rawMsg)
            if(rawMsg[3 : 5] == "21"): 
                print("Clear screen")
                display.clear()
            if(rawMsg[3 : 5] == "22"): 
                print("Destruction!")
                runBlockDestroySequence()


def processImageMessage(rawMsg):                                    #   tX12005100101 = tX12005  +  100101
    rawMsgRef = 7 + getColRef()                                     #   take pos of node in row (col ref) and displaces it 7 chars to right
    blockType = int(rawMsg[rawMsgRef])
    animationFrame = int(rawMsg[5])
    print("Animation frame = " + str(animationFrame))

    displayCorrectImage(blockType, animationFrame)

    #newDisplayImageRef = int(rawMsg[rawMsgRef : (rawMsgRef+ 1) ])   #   gets the bit that corresponds to the position of the node in this row   
    #display.show(Image(imagePresets[newDisplayImageRef]))
 
def displayCorrectImage(blockType, animationFrame):
    print("Block type = " + str(blockType))

    if(blockType == 0): return

    if(blockType == 9):
        display.clear()
        return

    if((blockType == 1) or (blockType == 3)):
        display.show(Image(image_SpecialPreset_Full))
        return

    if((blockType == 2) or (blockType == 4)):           # fading out...
        display.show(Image(image_AnimationPresets_FadeOut[animationFrame]))
        return

    if(blockType == 5):                                 # fading in...
        display.show(Image(image_AnimationPresets_FadeIn[animationFrame]))

    return


 
def processServerInstruction(rawMsg):
    instructionType = int(rawMsg[3 : 5])
    print(str(instructionType))
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

def runBlockDestroySequence():
    display.show(Image("09990:99999:99999:99999:09990"))
    sleep(50)
    display.show(Image("00900:09990:99999:09990:00900"))
    sleep(50)
    display.show(Image("00900:00900:99999:00900:00900"))
    sleep(50)
    display.show(Image("00000:00900:09990:00900:00000"))
    sleep(50)
    display.show(Image("00000:00000:00900:00000:00000"))
    sleep(50)
    display.clear()


def testBlockTypes():
    #nodeID = 34         # Block Type 2
    nodeID = 35         # Block Type 3
    #nodeID = 36         # Block Type 4
    #nodeID = 37         # Block Type 5
    print("tX120003000255500")
    processServerMessage("tX120003000234500")
    sleep(1000)
    print("tX120103000255500")
    processServerMessage("tX120103000234500")
    sleep(1000)
    print("tX120203000255500")
    processServerMessage("tX120203000234500")
    sleep(1000)
    print("tX120303000255500")
    processServerMessage("tX120303000234500")
    sleep(1000)    
    print("tX120403000255500")
    processServerMessage("tX120403000234500")
    sleep(1000)    
   

while True:
    sleep(10)
    #processServerMessage(getServerMessage())
    runBlockDestroySequence()
    #testBlockTypes()
    
    
