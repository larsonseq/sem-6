import os


def is_constant(expr):
    try:
        eval(expr)
        return True
    except:
        return False


def evaluate(expr):
    try:
        return eval(expr)
    except:
        return expr


def optimise_code(lines):

    optimised = []
    copies = {}
    expressions = {}
    constants = {}

    for stmt in lines: 
        lhs, rhs = stmt.split("=")
        lhs.strip()
        rhs.strip()

        # Constant Folding
        if is_constant(rhs):
            val = evaluate(rhs)
            constants[lhs] = val
            optimised.append(f"{lhs} = {val}")
            continue
        
        # Copy Propogation
        if rhs.isidentifier():
            while rhs in copies:
                rhs = copies[rhs]
            copies[lhs] = rhs
            continue
        
        # Constant subexpression evaluation
        tokens = ""
        token = ""
        for ch in rhs:
            if ch.isalnum() or ch == "_":
                token += ch
            else:
                if token:
                    token = copies.get(token, token)
                    tokens += token
                    token = ""
                tokens += ch
        if token:
            token = copies.get(token, token)
            tokens += token
        
        newrhs = tokens

        for expr, var in expressions.items():
            if expr in newrhs:
                newrhs = newrhs.replace(expr, var)
        
        expressions[newrhs] = lhs
        optimised.append(f"{lhs} = {newrhs}")
    
    return optimised


def main():
    print("Enter code to optimize: ")
    print("Enter 'end' to stop: ")
    lines = []
    while True:
        l = input().strip()
        if l.lower() == 'end':
            break
        lines.append(l)
    
    optimize = optimise_code(lines)

    for i in optimize:
        print(i)


if __name__ == "__main__":
    main()