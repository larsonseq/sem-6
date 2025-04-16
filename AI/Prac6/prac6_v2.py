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
        return 'AI_WIN'
    elif [HUMAN, HUMAN, HUMAN] in winning_combinations:
        return 'HUMAN_WIN'
    return None

# Function to check if moves are left
def is_moves_left(board):
    for row in board:
        if EMPTY in row:
            return True
    return False

# Function to count potential winning lines
def count_potential_lines(board, player):
    count = 0
    opponent = HUMAN if player == AI else AI
    
    # Check rows, columns, and diagonals
    for i in range(3):
        # Check rows
        row = board[i]
        if opponent not in row:
            count += row.count(player)
            
        # Check columns
        col = [board[j][i] for j in range(3)]
        if opponent not in col:
            count += col.count(player)
    
    # Check diagonals
    diag1 = [board[i][i] for i in range(3)]
    if opponent not in diag1:
        count += diag1.count(player)
        
    diag2 = [board[i][2-i] for i in range(3)]
    if opponent not in diag2:
        count += diag2.count(player)
        
    return count

# Enhanced minimax algorithm with better utility values
def minimax(board, depth, is_max):
    result = check_winner(board)
    
    # Base cases with depth-aware scoring
    if result == 'AI_WIN':
        return 100 - depth  # AI wins sooner is better (higher score)
    if result == 'HUMAN_WIN':
        return depth - 100  # Human wins later is better (less negative)
    if not is_moves_left(board):
        return 0  # Draw
    
    # Calculate positional value based on potential winning lines
    ai_potential = count_potential_lines(board, AI)
    human_potential = count_potential_lines(board, HUMAN)
    position_value = ai_potential - human_potential
    
    if is_max:  # Maximizing AI
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    move_value = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY  # Undo move
                    best = max(best, move_value)
        return best + position_value/10  # Add positional value as a smaller factor

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
                values.append(round(move_val, 2))
                
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
     
    utility_table = [
        ["Moves"] + positions,
        ["Values"] + values
    ]
    print("\nUtility Values:")
    print(tabulate(utility_table, tablefmt="grid"))
    
    print(f"\nAI chooses: ({best_move[0]},{best_move[1]}) with value: {round(best_val, 2)}")
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
        result = check_winner(board)
        if result == 'AI_WIN':
            print("AI Wins!")
            return
        elif result == 'HUMAN_WIN':
            print("You Win!")
            return
        elif not is_moves_left(board):
            print("Draw!")
            return

# Run the Game
if __name__ == "__main__":
    play_game()