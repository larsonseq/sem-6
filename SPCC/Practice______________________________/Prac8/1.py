
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, }


def tokenize(expr):
    """ Tokenizers the string"""
    print(f"Tokenizing : {expr}...")

    idx = 0
    tokens = []
    while (idx < len(expr)):
        ch = expr[idx]
        if ch == " ":
            idx += 1
            continue
        
        if ch in precedence.keys() or ch in ['(', ')']:
            tokens.append(ch)
            idx += 1
            continue
        
        token = ""
        while (ch not in precedence.keys() and ch not in ['(', ')']) and ch != " ": 
            token += ch
            idx += 1
            if idx >= len(expr):
                break
            ch = expr[idx]
        tokens.append(token) 
    
    return tokens


def infix_to_postfix(tokens):
    postfix = []
    stack = []

    for ch in tokens: 
        if ch not in precedence and ch not in ['(', ')']:
            postfix.append(ch)
            continue
        if ch == '(':
            stack.append(ch)
            continue
        if ch == ')':
            while stack and stack[-1] not in '(':
                postfix.append(stack.pop()) 
            stack.pop()
            continue
        if stack:
            while stack and stack[-1] not in "()" and (precedence[ch] < precedence[stack[-1]]):
                postfix.append(stack.pop()) 
        stack.append(ch)
    while stack:
        postfix.append(stack.pop())

    return postfix


def postfix_to_3ac(postfix):
    temp_id = 1
    chars = []
    three_ac = []

    for ch in postfix:
        if ch not in precedence:
            chars.append(ch) 
        elif ch in precedence:
            op2 = chars.pop()
            op1 = chars.pop()
            temp = f"t{temp_id} = {op1} {ch} {op2}"
            chars.append(f"t{temp_id}")
            temp_id += 1
            three_ac.append(temp) 
    return three_ac, three_ac[-1][: 2]

def quadruple(three_ac):
    quads = []

    for i in three_ac:
        j = i.replace("=", "")
        j = j.replace("  ", " ")
        l = j.split(" ")
        print(l)
        if len(l) == 2:
            q = ('', l[1], '', l[0])
        else:
            q = (l[2], l[1], l[3], l[0])
        quads.append(q)
    return quads


def triples(three_ac):
    triple = []
    result = {}
    loc = 0

    for i in three_ac:
        j = i.replace("=", "").replace("  "," ")
        l = j.split(" ") 
        for i in range(len(l)):
            if l[i] in result:
                l[i] = result[l[i]]
        result[l[0]] = f"({loc})"
        loc += 1
        print(f"Bleh 2 \t\t{l}")
        if len(l) == 4:
            triple.append((l[2], l[1], l[3]))
        else:
            triple.append((" ", l[1], " "))
    for i, j in result.items():
        print(f"{i} {j}")
    return triple


def main():
    expr = input("Enter Expression: ")

    if "=" in expr:
        lhs, rhs = expr.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        tokens = tokenize(rhs)
    else:
        rhs = expr.strip()
        lhs = None
        tokens = tokenize(rhs)
    print(f"Tokens are is {tokens}")
    postfix = infix_to_postfix(tokens)
    print(f"Postfix is {postfix}")

    three_ac, last_temp_var = postfix_to_3ac(postfix)

    if lhs:
        three_ac.append(f"{lhs} = {last_temp_var}")

    print(f"\nThree AC Code is : ")
    for i in three_ac:
        print(i)

    quads = quadruple(three_ac)
    print(f"\nQuadruple is ")
    for i in quads:
        print(i)

    triple = triples(three_ac)
    print(f"\nTriples is ")
    for i in triple:
        print(i)


if __name__ == "__main__":
    main()