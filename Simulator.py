#considering pc as integer value for now
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
        if filler < 0:
            print("number out of Range")
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
        if filler < 0:
            print("Number out of Range")
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
    func3 = i[-15:-13]
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

def R(i, pc, reg_dic):
    #try to create this
    ''''''

def lw(rd, rs1, imm, pc, reg_dic, mem_dic):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)               
    imm = signed_conversion(imm)               #check for rs1 + imm overflow
    reg_dic[rd] = mem_dic[rs1+imm]             #if binary value not 32 bits, you need to sign extend
    return pc + 4                              #assuming pc is int
def addi(rd, rs1, imm, pc, reg_dic):
    rs1 = sext(rs1)
    rs1 = signed_conversion(rs1)
    imm = signed_conversion(imm)
    reg_dic[rd] = decimaltobinary(rs1 + imm)   #check for rs1 + imm overflow
    return pc + 4                              #assuming pc is int 

def jalr(rd, x6, imm, pc):
    reg_dic[rd] = pc + 4
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
    rd = i[-11:-6]
    rs1 = i[-19:-14] 
    func3 = i[-14:-11]
    opcode = i[-6:]
    if (func3 == "010") and (opcode == "0000011"):
        pc = lw(rd, reg_dic[rs1], imm, pc, reg_dic, mem_dic)
    if func3 == "000" and (opcode == "0010011"):
        pc = addi(rd, reg_dic[rs1], imm, pc, reg_dic)
    if func3 == "000" and (opcode == "1100111"):
        pc = jalr(rd, reg_dic[rs1], imm, pc)
    return pc

def S_sw(i, pc, reg_dic, mem_dic):
    imm = i[:-24] + i[-11:-6]
    imm = sext(imm)
    imm = signed_conversion(imm)
    rs1 = i[-19:14]
    rs1 = sext(rs1)                           #check for rs1 + imm overflow
    rs1 = signed_conversion(rs1)
    rs2 = i[-24:-19]
    reg_dic[rs2] = mem_dic[rs1 + imm]         #if binary value not 32 bits, you need to sign extend
    return pc + 4                             #assuming pc is int

def lui(rd, imm, pc, reg_dic):
    imm = signed_conversion(imm)
    reg_dic[rd] = pc + imm
    return pc + 4                             #assuming pc is int

def aiupc(rd, imm, pc, reg_dic):
    reg_dic[rd] = imm
    return pc + 4                             #assuming pc is int

def U(i, pc, reg_dic):
    imm = i[:-11]
    imm = "000000000000" + imm
    rd = i[-11:-6]
    opcode = i[-6:]
    if opcode == "0110111":
        pc = lui(rd, imm, pc, reg_dic)
    if opcode == "0010111":
        pc = aiupc(rd, imm, pc, reg_dic)
    return pc

def J_jal(i, pc, reg_dic):
    imm = i[0] + i[-20:-11] + i[-21] + i[-31:-21]                #check
    imm = sext(imm)
    imm = signed_conversion(imm)
    rd = i[-11:-6]
    reg_dic[rd] = pc + 4
    pc += imm                                 #assuming pc is int
    return pc                                 #assuming pc is int                                               


reg_dic = {}
mem_dic = {}
