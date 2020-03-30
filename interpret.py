import getopt, sys
from src.XmlParse import Parse


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
            print("Napodporovaná možnost")
    if xml_file == "" and stdin == "":
        sys.stderr.write("Chybí '--input=' i '--source, alespoň jeden argument musí být zadaný.\n")
        sys.exit(10)
    
    if xml_file == "":
        xml_file = sys.stdin
    xml = Parse()
    ret = xml.parse(xml_file)
    if ret != 0:
        sys.exit(ret)
    if stdin == "":
        stdin = sys.stdin
    print(xml.instructions)
