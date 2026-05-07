import re

REGS = {f"R{i}": i for i in range(8)}

OPCODES = {
    "ADD": 0b0000,
    "SUB": 0b0000,
    "AND": 0b0000,
    "OR":  0b0000,
    "SLT": 0b0000,
    "ADDI": 0b0001,
    "LW":   0b0010,
    "SW":   0b0011,
    "BEQ":  0b0100,
    "BNE":  0b0101,
    "JAL":  0b0110,
}

FUNCTS = {
    "ADD": 0b000,
    "SUB": 0b001,
    "AND": 0b010,
    "OR":  0b011,
    "SLT": 0b100,
}

def clean_line(line):
    line = line.split("#")[0].strip()
    return line

def parse_num(x):
    x = x.strip()
    if x.startswith("0x"):
        return int(x, 16)
    return int(x)

def reg(x):
    return REGS[x.upper().replace(",", "")]

def imm6(x):
    n = parse_num(x.replace(",", ""))
    if n < 0:
        n = (1 << 6) + n
    return n & 0b111111

def offset9(x):
    n = parse_num(x.replace(",", ""))
    if n < 0:
        n = (1 << 9) + n
    return n & 0b111111111

def assemble_line(line, pc, labels):
    parts = re.split(r"[,\s]+", line.strip())
    inst = parts[0].upper()

    if inst in ["ADD", "SUB", "AND", "OR", "SLT"]:
        rd = reg(parts[1])
        rs1 = reg(parts[2])
        rs2 = reg(parts[3])
        funct = FUNCTS[inst]
        code = (OPCODES[inst] << 12) | (rd << 9) | (rs1 << 6) | (rs2 << 3) | funct
        return code

    if inst in ["ADDI", "LW"]:
        rd = reg(parts[1])
        rs1 = reg(parts[2])
        imm = imm6(parts[3])
        code = (OPCODES[inst] << 12) | (rd << 9) | (rs1 << 6) | imm
        return code

    if inst == "SW":
        rs2 = reg(parts[1])  # dado
        rs1 = reg(parts[2])  # base
        off = imm6(parts[3])
        code = (OPCODES[inst] << 12) | (rs1 << 9) | (rs2 << 6) | off
        return code

    if inst in ["BEQ", "BNE"]:
        rs1 = reg(parts[1])
        rs2 = reg(parts[2])
        target = parts[3]

        if target in labels:
            off = labels[target] - (pc + 1)
        else:
            off = parse_num(target)

        off = imm6(str(off))
        code = (OPCODES[inst] << 12) | (rs1 << 9) | (rs2 << 6) | off
        return code

    if inst == "JAL":
        rd = reg(parts[1])
        target = parts[2]

        if target in labels:
            off = labels[target] - pc
        else:
            off = parse_num(target)

        off = offset9(str(off))
        code = (OPCODES[inst] << 12) | (rd << 9) | off
        return code

    raise ValueError(f"Instrução desconhecida: {line}")

def assemble(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    lines = []
    labels = {}
    pc = 0

    for raw in raw_lines:
        line = clean_line(raw)
        if not line:
            continue

        if line.endswith(":"):
            label = line[:-1]
            labels[label] = pc
        else:
            lines.append(line)
            pc += 1

    hex_codes = []

    for pc, line in enumerate(lines):
        code = assemble_line(line, pc, labels)
        hex_codes.append(f"{code:04X}")

    return hex_codes

if __name__ == "__main__":
    entrada = "programa.asm"
    saida = "programa.hex"

    hex_codes = assemble(entrada)

    with open(saida, "w", encoding="utf-8") as f:
        f.write("v3.0 hex words addressed\n")
        for h in hex_codes:
            f.write(h + "\n")

    print("HEX gerado:")
    for h in hex_codes:
        print(h)