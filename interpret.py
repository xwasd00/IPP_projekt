import getopt, sys
from src.XmlParse import Parse
from src.Labels import Label
from src.Variables import Variables


if __name__ == "__main__":
    stdin = ""
    xml_file = ""

    try:
        opts, prog_argv = getopt.getopt(sys.argv[1:],'', ["help", "source=", "input="])
    except getopt.GetoptError as err:
        print(err)
        sys.stderr.write("Nápověda:`python3 interpret.py --help'\n")
        sys.exit(10)
    for name, value in opts:
        if name == "--help":
            # TODO:
            print("Nápověda")
            sys.exit(0)
        elif name == "--source":
            xml_file = value
        elif name == "--input":
            stdin = value
        else:
            pass
    if xml_file == "" and stdin == "":
        sys.stderr.write("Chybí '--input=' i '--source, alespoň jeden argument musí být zadaný.\n")
        sys.exit(10)
    if xml_file == "":
        xml_file = sys.stdin
    xml = Parse()
    ret = xml.parse(xml_file)
    if ret != 0:
        sys.exit(ret)
    if stdin != "":
        try:
            f = open(stdin)
        except IOError:
            sys.stderr.write("Soubor nedostupný.\n")
            sys.exit(11)
        sys.stdin = f
    #########################################################
    length = len(xml.instructions)
    i = 0

    label = Label()
    var = Variables()
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
    while i < length:
        opcode = xml.instructions[i][1].lower()
        args = xml.instructions[i][2]
        ################# LABEL - pass #######################
        if opcode == 'label':
            pass
        ##################### JUMP ###########################
        elif opcode == 'jump':
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
            label.pushL(i)
            i = label.get_label(args[0][0])
            if i == -1:
                sys.exit(52)
        #################### RETURN #########################
        elif opcode == 'return':
            ref1 = ['label']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            i = label.popL()
            if i == -1:
                sys.exit(56)
        ################### JUMPIFEQ ########################
        elif opcode == 'jumpifeq':
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
            if value1[1] != value2[1] and value1[1] != 'nil' and value[1] != 'nil':
                sys.exit(53)
            ## porovnavani
            if value1[1] == 'nil' and value1[1] == 'nil':
                i = label.get_label(xml.instructions[i][2][0][0])
            elif value1[1] == 'nil' or value2[1] == 'nil':
                pass
            elif value1[0] == value2[0]:
                i = label.get_label(xml.instructions[i][2][0][0])
            else:
                pass
            if(i == -1):
                sys.exit(52)
        ################### JUMPIFNEQ ########################
        elif opcode == 'jumpifneq':
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
            if value1[1] != value2[1] and value1[1] != 'nil' and value[1] != 'nil':
                sys.exit(53)
            ## porovnavani
            if value1[1] == 'nil' and value1[1] == 'nil':
                pass
            elif value1[1] == 'nil' or value2[1] == 'nil':
                i = label.get_label(xml.instructions[i][2][0][0])
            elif value1[0] == value2[0]:
                pass
            else:
                i = label.get_label(xml.instructions[i][2][0][0])

            if(i == -1):
                sys.exit(52)
        ##################### EXIT ###########################
        elif opcode == 'exit':
            ref1 = ['int']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            if args[0][0] < 50 and args[0][0] >= 0:
                sys.exit(args[0][0])
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
            if value[1] == 'nil':
                print()
            else:
                print(value[0], end='')
        #################### READ ############################
        elif opcode == 'read':
            ref1 = ['var']
            ref2 = ['type']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            try:
                a = input()
            except EOFError:
                value = ['nil', 'nil']
                var.update_var(args[0][0], value)
                pass
            if args[1][0] == 'int' and a.isdigit():
                value = [a, 'int']
            elif args[1][0] == 'string':
                value = [a, 'string']
            elif args[1][0] == 'bool':
                if a.lower() == 'true':
                    value = [a.lower , 'bool']
                else:
                    value = ['false', 'bool']
            else:
                value = ['nil', 'nil']
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
            value1[0] = value1[0] + value2[0]
            var.update_var(args[0][0], value1)
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
            value1[0] = value1[0] - value2[0]
            var.update_var(args[0][0], value1)
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
            value1[0] = value1[0] * value2[0]
            var.update_var(args[0][0], value1)
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
            value1[0] = value1[0] // value2[0]
            var.update_var(args[0][0], value1)
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
            if value1[1] != value2[1]:# musi byt stejneho typu
                sys.exit(53)
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
            if value1[1] != value2[1]:# musi byt stejneho typu
                sys.exit(53)
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
            if value1[1] != value2[1] and value1[1] != 'nil' and value[1] != 'nil':
                sys.exit(53)
            ## porovnavani
            if value1[1] == 'nil' and value1[1] == 'nil':
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
            value1[0] = value1[0] and value2[0]
            var.update_var(args[0][0], value1)
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
            value1[0] = value1[0] or value2[0]
            var.update_var(args[0][0], value1)
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
            if 0 <= value2[0] < len(value1[0]):
                sys.exit(58)
            char = value1[0][value2[0]]
            try:
                value1[0] = ord(char)
            except ValueError:
                sys.exit(58)
            value[1] = 'int'
            var.update_var(args[0][0], value)
        ################## TYPE ############################
        elif opcode == 'type':
            ref1 = ['var']
            ref2 = ['var', 'int', 'bool', 'string', 'nil']
            var.check(args[0], ref1)
            var.check(args[1], ref2)
            var.check_none(args[2])
            if args[1][1] == 'var':
                var_type = var.get_type(args[1][0])
            else:
                var_type = args[1][1]
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
            var.push_var(value)
        ################## POPS ##########################
        elif opcode == 'pops':
            ref1 = ['var']
            var.check(args[0], ref1)
            var.check_none(args[1])
            var.check_none(args[2])
            value = var.pop_var()
            var.update_var(args[0][0], value)

 

        

        i += 1
    f.close()

print(var.GF)
