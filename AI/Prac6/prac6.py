import math
from tabulate import tabulate

# Constants
AI = 'O'
HUMAN = 'X'
EMPTY = '_'

# Function to print the board using tabulate
def print_board(board):
    print(tabulate(board, tablefmt="grid"))

# Function to check for a winner
def check_winner(board):
    winning_combinations = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    
    if [AI, AI, AI] in winning_combinations:
        return 10
    elif [HUMAN, HUMAN, HUMAN] in winning_combinations:
        return -10
    return 0

# Function to check if moves are left
def is_moves_left(board):
    for row in board:
        if EMPTY in row:
            return True
    return False

# Minimax algorithm
def minimax(board, depth, is_max):
    score = check_winner(board)

    # Base cases
    if score == 10:
        return 1  # AI Win
    if score == -10:
        return -1  # AI Lose
    if not is_moves_left(board):
        return 0  # Draw

    if is_max:  # Maximizing AI
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    move_value = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY  # Undo move
                    best = max(best, move_value)
        return best

    else:  # Minimizing HUMAN
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    move_value = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY  # Undo move
                    best = min(best, move_value)
        return best

# Find the Best Move for AI with compact horizontal utility table
def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)
    
    # Store moves and their utility values
    positions = []
    values = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY  # Undo move
                
                positions.append(f"({i},{j})")
                values.append(move_val)
                
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    
    # Print compact horizontal utility table
    utility_table = [
        ["Moves"] + positions,
        ["Values"] + values
    ]
    print("\nUtility Values:")
    print(tabulate(utility_table, tablefmt="grid"))
    
    print(f"\nAI chooses: ({best_move[0]},{best_move[1]}) with value: {best_val}")
    return best_move

# Function for human to play their move
def human_move(board):
    while True:
        try:
            row = int(input("Row (0-2): "))
            col = int(input("Col (0-2): "))

            if board[row][col] == EMPTY:
                board[row][col] = HUMAN
                break
            else:
                print("Cell occupied! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Use 0-2.")

# Main Game Loop
def play_game():
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    
    print("Tic-Tac-Toe\nYou: X, AI: O")
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            print("Your Turn!")
            human_move(board)
        else:
            best_move = find_best_move(board)
            board[best_move[0]][best_move[1]] = AI

        print_board(board)

        # Check if there's a winner
        score = check_winner(board)
        if score == 10:
            print("AI Wins!")
            return
        elif score == -10:
            print("You Win!")
            return
        elif not is_moves_left(board):
            print("Draw!")
            return

# Run the Game
if __name__ == "__main__":
    play_game()