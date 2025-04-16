def evaluate_expression(expr, sym_table, lc):
    # Handle expressions like "L1 + 3" or "A-1"
    parts = expr.replace(" ", "").replace("+", " + ").replace("-", " - ").split()
    result = 0
    op = "+"
    
    for part in parts:
        if part in ["+", "-"]:
            op = part
            continue
            
        if part.isdigit():
            val = int(part)
        else:
            # Look up symbol in symbol table
            val = 0
            for sym in sym_table:
                if sym[1] == part:
                    val = sym[2]
                    break
            
        if op == "+":
            result += val
        else:
            result -= val
            
    return result

def extract_literal_value(literal):
    # Handle literals like '=5' or '=15'
    return literal.strip("'=")

def search_symbol_table(sym_table, var):
    for line in sym_table:
        if line[1] == var:
            return line[2]  # Return address
    return None

def add_to_symbol_table(sym_table, symbol, address):
    # Check if symbol already exists
    for entry in sym_table:
        if entry[1] == symbol:
            return entry[0]
            
    # Add new symbol
    idx = len(sym_table) + 1
    sym_table.append([idx, symbol, address])
    return idx

def add_to_literal_table(literal_table, literal, address=None):
    literal_value = extract_literal_value(literal)
    # Check if literal already exists
    for entry in literal_table:
        if entry[1] == literal_value:
            return entry[0]
            
    # Add new literal
    idx = len(literal_table) + 1
    literal_table.append([idx, literal_value, address])
    return idx

def generate_assembly():
    assembly = []
    sym_table = []
    literal_table = []
    pool_table = []
    lc = 0
    
    while True:
        try:
            line = input().strip()
            if not line:
                continue
                
            parts = line.split()
            
            if ":" in line:
                label = parts[0].rstrip(":")
                add_to_symbol_table(sym_table, label, lc)
                parts = parts[1:]
                
            if not parts:
                continue
                
            # Handle END statement
            if parts[0] == "END":
                assembly.append([lc, ("AD", "02"), "-", "-"])
                # Process any unassigned literals
                for lit in literal_table:
                    if lit[2] is None:  # If literal doesn't have an address
                        lc += 1
                        lit[2] = lc  # Assign next available location
                        # Add literal to assembly code
                        assembly.append([lc, ("DL", "01"), "-", ("C", lit[1])])
                break
                
            # Handle START
            elif parts[0] == "START":
                lc = int(parts[1])
                assembly.append(["-", ("AD", "01"), "-", ("C", lc)])
                
            # Handle ORIGIN
            elif parts[0] == "ORIGIN":
                expr = " ".join(parts[1:])
                new_lc = evaluate_expression(expr, sym_table, lc)
                lc = new_lc
                assembly.append(["-", ("AD", "03"), "-", ("C", lc)])
                
            elif "EQU" in line:
                var = parts[0]
                expr = " ".join(parts[2:])
                address = evaluate_expression(expr, sym_table, lc)
                add_to_symbol_table(sym_table, var, address)
                assembly.append(["-", ("AD", "04"), "-", ("S", address)])

                
            elif parts[0] == "LTORG":
                assembly.append([lc, ("AD", "05"), "-", "-"])
                for lit in literal_table:
                    if lit[2] is None:  # Assign address if not already assigned
                        lit[2] = lc
                        lc += 1
                pool_table.append([len(pool_table) + 1, len(literal_table)])
 
            # Handle DC
            elif "DC" in line:
                var = parts[0]
                val = extract_literal_value(parts[2]) if "=" in parts[2] else parts[2].strip("'")
                add_to_symbol_table(sym_table, var, lc)
                assembly.append([lc, ("DL", "01"), "-", ("C", val)])
                lc += 1
                
            # Handle DS
            elif "DS" in line:
                var = parts[0]
                size = int(parts[2])
                add_to_symbol_table(sym_table, var, lc)
                assembly.append([lc, ("DL", "02"), "-", size])
                lc += size
                
            # Handle machine instructions
            else:
                instruction = parts[0]
                instruction_map = {
                    "STOP": ("00", 0),
                    "ADD": ("01", 2),
                    "SUB": ("02", 2),
                    "MUL": ("03", 2),
                    "MULT": ("03", 2),
                    "MOVER": ("04", 2),
                    "MOVEM": ("05", 2),
                    "COMP": ("06", 2),
                    "BC": ("07", 2),
                    "DIV": ("08", 2),
                    "READ": ("09", 1),
                    "PRINT": ("10", 1),
                    "STORE": ("11", 1)
                }
                
                if instruction in instruction_map:
                    instr_code, num_operands = instruction_map[instruction]
                    
                    if instruction == "STOP":
                        assembly.append([lc, ("IS", instr_code), "-", "-"])
                        lc += 1
                    elif num_operands == 1:
                        operand = parts[1]
                        if operand.startswith("'="):  # Literal
                            lit_idx = add_to_literal_table(literal_table, operand)
                            assembly.append([lc, ("IS", instr_code), "-", ("L", lit_idx)])
                        else:  # Symbol
                            sym_addr = search_symbol_table(sym_table, operand)
                            assembly.append([lc, ("IS", instr_code), "-", ("S", operand)])  # Store symbol name instead of address
                        lc += 1
                    else:
                        reg = parts[1].rstrip(",")
                        operand = parts[2]
                        reg_code = handle_register(reg)
                        
                        if operand.startswith("'="):  # Literal
                            lit_idx = add_to_literal_table(literal_table, operand)
                            assembly.append([lc, ("IS", instr_code), reg_code, ("L", lit_idx)])
                        else:  # Symbol
                            sym_addr = search_symbol_table(sym_table, operand)
                            assembly.append([lc, ("IS", instr_code), reg_code, ("S", operand)])  # Store symbol name instead of address
                        lc += 1
                        
        except Exception as e:
            print(f"Error processing line: {line}")
            print(f"Error details: {str(e)}")
            return None, None, None, None
            
    return assembly, sym_table, literal_table, pool_table

