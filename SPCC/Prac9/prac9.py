import os

# Check if the expression is a constant value
def is_constant(expr):
    try:
        # Try evaluating the expression, if it evaluates, it's a constant
        eval(expr)
        return True
    except:
        # If it fails (e.g., contains variables), it's not a constant
        return False

# Evaluate the expression and return its value as a string
def evaluate(expr):
    try:
        return str(eval(expr))  # Evaluate and return as string
    except:
        return expr  # If not evaluable, return the original expression

# Perform the optimization process on the given lines of code
def optimize_code(lines):
    optimized = []
    constants = {}  # Store constant values
    copies = {}  # Store copy assignments for copy propagation
    expressions = {}  # Store subexpressions for common subexpression elimination

    for line in lines:
        if "=" not in line:
            optimized.append(line)
            continue  # Skip lines that do not contain an assignment

        lhs, rhs = line.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()

        # 1. Constant folding: If rhs is constant, evaluate it
        if is_constant(rhs):
            val = evaluate(rhs)
            constants[lhs] = val
            optimized.append(f"{lhs} = {val}")
            continue  # Skip further processing for constant assignments

        # 2. Copy propagation: If rhs is a variable, check if it is a copy of another variable
        if rhs.isidentifier():
            while rhs in copies:  # Replace with the original variable if it's a copy
                rhs = copies[rhs]
            copies[lhs] = rhs  # Track the copy propagation
            continue  # Skip adding direct copies to the optimized code

        # 3. Replace variables in rhs using the copies dictionary
        tokens = ""
        token = ""
        for ch in rhs:
            if ch.isalnum() or ch == "_":  # If the character is part of a variable
                token += ch
            else:
                if token:
                    token = copies.get(token, token)  # Replace with copy if needed
                    tokens += token
                    token = ""
                tokens += ch  # Add non-alphanumeric characters (operators, etc.)
        if token:  # If there's a final token left
            token = copies.get(token, token)
            tokens += token
        new_rhs = tokens

        # 4. Common Subexpression Elimination: Replace known subexpressions with stored variables
        replaced_rhs = new_rhs
        for expr, var in expressions.items():
            if expr in replaced_rhs:  # Replace any known subexpression
                replaced_rhs = replaced_rhs.replace(expr, var)

        expressions[new_rhs] = lhs  # Track the new expression for possible future elimination
        optimized.append(f"{lhs} = {replaced_rhs}")
        copies[lhs] = lhs  # Record that lhs is assigned to itself (copy) 

    return optimized

# Main function to run the program
def main():
    print("Working directory:", os.getcwd())

    try:
        # Read input file and strip empty lines
        with open(r"C:\Users\Admin\Desktop\BE\sem 6\SPCC\Prac9\src.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
        return

    print("\n--- Input Code (Before Optimization) ---")
    for line in lines:
        print(line)

    # Perform code optimization
    optimized = optimize_code(lines)

    print("\n--- Output Code (After Optimization) ---")
    for line in optimized:
        print(line)

if __name__ == "__main__":
    main()
