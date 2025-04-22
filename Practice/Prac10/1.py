

def simulate_code_gen(statements):
    output_table = []
    register_descriptor = {'R0': "", 'R1': ""}
    address_descriptor = {}

    for stmt in statements:
        code = []
        lhs, expr = stmt.split("=")
        lhs = lhs.strip()
        expr = expr.strip()

        if '+' in expr or '-' in expr:
            parts = expr.split()
            if len(parts) == 3: 
                op1, operator, op2 = parts
                reg = 'R0' if register_descriptor['R0'] == "" else "R1"
                code.append(f"Mov {op1}, {reg}")
                if '+' in expr:
                    code.append(f"Add {op2}, {reg}")
                else:
                    code.append(f"Sub {op2}, {reg}")
                
                register_descriptor[reg] = lhs
                address_descriptor[lhs] = f"{lhs} in {reg}"
        else:
            src = expr
            reg = 'R0' if register_descriptor['R0'] == "" else "R1"
            code.append(f"MOV {reg}, {lhs}")
            address_descriptor[lhs] = f"{lhs} in {reg} and memory"

        reg_desc_str = ', '.join([f"{k} contains {v}" if v else f"{k} empty" for k, v in register_descriptor.items()])
        addr_desc_str = ", ".join([f"{k} in {v.split()[-1]}" for k, v in address_descriptor.items()])

        output_table.append((stmt, code, reg_desc_str, addr_desc_str))
    return output_table


def display_table(output):
    pass

def main():
    stmt = []
    print("Enter 'end' to stop: ")
    line = ""
    while line.lower() != 'end':
        line = input().strip()
        if line == 'end':
            break
        stmt.append(line)

    output = simulate_code_gen(stmt)
    for i in output:
        print(i)


if __name__ == "__main__":
    main()