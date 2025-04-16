import re
from collections import Counter

class LexicalAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.keywords = {"int", "float", "double", "char", "string", "if", "else", "while", "for", "do",
                         "switch", "case", "break", "continue", "return", "void", "main", "class", "public",
                         "static", "final", "import", "new", "this", "true", "false", "null"}
        self.operators = {"=", "+", "-", "*", "/", "%", "++", "--", "&&", "||", "!", "<", ">", "<=", ">="}
        self.symbols = {"{", "}", "(", ")", "[", "]", ";", ",", "."}
        
        self.kSet = set()  
        self.iSet = set()  
        self.oSet = set()  
        self.sSet = set()  
        self.lSet = set()  

        self.words = []
        self.identifier_map = {}
        self.id_counter = 1

    def read_file(self):
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    self.words.extend(line.split())
        except FileNotFoundError:
            print("File not found.")
    
    def classify_tokens(self):
        for word in self.words:
            if word in self.keywords:
                self.kSet.add(word)
            elif word in self.operators:
                self.oSet.add(word)
            elif word in self.symbols:
                self.sSet.add(word)
            elif re.match(r'^\d+(\.\d+)?$', word):  
                self.lSet.add(word)
            else:
                self.iSet.add(word)

    def display_results(self):
        print("\n===== Tokens Found =====\n")

        print(f"Keywords: {self.kSet}")
        print(f"Keyword count = {len(self.kSet)}\n")

        print(f"Operators: {self.oSet}")
        print(f"Operator count = {len(self.oSet)}\n")

        print(f"Identifiers: {self.iSet}")
        print(f"Identifier count = {len(self.iSet)}\n")

        print(f"Symbols: {self.sSet}")
        print(f"Symbol count = {len(self.sSet)}\n")

        print(f"Literals: {self.lSet}")
        print(f"Literal count = {len(self.lSet)}\n")

        print("\n===== Symbol Table =====")
        print("---------------------------")
        print("Lexeme\t\tToken")
        print("---------------------------")

        for word in self.words:
            if word in self.keywords or word in self.operators or word in self.symbols:
                token = f"< {word} >"
            elif re.match(r'^\d+(\.\d+)?$', word):
                token = f"< {word} >"
            else:
                if word not in self.identifier_map:
                    self.identifier_map[word] = self.id_counter
                    self.id_counter += 1
                token = f"<id, {self.identifier_map[word]}>"
            
            print(f"{word}\t\t{token}" if len(word) < 8 else f"{word}\t{token}")

if __name__ == "__main__":
    analyzer = LexicalAnalyzer(r"src.txt")
    analyzer.read_file()
    analyzer.classify_tokens()
    analyzer.display_results()
