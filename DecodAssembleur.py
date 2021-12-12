# ============================================= #
#   Imports                                     #
# ============================================= #

from Datas import COMMANDS, CATEGORIES
import Tools

# ============================================= #
#   Fonctions                                   #
# ============================================= #

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
            lineBinProg = Tools.FillStr(lineBinProg, 26, True)
        elif nbParam == 1:
            lineBinProg += Tools.ConstantToBin(str(Labels[elems[1]])) + '0'
            lineBinProg = Tools.FillStr(lineBinProg, 26, True)
        elif nbParam == 2:
            if elems[0] == "LD":
                lineBinProg = Tools.FillStr(lineBinProg, 20, True)
                lineBinProg += Tools.RegisterToBinary(elems[2])
                lineBinProg += Tools.RegisterToBinary(elems[1])
            elif elems[0] == "STR":
                lineBinProg = Tools.FillStr(lineBinProg, 17, True)
                lineBinProg += Tools.RegisterToBinary(elems[2])
                lineBinProg += Tools.RegisterToBinary(elems[1])
                lineBinProg = Tools.FillStr(lineBinProg, 26, True)
            else:
                print("Error : unknown operation -->" + line + "<--")
                exit()
        elif nbParam == 3:
            lineBinProg += Tools.ConstantToBin(str(Labels[elems[3]])) + '0'
            lineBinProg += Tools.RegisterToBinary(elems[2])
            lineBinProg += Tools.RegisterToBinary(elems[1])
            lineBinProg = Tools.FillStr(lineBinProg, 26, True)
        else:
            print("Error : Unreadable number of params -->" + nbParam + "<--")
            exit()
    
    else:
        # Sinon, autres cas :

        # Cas d'une constante :
        if elems[0][-1] == 'i':
            lineBinProg += Tools.ConstantToBin(elems[3])
            lineBinProg = Tools.FillStr(lineBinProg, 20, True)

        # Sinon 2eme registre source :
        else:
            lineBinProg = Tools.FillStr(lineBinProg, 17, True)
            lineBinProg += Tools.RegisterToBinary(elems[3])

        # Source
        lineBinProg += Tools.RegisterToBinary(elems[2])
        # Destination
        lineBinProg += Tools.RegisterToBinary(elems[1])

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
hex = Tools.BinProgToHexProg(bin)
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