import xml.etree.ElementTree as ET
# třída pro parsování xml
class Parse:
    instructions = [] # seznam jednotlivých instrukcí
    duplicate_order = [] # seznam pro zjištění duplicitního pořadí instrukcí
    def parse(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except:
            return(31)

        # kontrola hlavního těla programu
        if (root.tag != 'program'):
            return(32)
        if (root.get('language') != 'IPPcode20'):
            return(32)

        # jednotlivé instrukce
        for inst in root:
            if (inst.tag != 'instruction'):
                return(32)
            # order
            try:
                order = int(inst.get('order'))
            except:
                return(32)
            self.duplicate_order.append(order)

            #opcode
            opcode = inst.get('opcode')
            if (opcode is None):
                return(32)

            # zpracování argumentů
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
                    return(32)
            # přidání jednotlivých instrukcí do seznamu instrukcí
            i = []
            i.append(order)
            i.append(opcode)
            args = []
            args.append(arg1)
            args.append(arg2)
            args.append(arg3)
            i.append(args)
            self.instructions.append(i)

        
        #seřazení seznamu instrukcí + zjištění duplicitního pořadí
        def sortOrder(val):
            return val[0]
        self.instructions.sort(key = sortOrder)
        if len(self.instructions) > 0:
            if self.instructions[0][0] < 1:
                return(32)
            if len(self.duplicate_order) != len(set(self.duplicate_order)):
                return(32)
        del root
        del tree
        return (0)
