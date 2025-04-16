# Terminals and precedence table (i represents id)
terminals = ['i', '+', '*', '$']
precedence_table = [
    ['-', '>', '>', '>'],  # i (represents id)
    ['<', '>', '<', '>'],  # +
    ['<', '>', '>', '>'],  # *
    ['<', '<', '<', ' ']   # $
]

def get_top_terminal(stack):
    for i in range(len(stack) - 1, -1, -1):
        if stack[i] != "E":
            return stack[i]
    return "$"

def get_index(symbol):
    for i in range(len(terminals)):
        if terminals[i] == symbol:
            return i
    return -1

def reduce(stack):
    handle = ""
    temp = []
    
    while stack:
        symbol = stack.pop()
        temp.append(symbol)
        handle = symbol + handle
        
        if handle == "id" or handle == "E+E" or handle == "E*E":
            stack.append("E")
            return handle
    
    return ""

def parse(input_str):
    stack = ['$']
    input_index = 0
    print("\nStack\t\tInput\t\tAction")
    print("-------------------------------------")
    
    while True:
        # Print current state
        print(f"{''.join(stack)}\t\t{input_str[input_index:]}\t\t", end="")
        
        # Get current input symbol
        if input_index < len(input_str):
            if input_str.startswith("id", input_index):
                current_input = "id"
            else:
                current_input = input_str[input_index]
        else:
            current_input = "$"
        
        # Get the topmost terminal in stack
        top_terminal = get_top_terminal(stack)
        
        # Get relation between top terminal and current input
        top_symbol = 'i' if top_terminal == "id" else top_terminal[0]
        curr_symbol = 'i' if current_input == "id" else current_input[0]
        
        top_index = get_index(top_symbol)
        curr_index = get_index(curr_symbol)
        
        relation = precedence_table[top_index][curr_index]
        
        if relation == '<' or relation == '=':
            stack.append(current_input)
            print("Shift")
            input_index += len(current_input)
        elif relation == '>':
            rule = reduce(stack)
            print(f"Reduce E -> {rule}")
        elif top_terminal == "$" and current_input == "$":
            print("Accept")
            break
        else:
            print("Error")
            break

# Main program
input_str = "id+id*id$"

# Print precedence table
print("\nPrecedence Table:")
print(" i + * $")
print("------------------")

for i in range(len(terminals)):
    print(f"{terminals[i]} | ", end="")
    for j in range(len(terminals)):
        if i == 3 and j == 3:
            print("accept ", end="")
        print(f"{precedence_table[i][j]} ", end="")
    print()

parse(input_str)