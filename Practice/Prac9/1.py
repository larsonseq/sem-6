

def is_constant(exrp):
    try:
        eval(expr)
        return True
    except:
        return False


def evaluate_expr(expr):
    try:
        return eval(expr)
    except:
        return expr

def main(lines):
    optimized = []
    constants = {}
    copies = dict()
    expression = {}

    for line in lines:
        if "=" not in line:
            optimized.append(line)
            continue
        
        lhs, rhs = line.split("=")
        lhs.strip()
        rhs.strip()

        # 1. Constant Folding
        if is_constant(rhs):
            val = evaluate_expr(expr)
            optimized.append(f"{lhs} = {val}")
            constants[lhs] = val
            continue
        
        # 2. Copy Propogation
        if rhs.isidentifier():
            while rhs in copies:
                rhs = copies[rhs]
            copies[rhs] = lhs
            continue
        
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
        if token:
            token = copies.get(token, token)
            tokens += token
        newrhs = tokens

        # 4. Common Subexpression Evaluation
        replaced_rhs = newrhs
        for expr, var in expression.items():
            if expr in replaced_rhs:
                replaced_rhs = replaced_rhs.replace(expr, var)
        
        expression[newrhs] = lhs
        optimized.append(f"{lhs} = {replaced_rhs}")
        copies[lhs] = lhs

    return optimized


if __name__ == "__main__":
    main()