def handle_register(reg):
    register_map = {
        "AREG": "01",
        "BREG": "02",
        "CREG": "03",
        "DREG": "04"
    }
    return register_map.get(reg, "Error: Invalid Register")

def generate_machine_code(assembly, sym_table, literal_table, pool_table):
    machine_code = []
    for line in assembly:
        try:
            location = str(line[0]) if line[0] != "-" else "---"
            
            # Handle different instruction types
            if isinstance(line[1], tuple):
                op_type, op_code = line[1]
                
                if op_type == "IS":  # Machine Instructions
                    reg_code = line[2] if line[2] != "-" else "00"
                    
                    # Handle operand
                    operand = "000"
                    if len(line) > 3 and isinstance(line[3], tuple):
                        ref_type, ref_val = line[3]
                        if ref_type == "S":  # Symbol reference
                            # Find symbol address in symbol table
                            for sym in sym_table:
                                if sym[1] == ref_val:
                                    operand = str(sym[2])
                                    break
                                elif isinstance(ref_val, int):  # Direct address reference
                                    operand = str(ref_val)
                                    break
                        elif ref_type == "L":  # Literal reference
                            for lit in literal_table:
                                if lit[0] == ref_val:
                                    operand = str(lit[2])
                                    break
                        elif ref_type == "C":  # Constant
                            operand = str(ref_val)
                    
                    machine_code.append([location, op_code, reg_code, operand])
                
                elif op_type == "DL":  # Declarative statements
                    if op_code == "01":  # DC
                        machine_code.append([location, "02", "00", line[3][1] if isinstance(line[3], tuple) else line[3]])
                    elif op_code == "02":  # DS
                        machine_code.append([location, "02", "00", line[3]])
                
                elif op_type == "AD":  # Assembler Directives
                    if op_code == "01":  # START
                        machine_code.append([location, "00", "00", str(line[3][1])])
                    elif op_code == "02":  # END
                        # Add END instruction to machine code
                        machine_code.append([location, "00", "00", "000"])
                        
                        # Process any remaining literals after END
                        for lit in literal_table:
                            if lit[2] is not None:  # Only process literals that have addresses
                                machine_code.append([str(lit[2]), "02", "00", lit[1]])
                    # Skip other assembler directives in machine code
            
        except Exception as e:
            print(f"Warning: Error in machine code generation for line: {line}")
            print(f"Error details: {str(e)}")
            continue
    
    return machine_code

if __name__ == "__main__":
    print("Enter assembly code (type 'END' to finish):")
    assembly, sym_table, literal_table, pool_table = generate_assembly()
    
    if assembly is None:
        print("Assembly failed. Please check your input.")
        exit(1)

    print("\nPass 1 Code:")
    for line in assembly:
        print(line)
    
    print("\nSymbol Table:")
    print("Index  Symbol  Address")
    for line in sym_table:
        print(f"{line[0]:<6} {line[1]:<7} {line[2]}")
    
    print("\nLiteral Table:")
    print("Index  Literal  Address")
    for line in literal_table:
        print(f"{line[0]:<6} {line[1]:<8} {line[2]}")
    
    print("\nPool Table:")
    print("Index  Literal Count")
    for line in pool_table:
        print(f"{line[0]:<6} {line[1]}")

    print("\nMachine Code:")
    print("LOC    OP    REG   OPERAND")
    print("-" * 30)
    machine_code = generate_machine_code(assembly, sym_table, literal_table, pool_table)
    for line in machine_code:
        print(f"{line[0]:<6} {line[1]:<5} {line[2]:<5} {line[3]}")
 