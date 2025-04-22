import re

# Define keyword, operator, symbol sets
keywords = {"int", "float", "double", "char", "string", "if", "else", "while", "for", "do",
            "switch", "case", "break", "continue", "return", "void", "main", "class", "public",
            "static", "final", "import", "new", "this", "true", "false", "null"}

operators = {"=", "+", "-", "*", "/", "%", "++", "--", "&&", "||", "!", "<", ">", "<=", ">="}
symbols = {"{", "}", "(", ")", "[", "]", ";", ",", "."}

# Token sets
kSet = set()    # Keywords
iSet = set()    # 
oSet = set()    # Operands
sSet = set()    # Symbols
lSet = set()    # Literals

words = []
identifier_map = {}
id_counter = 1

# Read the source file
def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read().split()
    except FileNotFoundError:
        print("File not found.")
        return []

# Classify tokens into respective categories
def classify_tokens(words):
    global id_counter
    for word in words:
        if word in keywords:
            kSet.add(word)
        elif word in operators:
            oSet.add(word)
        elif word in symbols:
            sSet.add(word)
        elif re.match(r'^\d+(\.\d+)?$', word):  # Literal
            lSet.add(word)
        else:
            iSet.add(word)

# Display the results
def display_results(words):
    print("\n===== Tokens Found =====\n")

    print(f"Keywords: {kSet}")
    print(f"Keyword count = {len(kSet)}\n")

    print(f"Operators: {oSet}")
    print(f"Operator count = {len(oSet)}\n")

    print(f"Identifiers: {iSet}")
    print(f"Identifier count = {len(iSet)}\n")

    print(f"Symbols: {sSet}")
    print(f"Symbol count = {len(sSet)}\n")

    print(f"Literals: {lSet}")
    print(f"Literal count = {len(lSet)}\n")

    print("\n===== Symbol Table =====")
    print("---------------------------")
    print("Lexeme\t\tToken")
    print("---------------------------")

    for word in words:
        if word in keywords or word in operators or word in symbols:
            token = f"< {word} >"
        elif re.match(r'^\d+(\.\d+)?$', word):
            token = f"< {word} >"
        else: 
            if word not in identifier_map:
                identifier_map[word] = get_next_id()
            token = f"<id, {identifier_map[word]}>"
        print(f"{word}\t\t{token}" if len(word) < 8 else f"{word}\t{token}")

def get_next_id():
    global id_counter
    current = id_counter
    id_counter += 1
    return current

# Main execution
if __name__ == "__main__":
    words = read_file(r"C:\Users\Admin\Desktop\BE\sem 6\SPCC\Prac5\src.txt")
    classify_tokens(words)
    display_results(words)
