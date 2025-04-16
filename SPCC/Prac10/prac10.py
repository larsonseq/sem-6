def simulate_code_generation(statements):
    # Register and address descriptor dictionaries to track the use of registers and addresses.
    register_descriptor = {'R0': '', 'R1': ''}
    address_descriptor = {}
    output_table = []

    for stmt in statements:
        stmt = stmt.strip()  # Remove extra spaces
        code_generated = []  # List to store the generated code for this statement
        lhs, expr = stmt.split('=')  # Split the statement into left-hand side (lhs) and right-hand side (expr)
        lhs = lhs.strip()  # Clean up lhs and rhs
        expr = expr.strip()

        if '+' in expr or '-' in expr:
            # Handling binary operations like a = b + c or a = b - c
            parts = expr.split()
            if len(parts) == 3:
                op1, operator, op2 = parts
                reg = 'R0' if register_descriptor['R0'] == '' else 'R1'  # Choose register R0 or R1
                code_generated.append(f"MOV {op1}, {reg}")  # Move operand 1 into the register
                if operator == '+':
                    code_generated.append(f"ADD {op2}, {reg}")  # Addition operation
                else:
                    code_generated.append(f"SUB {op2}, {reg}")  # Subtraction operation

                # Update the register and address descriptor
                register_descriptor[reg] = lhs
                address_descriptor[lhs] = f"{lhs} in {reg}"

            elif len(parts) == 5:
                # For cases like t + u + v, handle it manually (for now it's simplified)
                pass
        else:
            # Simple assignment like x = y
            src = expr
            reg = 'R0' if register_descriptor['R0'] == '' else 'R1'  # Choose register R0 or R1
            code_generated.append(f"MOV {src}, {reg}")  # Move src value into the register
            register_descriptor[reg] = lhs
            address_descriptor[lhs] = f"{lhs} in {reg}"

        # Final move to memory if required (e.g., d = result in register)
        if lhs in ['d', 'result']:
            code_generated.append(f"MOV {reg}, {lhs}")
            address_descriptor[lhs] = f"{lhs} in {reg} and memory"

        # Prepare the strings to display the current register and address descriptors
        reg_desc_str = ', '.join([f"{k} contains {v}" if v else f"{k} empty" for k, v in register_descriptor.items()])
        addr_desc_str = ', '.join([f"{k} in {v.split()[-1]}" for k, v in address_descriptor.items()])
        
        # Add the generated information for the current statement
        output_table.append((stmt, code_generated, reg_desc_str, addr_desc_str))

    return output_table

def display_table(table):
    print("\n--- Code Generation Output ---\n")
    print(f"{'Statements':<15} | {'Code Generated':<30} | {'Register Descriptor':<30} | {'Address Descriptor'}")
    print("-" * 100)
    for stmt, code, reg_desc, addr_desc in table:
        code_str = ('\n' + ' ' * 18).join(code)
        print(f"{stmt:<15} | {code_str:<30} | {reg_desc:<30} | {addr_desc}")


def main():
    print("Enter the 3-address code statements line by line. Type 'end' to finish:\n")
    statements = []
    while True:
        line = input()
        if line.lower() == 'end':
            break
        statements.append(line)

    output = simulate_code_generation(statements) 
    display_table(output)

if __name__ == "__main__":
    main()
