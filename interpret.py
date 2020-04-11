import getopt, sys
from src.XmlParse import Parse
from src.Labels import Label
from src.Variables import Variables

from pprint import pprint



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
    ### TODO: udelat trochu jinak (u read asi jenom) #######
    if stdin == "":
        stdin = sys.stdin
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
        ##################### JUMP ###########################
        if opcode == 'jump':
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
            #TODO: porovnání + kontrola argumentu
            i = label.get_label(xml.instructions[i][2][0][0])
            if(i == -1):
                sys.exit(52)
        ################### JUMPIFNEQ ########################
        elif opcode == 'jumpifneq':
            #TODO: porovnání + kontrola argumentu
            i = label.get_label(xml.instructions[i][2][0][0])
            if(i == -1):
                sys.exit(52)
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
            if (args[1][1] == 'var'):
                value = var.get_var(args[1][0])
            else:
                value = args[1]
            var.update_var(args[0][0], value)

        i += 1
    print(var.GF)

