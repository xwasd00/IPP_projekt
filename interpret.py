import getopt, sys
from src.XmlParse import Parse
from src.Labels import Label

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
    while i < length:
        ## TODO: checking argumentu
        opcode = xml.instructions[i][1].lower()
        args = xml.instructions[i][2]
        pprint (args)
        ################### LABEL ###########################
        if opcode == 'label':
            ret = label.set_label(args[0][0], i)
            if (ret == -1):
                sys.exit(52)
        #################### JUMP ###########################
        elif opcode == 'jump':
            i = label.get_label(args[0][0])
            if(i == -1):
                sys.exit(52)
        ################### JUMPIFEQ ########################
        elif opcode == 'jumpifeq':
            #TODO: porovnání
            i = label.get_label(xml.instructions[i][2][0][0])
            if(i == -1):
                sys.exit(52)
        ################### JUMPIFNEQ ########################
        elif opcode == 'jumpifneq':
            #TODO: porovnání
            i = label.get_label(xml.instructions[i][2][0][0])
            if(i == -1):
                sys.exit(52)
        i += 1

