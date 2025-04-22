# Operator Precedence Grammer 

def read_grammar_and_table():  

    print(f"Enter Terminals (Space Seperated): ")
    terminals = list(input().strip().split())

    print(f"Enter Non Terminals: ") 
    nonterminals = list(input().strip().split())

    productions = []
    print(f"Enter Productions (Form A -> B + C)")
    print("Enter 'done' to stop")
    while True:
        rule = input().strip()
        if rule.lower() == 'done':
            break
        if "->" not in rule:
            print(f"-> Should Exist in Rule")
            continue
        
        lhs, rhs = rule.split('->') 
        productions.append((lhs.strip(), rhs.strip().split()))
    
    symbols = terminals + ['$']
    precedence_table = {}
    print("Enter Precedence for Precedence Table: ")
    print("Accepted input :- '<', '>', 'accept;")
    for a in symbols:
        for b in symbols:
            print(f"Enter Precedence for {a} (On Stack) and {b} (On Input)")
            precedence = input().strip()
            while precedence not in [">", "<", "accept"]:
                print("Enter a valid Precedence")
                precedence = input().strip()
            precedence_table[(a, b)] = precedence
    return terminals, nonterminals, productions, precedence_table


def display_precedence_table(terminals, precedence_table):
    symbols = terminals + ["$"]
    print(f"Precedence Table: ")
    print("\t" + "\t".join(symbols))
    for row in symbols:
        line = [row]
        for col in symbols:
            rel = precedence_table.get((row, col), "Null")
            line.append(rel)
        print('\t'.join(line))

    
def get_precedence(a, b, precedence_table):
    return precedence_table.get((a, b), "Null")


def reduce_stack(stack, productions):
    for i in range(len(stack)):
        sub = stack[i : ]
        for lhs, rhs in productions:
            if sub == rhs:
                print(f"Reducing: {' '.join(sub)} to {lhs}")
                del stack[i : ]
                stack.append(lhs)
                return True
    return False

    
def parse_input(input_tokens, terminals, productions, precedence_table):
    stack = ['$']
    input_tokens.append('$')
    print("Parsing...")
    print(f"{'Stack':<30} {'Input':<30} {'Operation':<30}")

    i = 0
    while True:
        top_terminal = next((s for s in reversed(stack) if s in terminals or s == '$'), "$")
        current_input = input_tokens[i]

        precedence = get_precedence(top_terminal, current_input, precedence_table)

        if precedence == "accept":
            print("INput accepted")
            break
        elif precedence == "<" or precedence == "=":
            print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} SHIFT")
            stack.append(current_input)
            i += 1
        elif precedence == ">":
            if not reduce_stack(stack, productions):
                print("Error: No Rule To Reduce \nExiting...")
                break
        else:
            print("Something went wrongQ! \nExiting...")
            break


def main():
    terminals, nonterminals, productions, precedence_table = read_grammar_and_table()

    display_precedence_table(terminals, precedence_table)

    print("Enter input string to parse: ")
    tokens = input().strip().split()

    parse_input(tokens, terminals, productions, precedence_table)


if __name__ == "__main__":
    main()