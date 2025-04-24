import math
from tabulate import tabulate

AI = 'x'
HUMAN = 'o'
EMPTY = " "


def print_board(board):
    print(tabulate(board, tablefmt="grid"))


def human_move(board):
    while True:
        try:
            row = int(input("Enter row: ").strip())
            col = int(input("Enter col: ").strip())

            if board[row][col] == EMPTY:
                board[row][col] = HUMAN
            else:
                print("Invalid Move!!  Try Again")
                continue
        except:
            print("Enter Valid Input: 0 - 2")
# ------------------------------------------------------


def find_best_move(board):
    best_val = -math.inf 
    best_move = (-1, -1)

    # Stroe moves and their utility values
    positions = []
    values = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                # Now Undo Move
                board[i][j] = EMPTY

                positions.append(f"({i}, {j})")
                values.append(round(move_val, 2))
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    utility_table = [
        ["Moves"] + positions,
        ["Values"] + values
    ]

    print("\nUtility Values: ")
    print(tabulate(utility_table, tablefmt="grid"))

    print(f"AI Chooses: ({best_move}), with value {round(best_val, 2)}")

    return best_move
# -------------------------------------------------------------------------


def minimax(board, depth, is_max):
    result = check_winner(board)

    if result == "AI_WIN":
        return 100 - depth
    if result == "HUMAN_WIN":
        return depth - 100
    if not is_moves_left(board):
        return 0
    
    # calculate positional value based on potential winning lines
    ai_potential = count_potential_lines(board, AI)
    human_potential = count_potential_lines(board, HUMAN)
    potential_value = ai_potential - human_potential

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    move_value = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best = max(best, move_value)
        return best - position_value/10

    else:  # Minimizing HUMAN
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    move_value = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY  # Undo move
                    best = min(best, move_value)
        return best - position_value/10  # Subtract positional value as a smaller factor









def play_game():
    board = [
        [EMPTY] * 3,
        [EMPTY] * 3,
        [EMPTY] * 3
    ]

    print("TIC-TAC-TOE \nYou: x \tAI: o")
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            print("Your Move")
            human_move(board)
        else:
            best_move = find_best_move(board)
            board[best_move[0]][best_move[1]] = AI

        print(board)

        # Check if Theres a winner
        result = check_winner(board)
        if result == "AI_WIN":
            print("AI Has Won!!!")
            return
        elif result = "HUMAN_WIN":
            print("Congrats You Have Won")
            return
        elif not is_moves_left(board):
            print("Its a Draw")
            return
# --------------------------------------------------


if __name__ == "__main__":
    play_game()