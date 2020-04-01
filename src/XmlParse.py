import sys
import xml.etree.ElementTree as ET

class Parse:
    instructions = []
    def parse(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except:
            sys.stderr.write("Chybný XML formát.\n")
            return(31)

        if (root.tag != 'program'):
            sys.stderr.write("Očekáván element 'program'.\n")
            return(32)
        if (root.get('language') != 'IPPcode20'):
            sys.stderr.write("Očekáván správný atribut 'language' elementu 'program'.\n")
            return(32)

        # jednotlive instrukce
        for inst in root:
            if (inst.tag != 'instruction'):
                sys.stderr.write("Očekáván element 'instruction'.\n")
                return(32)

            # order
            try:
                order = int(inst.get('order'))
            except:
                sys.stderr.write("Očekáván správný atribut 'order' elementu 'instruction'.\n")
                return(32)

            #opcode
            opcode = inst.get('opcode')
            if (opcode is None):
                sys.stderr.write("Očekáván atribut 'opcode' elementu 'instruction'.\n")
                return(32)

            # zpracovani argumentu
            arg1 = []
            arg2 = []
            arg3 = []
            arg1.append( inst.findtext('arg1') )
            arg2.append( inst.findtext('arg2') )
            arg3.append( inst.findtext('arg3') )
            for arg in inst:
                if arg.tag == 'arg1':
                    if len(arg1) == 0:
                        return(32)
                    arg1.append(arg.get('type'))
                elif arg.tag == 'arg2':
                    if len(arg2) == 0:
                        return(32)
                    arg2.append(arg.get('type'))
                elif arg.tag == 'arg3':
                    if len(arg2) == 0:
                        return(32)
                    arg3.append(arg.get('type'))
                else:
                    sys.stderr.write("Očekáván element 'arg1', 'arg2' nebo 'arg3'.\n")
                    return(22)
            i = []
            i.append(order)
            i.append(opcode)
            args = []
            args.append(arg1)
            args.append(arg2)
            args.append(arg3)
            i.append(args)
            self.instructions.append(i)

        
        #serazeni seznamu instrukci
        def sortOrder(val):
            return val[0]
        self.instructions.sort(key = sortOrder)
        del root
        del tree
        return (0)
