import random
import os
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('minefield')

ranking_worksheet = SHEET.worksheet("ranking")
ranking_scores = ranking_worksheet.get_all_values()

def clear_screen():
    """
    Clear function to clean-up the terminal so things don't get messy.
    """
    os.system("cls" if os.name == "nt" else "clear")

def get_name_data():
    """
    Get name input from the player
    """
    while True:
        data_str = input("Please enter your name here: ")
        if data_str.isalpha():
            return data_str
        else:
            print(f"{data_str} is not a name.")

def displayRanking():
    """
    Print current Ranking
    """
    clear_screen()
    print(f"TOP RANKING")
    col_len = {i: max(map(len, inner))
                for i, inner in enumerate(zip(*ranking_scores))}

    for inner in ranking_scores:
        for col, word in enumerate(inner):
            print(f"{word:{col_len[col]}}", end=" | ")
        print()
    print()

def menu(get_name_data):
    """
    Menu to begin game, play game, check ranking, quit game
    """
    while True:
        print(f"{get_name_data}, what would you like to do?")
        print("Press 1 to play game")
        print("Press 2 to check ranking")
        print("Press 3 to quit game")
        number = input()
        if number == "1":
            break
        elif number == "2":
            displayRanking()
        elif number == "3":
            print(f"Goodbye {get_name_data}!")
            quit()
        else:
            clear_screen()
            print(f"{number} is not valid.")

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


def displayBoard():
    """
    Essential for adding the mines correctly.
    Also necessary to find the exact number of mines around a spot.
    It will be displayed when player steps on a mine.
    """
    for row in range(0,5):
        for col in range(0,5):
            print(board[row][col], end=" ")
        print("")

def displayBoardVisible():
    """
    Will show the board to Player without revealing mines´s locations
    """
    clear_screen()
    print("""
RULES:
1. Select a row number from 1 to 5.
2. Select a column number from 1 to 5.

For every correct movement you will get 100 points.
""")
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
    """
    Display the number of mines around the coordinates given 
    """
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

def updateMinesAround(rowValue, colValue):
    """
    In case of zeros, it will check the next 
    spaces until it finds at least one mine
    """
    totalOpened= 0
    if boardVisible[rowValue][colValue] == -1: #not yet opened
        numMines= checkMinesAround(rowValue, colValue)
        boardVisible[rowValue][colValue]=numMines
        totalOpened= totalOpened+1
        #if was 0, it´s safe to reveal
        if numMines == 0:
            r=rowValue - 1
            while r <= rowValue+1:
                if r >=0 and r <5:
                    c= colValue -1
                    while c <= colValue+1:
                        if c >=0 and c <5:
                            totalOpened= totalOpened+updateMinesAround(r, c)
                        c=c+1
                r=r+1
    return totalOpened

def game():
    """
    it receives the row and column numbers, calculate position
    and total score
    """
    score = 0
    movement = 0
    while movement < (25 - numMines):
        row = input("Select a row(1-5): ")
        if row == "1" or row == "2" or row == "3" or row == "4" or row == "5":
            rowValue = int(row) - 1
            col = input("Select a col(1-5): ")
            if col == "1" or col == "2" or col == "3" or col == "4" or col == "5":
                colValue = int(col) - 1
                if board[rowValue][colValue] == 1:
                    print("Ooops!!! You stepped on a mine.")
                    print("Score: " +str(score)+" Points") #Display final score
                    displayBoard()
                    break
                else:
                    movement= movement+updateMinesAround(rowValue, colValue)
                    displayBoardVisible()
                    score = score + 100 #It will add 100 Points for each correct movement
                    print("Score: " +str(score)+" Points")
            else:
                print(f"{col} is not valid!")
        else:
            print(f"{row} is not valid!")
    if movement > (24 - numMines):
        print("You have won!")
        return score
    else:
        print("You have lost, Game Over!")
        return score

def get_ranking_data(name, score):
    """
    Collect name and sccore data
    """
    ranking_data_str = name+","+str(score)
    ranking_data = ranking_data_str.split(",")
    return ranking_data

def update_ranking_worksheet(name, score):
    """
    Update ranking worksheet with name and score
    """
    ranking_worksheet.append_row(get_ranking_data(name, score))

def main():
    clear_screen()
    print("Welcome to Minefield.\n")
    print("Explore all spaces without exploding any mine inside this field.")
    print("There are seven mines, so be careful where you step on.\n")
    name = get_name_data()
    menu(name)
    displayBoardVisible()
    score = game()
    update_ranking_worksheet(name, score)
    #menu(name)
    #print("Thanks for playing :)")

main()