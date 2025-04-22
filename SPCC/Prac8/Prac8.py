precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'uminus': 3}
temp_counter = 1
three_ac = []

# Function to generate temporary variables
def get_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

# Tokenize the input expression into operators and operands
def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        if expr[i] in '+-*/=()':
            if expr[i] == '-' and (i == 0 or expr[i-1] in '+-*/=('):
                tokens.append('uminus')
            else:
                tokens.append(expr[i])
            i += 1
        elif expr[i].isalnum():
            var = ''
            while i < len(expr) and expr[i].isalnum():
                var += expr[i]
                i += 1
            tokens.append(var)
        else:
            i += 1
    return tokens

# Convert infix expression to postfix notation
def infix_to_postfix(tokens):
    output = []
    stack = []
    for token in tokens:
        if token not in precedence and token not in ('(', ')'):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    print(f"\nPostfix is : {output}\n")
    return output

# Generate Three-Address Code (3AC) from postfix expression
def generate_3ac_from_postfix(postfix):
    stack = []
    for token in postfix:
        if token == 'uminus':
            op = stack.pop()
            temp = get_temp()
            three_ac.append((temp, 'minus', op, ''))
            stack.append(temp)
        elif token in precedence:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = get_temp()
            three_ac.append((temp, op1, token, op2))
            stack.append(temp)
        else:
            stack.append(token)
    return stack.pop()

# Generate Quadruples from the Three-Address Code
def generate_quadruples():
    quads = []
    for instr in three_ac:
        if instr[1] == 'minus':
            quads.append(('minus', instr[2], '', instr[0]))
        elif instr[2] == '=':
            quads.append(('=', instr[1], '', instr[0]))
        else:
            quads.append((instr[2], instr[1], instr[3], instr[0]))
    return quads

# Generate Triples from the Three-Address Code
def generate_triples():
    triples = []
    result_map = {}
    for i, instr in enumerate(three_ac):
        if instr[1] == 'minus':
            operand = instr[2]
            triples.append(('minus', operand, ''))
        elif instr[2] == '=':
            # Assign result of (index of instr[1]) to variable instr[0]
            index = result_map[instr[1]]
            triples.append(('=', instr[0], f'({index})'))
        else:
            op1 = f"({result_map[instr[1]]})" if instr[1] in result_map else instr[1]
            op2 = f"({result_map[instr[3]]})" if instr[3] in result_map else instr[3]
            triples.append((instr[2], op1, op2))
        result_map[instr[0]] = i
    return triples

def main():
    global temp_counter, three_ac
    expr = input("Enter a statement (e.g. a = b * -c + b * -c): ").strip()

    temp_counter = 1
    three_ac = []

    if '=' in expr:
        lhs, rhs = expr.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        tokens = tokenize(rhs)
        postfix = infix_to_postfix(tokens)
        result = generate_3ac_from_postfix(postfix)
        three_ac.append((lhs, result, '=', ''))
    else:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        generate_3ac_from_postfix(postfix)

    # Display Three Address Code (3AC)
    print("\n--- Three Address Code ---")
    for instr in three_ac:
        if instr[1] == 'minus':
            print(f"{instr[0]} = minus {instr[2]}")
        elif instr[2] == '=':
            print(f"{instr[0]} = {instr[1]}")
        else:
            print(f"{instr[0]} = {instr[1]} {instr[2]} {instr[3]}")

    # Display Quadruples
    print("\n--- Quadruples ---")
    for i, quad in enumerate(generate_quadruples()):
        print(f"{i}: ({quad[0]:^7}, {quad[1]:^5}, {quad[2]:^5}, {quad[3]:^5})")

    # Display Triples
    print("\n--- Triples ---")
    triples = generate_triples()
    for i, triple in enumerate(triples):
        print(f"{i}: ({triple[0]:^7}, {triple[1]:^5}, {triple[2]:^5})")

if __name__ == "__main__":
    main()
