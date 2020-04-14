#############################################################################
#                     2. část projektu do IPP                               #
#                   autor: Michal Sova (xsovam00)                           #
#############################################################################

import getopt, sys
from src.XmlParse import Parse
from src.Labels import Label
from src.Variables import Variables
def help():
    print("Interpret XML reprezentace kódu IPPcode20.")
    print("Tento skript pracuje s těmito paramety:")
    print("     --help           - Zobrazí nápovědu")
    print("     --source=file    - soubor s XML reprezentací kódu")
    print("     --input=file     - soubor se vstupem kódu")


if __name__ == "__main__":
    stdin = ""
    xml_file = ""

    # parsování argumentů
    try:
        opts, prog_argv = getopt.getopt(sys.argv[1:],'', ["help", "source=", "input="])
    except getopt.GetoptError as err:
        print(err)
        sys.stderr.write("Nápověda: 'python3.8 interpret.py --help'\n")
        sys.exit(10)
    for name, value in opts:
        if name == "--help":
            help()
            sys.exit(0)
        elif name == "--source":
            xml_file = value
        elif name == "--input":
            stdin = value
        else:
            pass

    ## kontrola --source= a --input=
    if xml_file == "" and stdin == "":
        sys.stderr.write("Chybí '--input=' i '--source, alespoň jeden argument musí být zadaný.\n")
        sys.exit(10)
    if xml_file == "":
        xml_file = sys.stdin
    if stdin != "":
            try:
                f = open(stdin)
            except IOError:
                sys.stderr.write("Soubor nedostupný.\n")
                sys.exit(11)
            sys.stdin = f


    # parsování xml
    xml = Parse()
    ret = xml.parse(xml_file)
    if ret != 0:
        sys.exit(ret)


    length = len(xml.instructions)
    i = 0
    label = Label()
    var = Variables()
    #################### definice návěští #########################

    while i < length:
        opcode = xml.instructions[i][1].lower()
        args = xml.instructions[i][2]
        ################### LABEL ###########################
        if opcode == 'label':
            ref = ['label']
            var.check(args[0], ref)
            var.check_none(args[1])
            var.check_none(args[2])
            if label.set_label(args[0][0], i) == -1:
                sys.exit(52)
        i += 1
    i = 0

    ################# interpretace programu ######################
    while i < length:
        opcode = xml.instructions[i][1].lower()
        args = xml.instructions[i][2]
        ################# LABEL - pass #######################
        if opcode == 'label':
            pass
        ##################### JUMP ###########################
        elif opcode == 'jump':
            # kontrola jednotlivých argumentů instrukce
            ref1 = ['label']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            i = label.get_label(args[0][0])
            if i == -1:
                sys.exit(52)
        ##################### CALL ##########################
        elif opcode == 'call':
            ref1 = ['label']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            label.pushL(i) # přidání pořadí instrukce na zásobník
            i = label.get_label(args[0][0]) # skok na návěští
            if i == -1:
                sys.exit(52)
        #################### RETURN #########################
        elif opcode == 'return':
            var.check_none(args[0])
            var.check_none(args[1])
            var.check_none(args[2])
            i = label.popL()
            if i == -1:
                sys.exit(56)
        ################### JUMPIFEQ ########################
        elif opcode == 'jumpifeq':
            ref1 = ['label']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            ref3 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
            else:
                value2 = args[2]

            # kontrola typů, stené nebo 'nil'
            if value1[1] != value2[1] and value1[1] != 'nil' and value2[1] != 'nil':
                sys.exit(53)

            # získání pozice(pořadí) návěští
            tmp = label.get_label(xml.instructions[i][2][0][0])

            ## porovnávání + skok
            if tmp == -1:
                sys.exit(52)
            if value1[1] == 'nil' and value2[1] == 'nil':
                i = tmp
            elif value1[1] == 'nil' or value2[1] == 'nil':
                pass
            elif value1[0] == value2[0]:
                i = tmp
        ################### JUMPIFNEQ ########################
        elif opcode == 'jumpifneq':
            ref1 = ['label']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            ref3 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
            else:
                value2 = args[2]

            # kontrola typů, stené nebo 'nil'
            if value1[1] != value2[1] and value1[1] != 'nil' and value2[1] != 'nil':
                sys.exit(53)

            # získání pozice(pořadí) návěští
            tmp = label.get_label(xml.instructions[i][2][0][0])

            ## porovnávání + skok
            if tmp == -1:
                sys.exit(52)
            ## porovnavani
            if value1[1] == 'nil' and value2[1] == 'nil':
                pass
            elif value1[1] == 'nil' or value2[1] == 'nil':
                i = tmp
            elif value1[0] == value2[0]:
                pass
            else:
                i = tmp
        ##################### EXIT ###########################
        elif opcode == 'exit':
            ref1 = ['var', 'int']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            if args[0][1] == 'var':
                value = var.get_var(args[0][0])
                if value[1] != 'int':
                    sys.exit(53)
            else:
                value = args[0]
            if value[0] < 50 and value[0] >= 0:
                sys.exit(value[0])
            else:
                sys.exit(57)
        ################## CREATEFRAME #######################
        elif opcode == 'createframe':
            var.check_none(args[0])
            var.check_none(args[1])
            var.check_none(args[2])
            var.create_frame()
        ################## PUSHFRAME #########################
        elif opcode == 'pushframe':
            var.check_none(args[0])
            var.check_none(args[1])
            var.check_none(args[2])
            var.push_frame()
        ################# POPFRAME ###########################
        elif opcode == 'popframe':
            var.check_none(args[0])
            var.check_none(args[1])
            var.check_none(args[2])
            var.pop_frame()
        ################## DEFVAR ############################
        elif opcode == 'defvar':
            ref1 = ['var']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            var.create_var(args[0][0])
        ################### MOVE #############################
        elif opcode == 'move':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            if args[1][1] == 'var':
                value = var.get_var(args[1][0])
            else:
                value = args[1]
            var.update_var(args[0][0], value)
        ################## WRITE #############################
        elif opcode == 'write':
            ref1 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            if args[0][1] == 'var':
                value = var.get_var(args[0][0])
            else:
                value = args[0]

            #vypsání hodnoty
            if value[1] == 'nil':
                # print()
                pass
            else:
                print(value[0], end='')
        #################### READ ############################
        elif opcode == 'read':
            ref1 = ['var']
            ref2 = ['type']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])

            #načtení hodnoty
            try:
                a = input()
            except EOFError:
                value = ['nil', 'nil']
                var.update_var(args[0][0], value)
                i += 1
                continue

            #kontrola hodnoty a typu
            if args[1][0] == 'int':
                try:
                    int(a)
                    value = [a, 'int']
                except ValueError:
                    value = ['nil', 'nil']
            elif args[1][0] == 'string':
                value = [a, 'string']
            elif args[1][0] == 'bool':
                if a.lower() == 'true':
                    value = ['true' , 'bool']
                else:
                    value = ['false', 'bool']
            else:
                value = ['nil', 'nil']

            # zapsání hodnoty do proměnné
            var.update_var(args[0][0], value)
        ################### ADD ##############################
        elif opcode == 'add':
            ref1 = ['var']
            ref2 = ['var', 'int']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'int':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]

            # sečtení hodnot a uložení do proměnné
            value = [value1[0] + value2[0], 'int']
            var.update_var(args[0][0], value)
        ################### SUB ##############################
        elif opcode == 'sub':
            ref1 = ['var']
            ref2 = ['var', 'int']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'int':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]

            # odečtení a uložení do proměnné
            value = [value1[0] - value2[0], 'int']
            var.update_var(args[0][0], value)
        ################### MUL ##############################
        elif opcode == 'mul':
            ref1 = ['var']
            ref2 = ['var', 'int']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'int':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]
            # vynásobení a uložení do proměnné
            value = [value1[0] * value2[0], 'int']
            var.update_var(args[0][0], value)
        ################### IDIV ##############################
        elif opcode == 'idiv':
            ref1 = ['var']
            ref2 = ['var', 'int']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'int':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]
            if value2[0] == 0:
                sys.exit(57)

            # vydělení a uložení do proměnné
            value = [value1[0] // value2[0], 'int']
            var.update_var(args[0][0], value)
        ################### LT ##############################
        elif opcode == 'lt':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string']
            ref3 = ['var', 'int', 'bool', 'string']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
            else:
                value2 = args[2]

            if value1[1] != value2[1]:# musí být stejného typu
                sys.exit(53)

            # porovnávání
            if value1[0] < value2[0]:
                val = ['true', 'bool']
            else:
                val = ['false', 'bool']
            var.update_var(args[0][0], val) 
        ################### GT ##############################
        elif opcode == 'gt':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string']
            ref3 = ['var', 'int', 'bool', 'string']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
            else:
                value2 = args[2]

            if value1[1] != value2[1]:# musí být stejného typu
                sys.exit(53)

            # porovnávání
            if value1[0] > value2[0]:
                val = ['true', 'bool']
            else:
                val = ['false', 'bool']
            var.update_var(args[0][0], val)
        ################### EQ ##############################
        elif opcode == 'eq':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            ref3 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
            else:
                value2 = args[2]

            # musí být stejný typ nebo 'nil'
            if value1[1] != value2[1] and value1[1] != 'nil' and value2[1] != 'nil':
                sys.exit(53)

            ## porovnávání
            if value1[1] == 'nil' and value2[1] == 'nil':
                val = ['true', 'bool']
            elif value1[1] == 'nil' or value2[1] == 'nil':
                val = ['false', 'bool']
            elif value1[0] == value2[0]:
                val = ['true', 'bool']
            else:
                val = ['false', 'bool']
            var.update_var(args[0][0], val)
        ################### AND ##############################
        elif opcode == 'and':
            ref1 = ['var']
            ref2 = ['var', 'bool']
            ref3 = ['var', 'bool']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'bool':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'bool':
                    sys.exit(53)
            else:
                value2 = args[2]

            # vyhodnocení
            if value1[0] == 'true' and value2[0] == 'true':
                value = ['true', 'bool']
            else:
                value = ['false', 'bool']
            var.update_var(args[0][0], value)
        ################### OR ##############################
        elif opcode == 'or':
            ref1 = ['var']
            ref2 = ['var', 'bool']
            ref3 = ['var', 'bool']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'bool':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'bool':
                    sys.exit(53)
            else:
                value2 = args[2]

            # vyhodnocení
            if value1[0] == 'true' or value2[0] == 'true':
                value = ['true', 'bool']
            else:
                value = ['false', 'bool']
            var.update_var(args[0][0], value)
        ################### NOT ##############################
        elif opcode == 'not':
            ref1 = ['var']
            ref2 = ['var', 'bool']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            if args[1][1] == 'var':
                value = var.get_var(args[1][0])
                if value[1] != 'bool':
                    sys.exit(53)
            else:
                value = args[1]

            if value[0] == 'false':
                value[0] = 'true'
            else:
                value[0] = 'false'
            var.update_var(args[0][0], value)
        ################# INT2CHAR ###########################
        elif opcode == 'int2char':
            ref1 = ['var']
            ref2 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            if args[1][1] == 'var':
                value = var.get_var(args[1][0])
                if value[1] != 'int':
                    sys.exit(53)
            else:
                value = args[1]

            # převedení
            try:
                value[0] = chr(value[0])
            except ValueError:
                sys.exit(58)
            value[1] = 'string'
            var.update_var(args[0][0], value)
        ################# STRI2INT ###########################
        elif opcode == 'stri2int':
            ref1 = ['var']
            ref2 = ['var', 'string']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'string':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]
            
            # převedení
            if not (0 <= value2[0] < len(value1[0])):
                sys.exit(58) # index je mimo rozsah
            char = value1[0][value2[0]]
            try:
                value1[0] = ord(char)
            except ValueError:
                sys.exit(58)
            value1[1] = 'int'
            var.update_var(args[0][0], value1)
        ################## TYPE ############################
        elif opcode == 'type':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            # zjištění typu
            if args[1][1] == 'var':
                var_type = var.get_type(args[1][0])
            else:
                var_type = args[1][1]

            # zapsání typu
            value = [var_type, 'string']
            var.update_var(args[0][0], value)
        ################## PUSHS ##########################
        elif opcode == 'pushs':
            ref1 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            if args[0][1] == 'var':
                value = var.get_var(args[0][0])
            else:
                value = args[0]

            # přidání na zásobník
            var.push_var(value)
        ################## POPS ##########################
        elif opcode == 'pops':
            ref1 = ['var']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            value = var.pop_var()

            # odebrání ze zásobníku
            var.update_var(args[0][0], value)
        ################# CONCAT ###########################
        elif opcode == 'concat':
            ref1 = ['var']
            ref2 = ['var', 'string']
            ref3 = ['var', 'string']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'string':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'string':
                    sys.exit(53)
            else:
                value2 = args[2]

            # konkatenace
            value = [value1[0] + value2[0], 'string']
            var.update_var(args[0][0], value)
        ################## STRLEN ###########################
        elif opcode == 'strlen':
            ref1 = ['var']
            ref2 = ['var', 'string']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            if args[1][1] == 'var':
                value = var.get_var(args[1][0])
                if value[1] != 'string':
                    sys.exit(53)
            else:
                value = args[1]

            # vypočítání délky
            val = [len(value[0]), 'int']
            var.update_var(args[0][0], val)
        ################## GETCHAR #########################
        elif opcode == 'getchar':
            ref1 = ['var']
            ref2 = ['var', 'string']
            ref3 = ['var', 'int']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'string':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'int':
                    sys.exit(53)
            else:
                value2 = args[2]

            # kontrola indexu
            if not (0 <= value2[0] < len(value1[0])):
                sys.exit(58)

            # získání znaku
            char = value1[0][value2[0]]
            value = [char, 'string']
            var.update_var(args[0][0], value)
        ################## SETCHAR #########################
        elif opcode == 'setchar':
            ref1 = ['var']
            ref2 = ['var', 'int']
            ref3 = ['var', 'string']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check(args[2], ref3)
            variable = var.get_var(args[0][0])
            if variable[1] != 'string':
                sys.exit(53)
            if args[1][1] == 'var':
                value1 = var.get_var(args[1][0])
                if value1[1] != 'int':
                    sys.exit(53)
            else:
                value1 = args[1]
            if args[2][1] == 'var':
                value2 = var.get_var(args[2][0])
                if value2[1] != 'string':
                    sys.exit(53)
            else:
                value2 = args[2]
            
            # kontrola indexu a délky 2. řetězce
            if not (0 <= value1[0] < len(variable[0])):
                sys.exit(58)
            if len(value2[0]) == 0:
                sys.exit(58)

            # přepsání znaku
            char = value2[0][0]
            variable[0] = variable[0][:value1[0]] + char + variable[0][value1[0]+1:]
            var.update_var(args[0][0], variable)
        ##################### DPRINT ########################
        elif opcode == 'dprint':
            ref1 = ['var', 'string', 'int', 'bool', 'nil']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            if args[0] == 'var':
                value = var.get_var(args[0][0])
            else:
                value = args[0]
            print(value[0], file=sys.stderr)
        #################### BREAK ########################
        elif opcode == 'break':
            var.check_none(args[0])
            var.check_none(args[1])
            var.check_none(args[2])
            print('pozice(order): ', xml.instructions[i][0], file=sys.stderr)
            print('vykonané instrukce: ', i, file=sys.stderr)
            print('globální rámec: ', var.GF, file=sys.stderr)
            print('lokální rámce: ', var.sLF, file=sys.stderr)
            print('dočasný rámec: ', var.TF, file=sys.stderr)
        ################## ostatni #################
        else:
            sys.exit(32)
        i += 1
    f.close()

