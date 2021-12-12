def BinProgToHexProg(BinProg : str) -> str :
    """
    Convertit un programme binaire en hexadécimal
    """
    lines = BinProg.split("\n")
    HexProg = ""
    for line in lines:
        if line == "":
            continue
        HexProg += FillStr(hex(int(line, 2))[2:], 8, False)
        HexProg += "\n"
    return HexProg[:-1]

def FillStr(string : str, finalSize : int, back : bool = True) -> str :
    """
    Permet de remplir une chaine de caractere par l'avant ou l'arriere
    jusqu'a une taille souhaitée
    """
    while len(string) < finalSize:
        if back:
            string += '0'
        else:
            string = '0' + string
    return string

def RegisterToBinary(reg : str) -> str :
    """
    Convertit un registre (ex : 'R6') en binaire (ex : '110')
    """
    if len(reg) != 2:
        print("Error : Cannot understand register -->" + reg + "<--")
        exit()
    num = int(reg[1])
    if num > 7:
        print("Error : Too high register number -->"+ reg+"<--")
        exit()
    numBinary = str(bin(num))[2:]
    numBinary = FillStr(numBinary, 3, False)
    return numBinary

def ConstantToBin(constant : str) -> str :
    """
    Convertit une constante de décimal à binaire sur 16 bits
    (ex : '12' -> '0000000000001100')
    """
    num = int(constant)
    if num > 65535:
        print("Error : Constant too high -->"+constant+"<--")
        exit()
    numBinary = str(bin(num))[2:]
    numBinary = FillStr(numBinary, 16, False)
    return numBinary