import random

"""
Create a board for mines and for the player
"""

#Board player can not see
board =[[0,0,0,0,0],   #0= no mine
        [0,0,0,0,0],   #1= mine
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]]


#Board player can see
boardVisible = [[-1,-1,-1,-1,-1],  #-1=unkown
                [-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1]]


#add mines
numMines = 7
num = 0 #num mines
while num < numMines:
    row=random.randint(0, 4)
    col=random.randint(0, 4)
    if board[row][col] == 0:
        board[row][col]= 1 #add mine
        num = num+1

"""
Essential for testing if the mines were added correctly.
It will be displayed when player steps on a mine.
"""
def displayBoard():
    for row in range(0,5):
        for col in range(0,5):
            print(board[row][col], end=" ")
        print("")

#Will show the board to Player without revealing mines´s locations
def displayBoardVisible():
    print("-"*21)
    for row in range(0,5):
        print("| ", end="")
        for col in range(0,5):
            if boardVisible[row][col] == -1:
                print(" ", end= " | ")
            else:
                print(boardVisible[row][col], end=" | ")
        print("")
        print("-"*21)

def checkMinesAround(row, col):
    totalMines = 0 #total mines around location
    r= row -1
    while r <= row+1:
        if r >=0 and r <5:
            c= col -1
            while c <= col+1:
                if c >=0 and c <5:
                    totalMines=totalMines+board[r][c]
                c=c+1
        r=r+1
    return totalMines

displayBoard()
displayBoardVisible()

movement=0
while movement < (25 - numMines):
    row= int(input("Select a row(1-5): ")) - 1
    col= int(input("Select a col(1-5): ")) - 1
    if board[row][col] == 1:
        print("Ooops!!! You stepped on a mine.")
        displayBoard()
    else:
        boardVisible[row][col] = checkMinesAround(row, col)
        displayBoardVisible()