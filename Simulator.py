import sys
import os

def sext(imm):
    if imm[0] == 0:
        while len(imm)<32 :
            imm = '0' + imm
        return imm
    while len(imm) < 32:
        imm = '1' + imm
    return imm

def decimaltobinary(num):
    num=int(num)
    if num >= 0:
        a = num
        s = ""
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            #print("number out of Range")
            s='-1'
            return s
        s = filler*"0" + s
        return s
    else:
        z = abs(num)
        s = ""
        cnt = 1
        temp = z
        while temp != 0:
            cnt += 1
            temp = temp//2
        a = (2**cnt) - z
        while a != 0:
            b = a%2
            s = s + str(b)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            #print("Number out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s 

def signed_conversion(imm):
    if imm[0] == '1':
        flipped_bits = ''.join('1' if bit == '0' else '0' for bit in imm)
        return -(int(flipped_bits, 2) + 1)  
    else:
        return int(imm, 2)

def unsigned_conversion(imm):
    return int(imm, 2)

def beq(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 == rs2:
        pc += imm                              #assuming pc is int
    else:
        pc += 4                                #assuming pc is int
    return pc

def bne(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 != rs2:
        pc += imm                              #assuming pc is int
    else:
        pc += 4                                #assuming pc is int
    return imm

def bge(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 >= rs2:
        pc += imm                              #assuming pc is int
    else:
        pc += 4                                #assuming pc is int
    return pc

def blt(rs1, rs2, imm, pc):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    if rs1 < rs2:
        pc += imm                              #assuming pc is int
    else:
        pc += 4                                #assuming pc is int                                         
    return pc
def B(i, pc, reg_dic):
    imm = i[0] + i[24] + i[1:7] + i[20:24]
    imm = sext(imm)
    func3 = i[-15:-12]
    rs1 = i[-20:-15]
    rs2 = i[-25:-20]
    if func3 == "000":
        pc = beq(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "001":
        pc = bne(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "100":
        pc = blt(reg_dic[rs1], reg_dic[rs2], imm, pc)
    if func3 == "101":
        pc = bge(reg_dic[rs1], reg_dic[rs2], imm, pc)
    return pc                               

# Add: add rd, rs1, rs2 rd = sext(rs1) + sext(rs2) (Overflow are ignored)
def add(rd, rs1, rs2, pc, reg_dic):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs2)
    reg_dic[rd] = decimaltobinary(rs1 + rs2)   #check for rs1 + rs2 overflow
    return pc + 4                              #assuming pc is int

# Sub: sub rd, rs1, rs2 rd = signed(rs1) - signed(rs2) 
def sub(rd, rs1, rs2, pc, reg_dic):
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs2)
    reg_dic[rd] = decimaltobinary(rs1 - rs2)   #check for rs1 - rs2 overflow
    return pc + 4                              #assuming pc is int

# Slt: slt rd, rs1, rs2 rd = 1. If sext(rs1) < sext(rs2)
def slt(rd, rs1, rs2, pc, reg_dic):
    rs1 = sext(rs1)
    rs2 = sext(rs2)
    rs1 = signed_conversion(rs1)
    rs2 = signed_conversion(rs2)
    if rs1 < rs2:
        reg_dic[rd] = decimaltobinary(1)
    return pc + 4                              #assuming pc is int

# Sltu: sltu rd, rs1, rs2 rd = 1. If unsigned(rs1) < unsigned(rs2)
def sltu(rd, rs1, rs2, pc, reg_dic):
    if rs1 < rs2:
        reg_dic[rd] = decimaltobinary(1)
    return pc + 4                              #assuming pc is int

# XOR: xor rd, rs1, rs2 rd = rs1⊕rs2 (Bitwise Exor)
def xor(rd, rs1, rs2, pc, reg_dic):
    reg_dic[rd] = decimaltobinary(rs1 ^ rs2)
    return pc + 4                              #assuming pc is int

# sll rd, rs1, rs2 rd = rs1<<unsigned(rs2[4:0])
# Left shift rs1 by the value in lower 5 bits of rs2.
def sll(rd, rs1, rs2, pc, reg_dic):
    rs2 = rs2[-5:]
    reg_dic[rd] = decimaltobinary(rs1 << int(rs2, 2))
    return pc + 4                              #assuming pc is int

# srl rd, rs1, rs2 rd = rs1>>unsigned(rs2[4:0])
# Right shift rs1 by the value in lower 5 bits of rs2.
def srl(rd, rs1, rs2, pc, reg_dic):
    rs2 = rs2[-5:]                             #check indexing here
    reg_dic[rd] = decimaltobinary(rs1 >> int(rs2, 2))
    return pc + 4                              #assuming pc is int

# or rd, rs1, rs2 rd = rs1|rs2 (Bitwise logical or.)
def or_(rd, rs1, rs2, pc, reg_dic):
    reg_dic[rd] = decimaltobinary(rs1 | rs2)
    return pc + 4                              #assuming pc is int

# and rd, rs1, rs2 rd = rs1&rs2 (Bitwise logical and.)
def and_(rd, rs1, rs2, pc, reg_dic):
    reg_dic[rd] = decimaltobinary(rs1 & rs2)
    return pc + 4                              #assuming pc is int
# [31:25] [24:20] [19:15] [14:12] [11:7] [6:0]
# funct7 rs2 rs1 funct3 rd opcode R-type
def R(i, pc, reg_dic):
    rd = i[-7:]
    rs1 = i[-20:-15]
    rs2 = i[-25:-20]
    funct3 = i[-15:-12]
    funct7 = i[:7]  
    if (funct3 == "000") and (funct7 == "0000000"):
        pc = add(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "000") and (funct7 == "0100000"):
        pc = sub(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "010") and (funct7 == "0000000"):
        pc = slt(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "011") and (funct7 == "0000000"):
        pc = sltu(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "100") and (funct7 == "0000000"):
        pc = xor(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "001") and (funct7 == "0000000"):
        pc = sll(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "101") and (funct7 == "0000000"):
        pc = srl(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "110") and (funct7 == "0000000"):
        pc = or_(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "111") and (funct7 == "0000000"):
        pc = and_(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    return pc
def lw(rd, rs1, imm, pc, reg_dic, mem_dic):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)               
    imm = signed_conversion(imm)               #check for rs1 + imm overflow
    number = rs1 + imm
    hex = f"0x{number:08X}" 
    reg_dic[rd] = mem_dic[hex]             
    return pc + 4                              #assuming pc is int
def addi(rd, rs1, imm, pc, reg_dic):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    reg_dic[rd] = decimaltobinary(rs1 + imm)   #check for rs1 + imm overflow
    return pc + 4                              #assuming pc is int 

def jalr(rd, x6, imm, pc, reg_dic):
    reg_dic[rd] = decimaltobinary(pc + 4)      #pc + 4 is int but reg_dic[rd] stores binary value
    x6 = sext(x6)
    x6 = signed_conversion(x6)
    imm = signed_conversion(imm)
    pc += decimaltobinary(x6 + imm)            #check for rs1 + imm overflow
    pc = pc[:-1] + "0"                         #here pc is now in binary and binary str is being returned,
                                               #but otherwise i am returning pc with type <int>, handle that
    return pc 

def I(i, pc, reg_dic, mem_dic):
    imm = i[:12]
    imm = sext(imm)
    rd = i[-12:-7]
    rs1 = i[-20:-15] 
    func3 = i[-15:-12]
    opcode = i[-7:]
    if (func3 == "010") and (opcode == "0000011"):
        pc = lw(rd, reg_dic[rs1], imm, pc, reg_dic, mem_dic)
    if func3 == "000" and (opcode == "0010011"):
        pc = addi(rd, reg_dic[rs1], imm, pc, reg_dic)
    if func3 == "000" and (opcode == "1100111"):
        pc = jalr(rd, reg_dic[rs1], imm, pc, reg_dic)
    return pc

def S_sw(i, pc, reg_opc_to_mem_add, mem_dic):
    imm = i[:-25] + i[-12:-7]
    imm = sext(imm)
    imm = signed_conversion(imm)
    rs1 = i[-20:-15]
    rs1 = sext(rs1)                           #check for rs1 + imm overflow
    rs1 = signed_conversion(rs1)
    rs2 = i[-25:-20]
    number = rs1 + imm
    mem_dic[reg_opc_to_mem_add[rs2]] = decimaltobinary(number)
    return pc + 4                             #assuming pc is int

def lui(rd, imm, pc, reg_dic):
    imm = signed_conversion(imm)
    reg_dic[rd] = decimaltobinary(pc + imm)   #pc + imm is int but reg_dic[rd] stores binary value
    return pc + 4                             #assuming pc is int

def aiupc(rd, imm, pc, reg_dic):
    reg_dic[rd] = imm
    return pc + 4                             #assuming pc is int

def U(i, pc, reg_dic):
    imm = i[:-12]
    imm = "000000000000" + imm
    rd = i[-12:-7]
    opcode = i[-7:]
    if opcode == "0110111":
        pc = lui(rd, imm, pc, reg_dic)
    if opcode == "0010111":
        pc = aiupc(rd, imm, pc, reg_dic)
    return pc

def J_jal(i, pc, reg_dic):
    imm = i[0] + i[13:21] + i[12] + i[1:11]                #check
    imm = sext(imm)
    imm = signed_conversion(imm)
    rd = i[-12:-7]
    reg_dic[rd] = decimaltobinary(pc + 4)     #pc + imm is int but reg_dic[rd] stores binary value
    pc += imm                                 #assuming pc is int
    return pc                                 #assuming pc is int                                               

def simulator(reg_dic, mem_dic, pc_dic, reg_opc_to_mem_add):
    pc = 0
    while pc <= 252:
        inst = pc_dic[pc]
        opc = inst[-7:]
        
        if opc == "0110011":
            pc = R(inst, pc, reg_dic)
        if opc == "0000011" or opc == "0010011" or opc == "1100111":
            pc = I(inst, pc, reg_dic, mem_dic)
        if opc == "0100011":
            pc = S_sw(inst, pc, reg_opc_to_mem_add, mem_dic)
        if opc == "1100011":
            pc = B(inst, pc, reg_dic)
        if opc == "0010111" or opc == "0110111":
            pc = U(inst, pc, reg_dic)
        if opc == "1101111":
            pc = J_jal(inst, pc, reg_dic)
        reg_dic["program"] = "0b" + decimaltobinary(pc)



reg_dic = { }
mem_dic = {}
reg_opc_to_mem_add = {}

# Data Memory
for i in range(32):  
    address = f'0x{int(0x00100000 + i * 4):08X}'  
    mem_dic[address] = '0' * 32
    
last_address = '0x0010007F'
mem_dic[last_address] = '0' * 32

# Read input from file
if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

# Get the input file path and output file path from command line arguments
input = sys.argv[1]
output = sys.argv[2]

# Check if the input file exists
if not os.path.exists(input):
    sys.exit("Input file does not exist")

# Open the input file
input_file = open(input, "r")
with open(input, "r") as input_file:
    # Check if the input file is empty
    if not input_file:
        sys.exit("Input file is empty")
    # Read the input file
    x = input_file.readlines()
    pc_dic = {}
    pc = 0
    output = []
    for line in x:
        pc_dic[pc] = line
        pc += 4

simulator(reg_dic, mem_dic, pc_dic, reg_opc_to_mem_add)
# Write output to the output file
with open(output, "r") as output_file:
    for line in output:
        output_file.write(line + "\n")
    for i in mem_dic.keys():
        output_file.write(i + ":" + mem_dic[i] + "\n")


sys.exit()   
