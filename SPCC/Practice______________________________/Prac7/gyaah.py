# Operator Precedence Parser - Enhanced Version

def read_grammar_and_table():
    print("===== Operator Precedence Parser =====")

    # Step 1: Input Non-terminals and Terminals
    print("\nEnter NON-TERMINALS (space-separated):")
    non_terminals = input().split()

    print("Enter TERMINALS (space-separated):")
    terminals = input().split()

    print("\nYou have entered:")
    print(f"Non-terminals: {non_terminals}")
    print(f"Terminals: {terminals}")

    # Step 2: Input grammar rules
    print("\nEnter Grammar Rules (one per line) in the format: A → B C or E → id")
    print("Type 'done' when finished.")
    productions = []
    while True:
        rule = input("Production: ").strip()
        if rule.lower() == 'done':
            break
        if "->" not in rule:
            print("Invalid format. Use -> symbol. Example: E -> E + E")
            continue
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = rhs.strip().split()
        productions.append((lhs, rhs))
    print(f"Production Rules: {productions}\n")

    # Step 3: Build precedence table
    symbols = terminals + ["$"]
    precedence_table = {}

    print("\nNow define precedence relations between terminal symbols.")
    print("For each pair (A on stack, B in input), enter relation (<, >, =, accept, NULL).")

    for a in symbols:
        for b in symbols:
            while True:
                rel = input(f"Relation between '{a}' (on stack) and '{b}' (input): ").strip()
                if rel in {"<", ">", "=", "accept", "NULL"}:
                    precedence_table[(a, b)] = rel
                    break
                else:
                    print("Invalid input. Please enter one of: <, >, =, accept, NULL")

    return non_terminals, terminals, productions, precedence_table



def display_table(terminals, table):
    terminals_with_dollar = terminals + ["$"]
    print("\n===== Precedence Table =====")
    print("\t" + "\t".join(terminals_with_dollar))
    for row in terminals_with_dollar:
        line = [row]
        for col in terminals_with_dollar:
            rel = table.get((row, col), "NULL")
            line.append(rel)
        print("\t".join(line))


def get_precedence(a, b, table):
    return table.get((a, b), "NULL")


def reduce_stack(stack, productions):
    for i in range(len(stack)):
        sub = stack[i:]
        for lhs, rhs in productions:
            if sub == rhs:
                print(f"Reducing: {' '.join(sub)} to {lhs}")
                del stack[i:]
                stack.append(lhs)
                return True
    return False


def parse_input(input_tokens, precedence_table, terminals, productions):
    stack = ["$"]
    input_tokens.append("$")
    print("\n===== Parsing Steps =====")
    print(f"{'Stack':<30} {'Input':<30} {'Action'}")

    i = 0
    while True:
        # Get top terminal in stack
        top_terminal = next((s for s in reversed(stack) if s in terminals or s == "$"), "$")
        current_input = input_tokens[i]

        precedence = get_precedence(top_terminal, current_input, precedence_table)

        if precedence == "accept":
            print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} ACCEPTED")
            break
        elif precedence == "<" or precedence == "=":
            print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} Shift")
            stack.append(current_input)
            i += 1
        elif precedence == ">":
            print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} Reduce")
            reduced = reduce_stack(stack, productions)
            if not reduced:
                print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} ERROR: No rule to reduce")
                break
        else:
            print(f"{' '.join(stack):<30} {' '.join(input_tokens[i:]):<30} ERROR: Invalid precedence")
            break


# MAIN FUNCTION
if __name__ == "__main__":
    non_terminals, terminals, productions, precedence_table = read_grammar_and_table()
    display_table(terminals, precedence_table)

    print("\nEnter input string to parse (space-separated tokens):")
    input_expr = input().split()

    parse_input(input_expr, precedence_table, terminals, productions)
