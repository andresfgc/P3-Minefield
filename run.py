import random
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
"""
ranking = SHEET.worksheet('ranking')
ranking_scores = ranking.get_all_values()
"""

def get_name_data():
    """
    Get name input from the player
    """
    data_str = input("Please enter your name here: ")
    print(f"Thanks {data_str}, let's play!")

get_name_data()
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
Essential for adding the mines correctly.
Also necessary to find the exact number of mines around a spot.
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

#Display the number of mines around the coordinates given
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

#In case of zeros, it will check the next spaces until it finds at least one mine
def updateMinesAround(row, col):
    totalOpened= 0
    if boardVisible[row][col] == -1: #not yet opened
        numMines= checkMinesAround(row, col)
        boardVisible[row][col]=numMines
        totalOpened= totalOpened+1
        #if was 0, it´s safe to reveal
        if numMines == 0:
            r=row - 1
            while r <= row+1:
                if r >=0 and r <5:
                    c= col -1
                    while c <= col+1:
                        if c >=0 and c <5:
                            totalOpened= totalOpened+updateMinesAround(r, c)
                        c=c+1
                r=r+1
    return totalOpened
"""
#Adds user data to ranking
def update_ranking(player):
    for count, score in enumerate(ranking_scores[1:11], 2):
        if player.score > int(score[2]):
            player_as_list = [player.name, player.place, player.score]
            ranking.append_row(player_as_list)
            ranking.sort((3, 'des'), range='A2:C999')
            ranking.delete_rows(12)
            break
        

#print current leaderboard
def displayRanking():
    clear_screen()
    print(f"TOP 10 RANKING")
    col_len = {i:max(map(len, inner))
        for i, inner in enumerate(zip(ranking_scores))}

        for inner in ranking_scores:
            for col, word in enumerate(inner):
                print(f"{word:{col_len[col]}}", end= " | ")
            print()
        print()
        input("Press enter to return to main menu\n")
        clear_screen()


#Player class used to creater player object containing name and score
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = 0

#Ask player for name
def playerDetails():
    player_name = input("What is your name?\n").upper()
    if player_name.isalpha():
        player = Player(name=player_name, score=0)
        return player
    else:
        clear_screen()
        print(f"{player_name} is not valid")
"""

def main():
    displayBoard()
    displayBoardVisible()
    print(ranking_scores)
    score=0
    movement=0
    while movement < (25 - numMines):
        row= int(input("Select a row(1-5): ")) - 1
        col= int(input("Select a col(1-5): ")) - 1
        if board[row][col] == 1:
            print("Ooops!!! You stepped on a mine.")
            print("Score: " +str(score)+" Points") #Display final score
            displayBoard()
            break
        else:
            movement= movement+updateMinesAround(row, col)
            displayBoardVisible()
            score = score + 100 #It will add 100 Points for each correct movement
            print("Score: " +str(score)+" Points")
    if movement > (24 - numMines):
        print("You have won!")
    else:
        print("You have lost, Game Over!")

"""
if __name__ == '__main__':
    main()
"""