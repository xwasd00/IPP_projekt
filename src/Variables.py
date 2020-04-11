import sys
import re
class Variables:
    GF = {} # typ dictionary
    sLF = [] # zasobnik ramcu
    LF = None # nedefinovane ramce
    TF = None

    def check(self, arg, ref):
        if len(arg) < 2:
            sys.exit(32)
        arg_type = arg[1]
        for r in ref:
            if r == arg_type:
                if arg_type == 'label' or arg_type == 'var':
                    return
                elif arg_type == 'int':
                    if not isinstance(arg[0], int):
                        sys.exit(53)
                    return
                elif arg_type == 'string':
                    match = re.findall(r'\\(\d\d\d)', arg[0])
                    for i in match:
                        i = chr(int(i))
                        arg[0] = re.sub(r'\\\d\d\d', i, arg[0], 1)
                    return
                elif arg_type == 'bool':
                    if re.match(r"^(true|false)$", arg[0]) is None:
                        sys.exit(53)
                    return
                elif arg_type == 'nil':
                    if arg[0] != 'nil':
                        sys.exit(53)
                    return
                elif arg_type == 'type':
                    if re.match(r"^(int|bool|string)$", arg[0]) is None:
                        sys.exit(53)
                    return
                break
        sys.exit(53)

    def check_none(self, arg):
        if len(arg) > 1:
            sys.exit(32)
        if arg[0] is not None:
            sys.exit(32)
        return

    def create_frame(self):
        if self.TF is None:
            self.TF = {}
        self.TF.clear()

    def push_frame(self):
        if self.TF is None:
            sys.exit(55)
        self.sLF.append(self.TF)
        self.TF = None

    def pop_frame(self):
        if len(self.sLF) == 0:
            sys.exit(55)
        self.TF = self.sLF.pop()

    def split_var(self, var):
        var = var.split('@')
        if len(var) != 2 or re.match(r"^([a-zA-Z\_\-\$\%\&\*]*)$", var[1]) is None:
            sys.exit(32)
        return var

    def get_var(self, var):
        var = self.split_var(var)
        if var[0] == 'GF':
            frame = self.GF
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovany ramec
                sys.exit(55)
            LF = self.sLF.pop()
            frame = LF
            self.sLF.append(LF)
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovany ramec
                sys.exit(55)
            frame = self.TF
        else:
            sys.exit(32)
        if not var[1] in frame:
            sys.exit(54)
        if frame[var[1]] is None:
            sys.exit(56)
        return frame[var[1]]

    def update_var(self, var, value):
        var = self.split_var(var)
        ####### GLOBAL FRAME #######
        if var[0] == 'GF':
            if not var[1] in self.GF:
                sys.exit(54)
            if self.GF[var[1]] is None:
                self.GF[var[1]] = value
            elif self.GF[var[1]][1] == value[1]:
                self.GF[var[1]] = value
            else:
                sys.exit(53)
        ######## LOCAL FRAME #######
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovany ramec
                sys.exit(55)
            LF = self.sLF.pop()
            if not var[1] in LF:
                sys.exit(54)
            if LF[var[1]] is None:
                LF[var[1]] = value
            elif LF[var[1]][1] == value[1]:
                LF[var[1]] = value
            else:
                sys.exit(53)
            self.sLF.append(LF)
        ##### TEMPORARY FRAME ######
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovany ramec
                sys.exit(55)
            if not var[1] in self.TF: 
                sys.exit(54)
            if self.TF[var[1]] is None:
                self.TF[var[1]] = value
            elif self.TF[var[1]][1] == value[1]:
                self.TF[var[1]] = value
            else:
                sys.exit(53)
        else:
            sys.exit(32)
        return

    def create_var(self, var):
        var = self.split_var(var)
        ####### GLOBAL FRAME #######
        if var[0] == 'GF':
            if var[1] in self.GF: # redefinice promenne
                sys.exit(52)
            self.GF[var[1]] = None
        ######## LOCAL FRAME #######
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovany ramec
                sys.exit(55)
            LF = self.sLF.pop()
            if var[1] in LF: # redefinice promenne
                sys.exit(52)
            LF[var[1]] = None
            self.sLF.append(LF)
        ##### TEMPORARY FRAME ######
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovany ramec
                sys.exit(55)
            if var[1] in self.TF: #redefinice promenne
                sys.exit(52)
            self.TF[var[1]] = None
        else:
            sys.exit(32)
    
