CATEGORIES = {
    "UAL" : "00",
    "MEM" : "01",
    "CTRL" : "11"
}
COMMANDS = {
    
    # ----- UAL ----- #

    "ADD" : {
        "categorie" : "UAL",
        "code" : "0110"
    },
    "ADDI" : {
        "categorie" : "UAL",
        "code" : "0111"
    },
    "SUB" : {
        "categorie" : "UAL",
        "code" : "1000"
    },
    "SUBI" : {
        "categorie" : "UAL",
        "code" : "1001"
    },
    "OR" : {
        "categorie" : "UAL",
        "code" : "0010"
    },
    "ORI" : {
        "categorie" : "UAL",
        "code" : "0011"
    },
    "XOR" : {
        "categorie" : "UAL",
        "code" : "0100"
    },
    "XORI" : {
        "categorie" : "UAL",
        "code" : "0101"
    },
    "AND" : {
        "categorie" : "UAL",
        "code" : "0000"
    },
    "ANDI" : {
        "categorie" : "UAL",
        "code" : "0001"
    },
    "SL" : {
        "categorie" : "UAL",
        "code" : "1010"
    },
    "SR" : {
        "categorie" : "UAL",
        "code" : "1100"
    },

    # ----- MEM ----- #

    "STR" : {
        "categorie" : "MEM",
        "nbParam" : 2,
        "code" : "0000"
    },
    "LD" : {
        "categorie" : "MEM",
        "nbParam" : 2,
        "code" : "0010"
    },

    # ----- CTRL ----- #

    "JMP" : {
        "categorie" : "CTRL",
        "nbParam" : 1,
        "code" : "0000"
    },
    "JEQU" : {
        "categorie" : "CTRL",
        "nbParam" : 3,
        "code" : "0010"
    },
    "JNEQ" : {
        "categorie" : "CTRL",
        "nbParam" : 3,
        "code" : "0100"
    },
    "JSUP" : {
        "categorie" : "CTRL",
        "nbParam" : 3,
        "code" : "0110"
    },
    "JINF" : {
        "categorie" : "CTRL",
        "nbParam" : 3,
        "code" : "1000"
    },
    "CALL" : {
        "categorie" : "CTRL",
        "nbParam" : 1,
        "code" : "1010"
    },
    "RET" : {
        "categorie" : "CTRL",
        "nbParam" : 0,
        "code" : "1100"
    }
}