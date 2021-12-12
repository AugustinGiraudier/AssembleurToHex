# ============================================= #
#   Datas                                       #
# ============================================= #

CATEGORIES = { "UAL" : "00","MEM" : "01","CTRL" : "11" }
COMMANDS = {
    # ----- UAL ----- #
    "ADD" : {"categorie" : "UAL","code" : "0110"},
    "ADDi" : {"categorie" : "UAL","code" : "0111"},
    "SUB" : {"categorie" : "UAL","code" : "1000"},
    "SUBi" : {"categorie" : "UAL","code" : "1001"},
    "OR" : {"categorie" : "UAL","code" : "0010"},
    "ORi" : {"categorie" : "UAL","code" : "0011"},
    "XOR" : {"categorie" : "UAL","code" : "0100"},
    "XORi" : {"categorie" : "UAL","code" : "0101"},
    "AND" : {"categorie" : "UAL","code" : "0000"},
    "ANDi" : {"categorie" : "UAL","code" : "0001"},
    "SL" : {"categorie" : "UAL","code" : "1010"},
    "SR" : {"categorie" : "UAL","code" : "1100"
    },
    # ----- MEM ----- #
    "STR" : {"categorie" : "MEM","nbParam" : 2,"code" : "0000"},
    "LD" : {"categorie" : "MEM","nbParam" : 2,"code" : "0010"},
    # ----- CTRL ----- #
    "JMP" : {"categorie" : "CTRL","nbParam" : 1,"code" : "0000"},
    "JEQU" : {"categorie" : "CTRL","nbParam" : 3,"code" : "0010"},
    "JNEQ" : {"categorie" : "CTRL","nbParam" : 3,"code" : "0100"},
    "JSUP" : {"categorie" : "CTRL","nbParam" : 3,"code" : "0110"},
    "JINF" : {"categorie" : "CTRL","nbParam" : 3,"code" : "1000"},
    "CALL" : {"categorie" : "CTRL","nbParam" : 1,"code" : "1010"},
    "RET" : {"categorie" : "CTRL","nbParam" : 0,"code" : "1100"}
}

# ============================================= #
#   Fonctions                                   #
# ============================================= #

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

def GetLabels(lines : list[str]) -> dict :
    """
    Retourne le dictionnaire label -> ligne 
    qui correspond au programme assembleur passé en paramètre
    (ex : {'FONCTION' : 10})
    """
    Labels = {}
    NumLine = -1
    for line in lines:
        if line == "" or line[0] == "#":
            continue
        NumLine +=1
        elems = line.split(" ")
        if (elems[0])[-1] == ':':
            Labels[(elems[0])[:-1]] = NumLine
    return Labels

def ComputeLines(lines : list[str], reverseLine : bool = False) -> str :
    """
    Retourne le code binaire de la liste des lignes d'un programme assembleur
    Les lignes peuvent etre retournées (ex : '011' -> '110')
    """
    BinProg = ""
    NumLine = -1
    for line in lines:
        # Lignes vides ou commentées :
        if line == "" or line[0] == "#":
            continue
        NumLine +=1
        try:
            NewLine =  ComputeLine(line, NumLine) + "\n"
            if reverseLine:
                NewLine = NewLine[::-1]
            BinProg += NewLine
        except:
            print("Error : Cannot read -->" + line + "<--")
            exit()
    if reverseLine:
        BinProg = BinProg[1:]
    else:
        BinProg = BinProg[:-1]
    return BinProg

def ComputeLine(line : str, num : int) -> str :
    """
    Retourne le code binaire d'une ligne de programme assembleur
    """
    lineBinProg = ""
    elems = line.split(" ")

    # Cas d'un label (finissant par ':')
    if (elems[0])[-1] == ':':
        elems = elems[1:]
        if len(elems) == 0:
            return ""


    categorie = COMMANDS[elems[0]]["categorie"]

    # Cas des JMP/CALL/RET/LD/STR...
    if categorie == "CTRL" or categorie == "MEM":
        nbParam = COMMANDS[elems[0]]["nbParam"]
        if nbParam == 0:
            lineBinProg = FillStr(lineBinProg, 26, True)
        elif nbParam == 1:
            lineBinProg += ConstantToBin(str(Labels[elems[1]])) + '0'
            lineBinProg = FillStr(lineBinProg, 26, True)
        elif nbParam == 2:
            if elems[0] == "LD":
                lineBinProg = FillStr(lineBinProg, 20, True)
                lineBinProg += RegisterToBinary(elems[2])
                lineBinProg += RegisterToBinary(elems[1])
            elif elems[0] == "STR":
                lineBinProg = FillStr(lineBinProg, 17, True)
                lineBinProg += RegisterToBinary(elems[2])
                lineBinProg += RegisterToBinary(elems[1])
                lineBinProg = FillStr(lineBinProg, 26, True)
            else:
                print("Error : unknown operation -->" + line + "<--")
                exit()
        elif nbParam == 3:
            lineBinProg += ConstantToBin(str(Labels[elems[3]])) + '0'
            lineBinProg += RegisterToBinary(elems[2])
            lineBinProg += RegisterToBinary(elems[1])
            lineBinProg = FillStr(lineBinProg, 26, True)
        else:
            print("Error : Unreadable number of params -->" + nbParam + "<--")
            exit()
    
    else:
        # Sinon, autres cas :

        # Cas d'une constante :
        if elems[0][-1] == 'i':
            lineBinProg += ConstantToBin(elems[3])
            lineBinProg = FillStr(lineBinProg, 20, True)

        # Sinon 2eme registre source :
        else:
            lineBinProg = FillStr(lineBinProg, 17, True)
            lineBinProg += RegisterToBinary(elems[3])

        # Source
        lineBinProg += RegisterToBinary(elems[2])
        # Destination
        lineBinProg += RegisterToBinary(elems[1])

    # Opération (XOR/ADD...) + immédiat
    lineBinProg += COMMANDS[elems[0]]["code"]

    # Categorie (MEM/CTRL/UAL)
    lineBinProg += CATEGORIES[categorie]

    return lineBinProg

# ============================================= #
#   Main                                        #
# ============================================= #

# Récupération programme assembleur :
progFile = open("./AssembleurProgramme.obj", "r")
str_prog = progFile.read()
progFile.close()

# Séparation des lignes :
prog_lines = str_prog.split("\n")

# Récupération des labels :
Labels = GetLabels(prog_lines)

## Binaire :
bin = ComputeLines(prog_lines, False)
# Enregistrement
fileBin = open("./Results.bin", "w")
fileBin.write(bin)
fileBin.close()

## Hexa :
hex = BinProgToHexProg(bin)
# Enregistrement
fileHex = open("./Results.hex", "w")
fileHex.write(hex)
fileHex.close()
#exit()
# Affichage console :
print("--------------------------")
print(" BINARY :")
print("--------------------------")
print(bin)
print("--------------------------")
print(" HEXA :")
print("--------------------------")
print(hex)
print("--------------------------")
print(" LABELS :")
print("--------------------------")
print(Labels)      