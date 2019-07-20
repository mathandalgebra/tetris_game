import os
import sys
import zipfile
import random
import math

# Updated Animation Starter Code

from tkinter import *

####################################
# customize these functions
####################################

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    list = [rows,cols,cellSize,margin]
    t = tuple(list)
    return t
    
def init(data):
    # load data.xyz as appropriate
    data.rows = gameDimensions()[0]
    data.cols = gameDimensions()[1]
    data.cellSize = gameDimensions()[2]
    data.margin = gameDimensions()[3]
    data.emptyColor = "blue"
    data.board = []
    data.rowNum = 0
    data.colNum = 0
    data.count = 0    
    data.gameOver = False
    for row in range(data.rows): data.board += [[data.emptyColor] * data.cols]
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    data.tetrisPieces = [ lPiece, oPiece]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    newFallingPiece(data)
    
# Initialize all the starting characteristics of the piece
def newFallingPiece(data):
     randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
     data.shape = data.tetrisPieces[randomIndex]
     data.color = data.tetrisPieceColors[randomIndex]
     print(data.color)
     data.positionY = 25
     if(data.cols % 2 == 0):
        data.colNum = data.cols//2 - 1
     if(data.cols % 2 == 1):
        data.positionX = (data.cols//2) * data.cellSize
        data.colNum = data.cols//2
    #Keeps track of the current row of cursor
     data.currentRowPiece = 0
     data.currentColPiece = data.cols//2 - 1
     data.drow = 0
     data.dcol = 0
     if(data.shape == data.tetrisPieces[0]):
         data.currentColPiece = data.cols//2 - 1 - 1
     if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece) == False):
         gameOver(data)
    
def gameOver(data):
    data.gameOver = True
    
def rotateFallingPiece(data):
    #Store the old data of pieces into temporary local variable
    oldPieceDimensionRow = len(data.shape)
    oldPieceDimensionCol = len(data.shape[0])
    #Compute the dimension of new data
    newPieceDimensionRow = oldPieceDimensionCol
    newPieceDimensionCol = oldPieceDimensionRow
    #Compute the new location of the Falling Piece
    data.currentRowPiece = data.currentRowPiece + oldPieceDimensionRow // 2 - newPieceDimensionRow // 2
    data.currentColPiece = data.currentColPiece + oldPieceDimensionCol // 2 - newPieceDimensionCol // 2
    #Generate a new 2D list based on the old value. Fill it with None.
    print(data.currentRowPiece,data.currentRowPiece)
    #Generate an empty list with the new dimension
    newPieceList = [[False for i in range(0,oldPieceDimensionRow)]for j in range(0,oldPieceDimensionCol)] 
    print(newPieceList)
    #Put True into the newPieceList
    for i in range(newPieceDimensionRow):
        for j in range(newPieceDimensionCol):
            newPieceList[i][j] = data.shape[j][len(data.shape[0])-1-i]
    data.shape = newPieceList
    
# check if the cell underneath the block is empty color 
def fallingPieceIsLegal(data,currentRow,currentCol):
    if(currentRow < 0 or currentRow + len(data.shape) > data.rows):
        return False
    if(currentCol < 0 or currentCol + len(data.shape[0]) > data.cols):
        return False
    for row in range(len(data.shape)):
        for col in range(len(data.shape[0])):
            if(data.shape[row][col] == True):
                if(data.board[currentRow + row][currentCol + col] != data.emptyColor):
                    return False
    return True

def JustforBottomAndColor(data):
    if((data.currentRowPiece + len(data.shape) > data.rows) == True):
        return False
    # if((data.currentColPiece + len(data.shape[0]) < data.cols) == True):
    for row in range(len(data.shape)):
        for col in range(len(data.shape[0])):
            if(data.shape[row][col] == True):
                if(data.board[data.currentRowPiece + row][data.currentColPiece + col] != data.emptyColor):
                    return False
    return True
#place the Falling Piece onto the Board
def placeFallingPiece(data):
    for row in range(len(data.shape)):
        for col in range(len(data.shape[0])):
            if(data.shape[row][col] == True):
                print(data.currentRowPiece + row,data.currentColPiece + col)
                data.board[data.currentRowPiece + row][data.currentColPiece + col] = data.color
    
    removeBoard(data)
    
# Just move the fallingPiece, disregard other factors
def moveFallingPiece(data,drow,dcol):
    data.currentRowPiece = data.currentRowPiece + drow
    data.currentColPiece = data.currentColPiece + dcol
    # if(data.currentColPiece > 0 and data.currentColPiece + len(data.shape[0]) < data.cols):
    if(JustforBottomAndColor(data) == False):
        data.currentRowPiece = data.currentRowPiece - drow
        data.currentColPiece = data.currentColPiece - dcol
        placeFallingPiece(data) 
        newFallingPiece(data)
        return False
    return True


