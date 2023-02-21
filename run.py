import random
import os
import gspread
from google.oauth2.service_account import Credentials


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
        data_str = input("Please enter your name here:\n")
        if data_str.isalpha():
            return data_str
        else:
            print(f"{data_str} is not a name.")


def display_ranking():
    """
    Print current Ranking
    """
    clear_screen()
    print("TOP RANKING")
    col_len = {
        i: max(map(len, inner)) for i, inner in enumerate(zip(*ranking_scores))
    }

    for inner in ranking_scores:
        for col, word in enumerate(inner):
            print(f"{word:{col_len[col]}}", end=" | ")
        print()
    print()


def menu(user_name):
    """
    Menu to begin game, play game, check ranking, quit game
    """
    while True:
        print(f"{user_name}, what would you like to do?")
        print("Press 1 to play game")
        print("Press 2 to check ranking")
        print("Press 3 to quit game")
        number = input()
        if number == "1":
            break
        if number == "2":
            display_ranking()
            return 2
        if number == "3":
            print(f"Goodbye {user_name}!")
            return 3
        clear_screen()
        print(f"{number} is not valid.")
    return 1


def display_board(board):
    """
    Essential for adding the mines correctly.
    Also necessary to find the exact number of mines around a spot.
    It will be displayed when player steps on a mine.
    """
    print("-"*21)
    for row in range(0, 5):
        print("| ", end="")
        for col in range(0, 5):
            if board[row][col] == 1:
                print("*", end=" | ")
            else:
                print(board[row][col], end=" | ")
        print("")
        print("-"*21)


def display_board_visible(board_visible):
    """
    Will show the board to Player without revealing mines's locations
    """
    clear_screen()
    print("""
RULES:
1. Select a row number from 1 to 5.
2. Select a column number from 1 to 5.

For every correct movement you will get 100 points.
""")
    print("-"*21)
    for row in range(0, 5):
        print("| ", end="")
        for col in range(0, 5):
            if board_visible[row][col] == - 1:
                print(" ", end=" | ")
            else:
                print(board_visible[row][col], end=" | ")
        print("")
        print("-"*21)


def check_mines_around(row, col, board):
    """
    Display the number of mines around the coordinates given
    """
    total_mines = 0  # total mines around location
    r = row - 1
    while r <= row+1:
        if r >= 0 and r < 5:
            c = col - 1
            while c <= col + 1:
                if c >= 0 and c < 5:
                    total_mines = total_mines + board[r][c]
                c = c + 1
        r = r + 1
    return total_mines


def update_mines_around(row_value, col_value, board_visible, board):
    """
    In case of zeros, it will check the next
    spaces until it finds at least one mine
    """
    total_opened = 0
    if board_visible[row_value][col_value] == - 1:  # not yet opened
        num_mines = check_mines_around(row_value, col_value, board)
        board_visible[row_value][col_value] = num_mines
        total_opened = total_opened + 1
        # if was 0, it´s safe to reveal
        if num_mines == 0:
            r = row_value - 1
            while r <= row_value + 1:
                if r >= 0 and r < 5:
                    c = col_value - 1
                    while c <= col_value + 1:
                        if c >= 0 and c < 5:
                            total_opened += update_mines_around(
                                r, c, board_visible, board
                                )
                        c = c + 1
                r = r + 1
    return total_opened


def game(board_visible, board):
    """
    it receives the row and column numbers, calculate position
    and total score.
    """
    score = 0
    movement = 0
    while movement < (25 - num_mines):
        row = input("Select a row(1-5):\n")
        if row in ("1", "2", "3", "4", "5"):
            row_value = int(row) - 1
            col = input("Select a col(1-5):\n")
            if col in ("1", "2", "3", "4", "5"):
                col_value = int(col) - 1
                if board[row_value][col_value] == 1:
                    print("Ooops!!! You stepped on a mine.")
                    print(f"Score: {score} Points")  # Display final score
                    display_board(board)
                    break
                movement += update_mines_around(
                    row_value, col_value, board_visible, board
                    )
                display_board_visible(board_visible)
                # It will add 100 Points for each correct movement
                score = score + 100
                print(f"Score: {score} Points")
            else:
                print(f"{col} is not valid!")
        else:
            print(f"{row} is not valid!")
    if movement > (24 - num_mines):
        print("You have won!")
        return score
    else:
        print("You have lost, Game Over!")
        return score


def get_ranking_data(name, score):
    """
    Collect name and sccore data
    """
    ranking_data_str = name + "," + str(score)
    ranking_data = ranking_data_str.split(",")
    return ranking_data


def update_ranking_worksheet(name, score):
    """
    Update ranking worksheet with name and score
    """
    ranking_worksheet.append_row(get_ranking_data(name, score))


def main():
    """
    Contains all functions
    """
    clear_screen()
    print("Welcome to Minefield.\n")
    print("Explore all spaces without exploding any mine inside this field.")
    print("There are seven mines, so be careful where you step on.\n")
    name = get_name_data()
    play = menu(name)
    while play == 1:
        # Board player can not see
        board = create_board(True)
        # Board player can see
        board_visible = create_board()
        # Add mines
        num = 0  # num mines
        while num < num_mines:
            row = random.randint(0, 4)
            col = random.randint(0, 4)
            if board[row][col] == 0:
                board[row][col] = 1  # Add mine
                num = num + 1
        display_board_visible(board_visible)
        score = game(board_visible, board)
        update_ranking_worksheet(name, score)
        play = menu(name)


def create_board(hidden=False):
    board = []
    for i in range(5):
        row = []
        for j in range(5):
            if hidden is True:
                row.append(hidden_space)
            else:
                row.append(empty_space)
        board.append(row)
    return board


if __name__ == '__main__':
    empty_space = -1
    mine = 1
    hidden_space = 0

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
    num_mines = 7
main()