def removeBoard(data):
    count = 0
    checkBoard = True
    lastRow = data.rows - 1
    #pop the row that is complete, append new list on top. .append(0,
    while(lastRow > 0):
        for col in range(data.cols):
            if(data.board[lastRow][col] == data.emptyColor):
                checkBoard = False
        if(checkBoard == True):
            data.board.insert(0,[data.emptyColor,data.emptyColor,data.emptyColor,data.emptyColor,data.emptyColor,
 data.emptyColor,data.emptyColor,data.emptyColor,data.emptyColor,data.emptyColor])#Insert the blue to First Row
            data.board.pop(lastRow + 1)#Delete the element of last row 
            data.count = data.count + 1
            # data.count = data.count + 1
            # data.row = data.row + 1
        lastRow = lastRow - 1
        
                

    
    
def drawBoard(canvas,data):
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            drawCell(canvas, data,row,col)
    canvas.create_text(data.width/2,12,text = "Score: %d"%data.count)
    
            
def drawCell(canvas, data,rowCur,colCur):
    canvas.create_rectangle(gameDimensions()[3] + colCur * data.cellSize,
    gameDimensions()[3] + rowCur * data.cellSize,
    gameDimensions()[3] + colCur *data.cellSize + data.cellSize,
    gameDimensions()[3] + rowCur * data.cellSize + data.cellSize,
    fill = data.board[rowCur][colCur])
    
def drawFallingPieceCell(canvas, data,rowCur,colCur):
    canvas.create_rectangle(gameDimensions()[3] + colCur * data.cellSize + data.currentColPiece * data.cellSize,
    gameDimensions()[3] + rowCur * data.cellSize + data.currentRowPiece * data.cellSize,
    gameDimensions()[3] + colCur *data.cellSize + data.cellSize + data.currentColPiece * data.cellSize,
    gameDimensions()[3] + rowCur * data.cellSize + data.cellSize + data.currentRowPiece * data.cellSize,
    fill = data.color)

#Draw the piece that falls down
def drawFallingPiece(canvas,data):
    for row in range(len(data.shape)):
        for col in range(len(data.shape[0])):
            if(data.shape[row][col] == True):
                drawFallingPieceCell(canvas,data,row,col)
                
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

#Pressing the key, and change the data. If the data is not legal, redo the move.
def keyPressed(event, data):

    if(event.keysym == "Up"):
        oldShape = data.shape
        oldRow = data.currentRowPiece
        oldCol = data.currentColPiece
        rotateFallingPiece(data)
        if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece) == False):
            data.shape = oldShape
            data.currentRowPiece = oldRow 
            data.currentColPiece = oldCol 
            
    if(event.keysym == "Down"):
        moveFallingPiece(data,1,data.dcol)
        if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece)==False):
            moveFallingPiece(data,-1,data.dcol)
    if(event.keysym == "Right"):
        if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece + 1)==True):
            moveFallingPiece(data,data.drow,1)
        if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece)==False):
            moveFallingPiece(data,data.drow,-1)
    if(event.keysym == "Left"):
        moveFallingPiece(data,data.drow,-1)
        if(fallingPieceIsLegal(data,data.currentRowPiece,data.currentColPiece)==False):
            moveFallingPiece(data,data.drow,1)
    if((event.keysym != "Left") and 
       (event.keysym != "Right") and
       (event.keysym != "Up") and
       (event.keysym != "Down") and
       (event.keysym != "b")):
           newFallingPiece(data)
    

            
    # pass

def timerFired(data):
    moveFallingPiece(data, +1, 0)
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,
    gameDimensions()[3] + gameDimensions()[1] * gameDimensions()[2] + gameDimensions()[3],
    gameDimensions()[3] + gameDimensions()[0] * gameDimensions()[2] + gameDimensions()[3],fill = "yellow")
    drawBoard(canvas,data)
    drawFallingPiece(canvas,data)
    if(data.gameOver == True):
         canvas.create_text(data.width/2,data.height/2,text = "Game is Over",font = "40")
    
    # draw in canvas
    
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris():
    width = gameDimensions()[3] + gameDimensions()[1] * gameDimensions()[2] + gameDimensions()[3]
    height = gameDimensions()[3] + gameDimensions()[0] * gameDimensions()[2] + gameDimensions()[3]
    print(height)
    run(width,height)

playTetris()
    
def _exit():
    if sys.flags.interactive:
        try:
            exit()
            sys.exit()
        except:
            os._exit(0)
    else: sys.exit()

def add_to_zip(path, zipf, required=False):
    if not os.path.exists(path):
        if required:
            print('Fail: Unable to find file %s' % path)
            raise Exception
        return
    print('Adding: %s' % path)
    zipf.write(path)

def intro():
    print("""\
 _ _ ____    ____       _
/ / |___ \  |  _ \ _ __(_)_   _____ _ __
| | | __) | | | | | '__| \ \ / / _ \ '__|
| | |/ __/  | |_| | |  | |\ V /  __/ |
|_|_|_____| |____/|_|  |_| \_/ \___|_|
""")

def main():
    intro()
    zip_name = 'hw6.zip'
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    required_files = ['hw6-tetris.py', 'hw6-clicker.py']
    optional_files = ['hw6-bonus-tetris.py', 'hw6-bonus-dab.py', 'hw6-image.gif']
    try:
        for file in required_files: add_to_zip(file, zipf, required=True)
        for file in optional_files: add_to_zip(file, zipf, required=False)
    except:
        zipf.close()
        os.remove(zip_name)
        _exit()
    zipf.close()
    print("Success!")

if __name__ == '__main__':
    main()
