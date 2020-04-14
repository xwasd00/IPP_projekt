import sys
import re
## třída pro manipulaci s rámci proměnných a kontrolu
class Variables:
    GF = {} # typ dictionary
    sLF = [] # zásobník rámců
    TF = None # na začátku neinicializovány

    vStack = [] # zásobnik hodnot (PUSHS, POPS)



    # kontrola argumentů
    # arg - argument instrukce ve tvaru [hodnota, typ]
    # ref - možné typy argumentu (int, string, ...) v seznamu
    def check(self, arg, ref):
        if len(arg) < 2:
            sys.exit(32)
        arg_type = arg[1]
        for r in ref:
            # kontrola typu s referenčním
            if r == arg_type:

                # kontrola jednotlivých typů
                if arg_type == 'var':
                    return
                elif arg_type == 'label':
                    if re.match(r"^([a-zA-Z\_\-\$\%\&\*]+|[a-zA-Z\_\-\$\%\&\*][a-zA-Z0-9\_\-\$\%\&\*]+)$", arg[0]) is None:
                        sys.exit(32)
                    return
                elif arg_type == 'int':
                    try:
                        arg[0] = int(arg[0])
                    except ValueError:
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
                else:
                    return
                break
        sys.exit(53)

    def check_none(self, arg):
        if len(arg) > 1:
            sys.exit(32)
        if arg[0] is not None:
            sys.exit(32)
        return

    # vytvoření rámce
    def create_frame(self):
        if self.TF is None:
            self.TF = {}
        self.TF.clear()

    # uložení rámce z dočasného rámce na zásobník lokálních rámců
    def push_frame(self):
        if self.TF is None:
            sys.exit(55)
        self.sLF.append(self.TF)
        self.TF = None

    # vyjmutí vrchního rámce ze zásobníku rámců do dočasného rámce
    def pop_frame(self):
        if len(self.sLF) == 0:
            sys.exit(55)
        self.TF = self.sLF.pop()

    # rozdělení proměnné (např. GF@a na ['GF', 'a'])
    def split_var(self, var):
        var = var.split('@')
        if len(var) != 2 or re.match(r"^([a-zA-Z\_\-\$\%\&\*]+|[a-zA-Z\_\-\$\%\&\*][a-zA-Z0-9\_\-\$\%\&\*]+)$", var[1]) is None:
            sys.exit(32)
        return var

    # najití hodnoty proměnné v příslušném rámci
    def get_var(self, var):
        var = self.split_var(var)
        if var[0] == 'GF':
            frame = self.GF
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovaný rámec
                sys.exit(55)
            LF = self.sLF.pop()
            frame = LF
            self.sLF.append(LF)
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovaný rámec
                sys.exit(55)
            frame = self.TF
        else:
            sys.exit(32)
        if not var[1] in frame:
            sys.exit(54)
        if frame[var[1]] is None:
            sys.exit(56)
        return frame[var[1]]

    # najití typu proměnné v příslušném rámci
    def get_type(self, var):
        var = self.split_var(var)
        if var[0] == 'GF':
            frame = self.GF
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovaný rámec
                sys.exit(55)
            LF = self.sLF.pop()
            frame = LF
            self.sLF.append(LF)
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovaný rámec
                sys.exit(55)
            frame = self.TF
        else:
            sys.exit(32)
        if not var[1] in frame:
            sys.exit(54)
        if frame[var[1]] is None:
            return ''
        return frame[var[1]][1]

    # aktualizace proměnné 'var' hodnotou 'value' 
    # var = 'GF@a'
    # value = [hodnota, typ]
    def update_var(self, var, value):
        var = self.split_var(var)
        ####### GLOBAL FRAME #######
        if var[0] == 'GF':
            if not var[1] in self.GF:
                sys.exit(54)
            self.GF[var[1]] = value
        ######## LOCAL FRAME #######
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovany ramec
                sys.exit(55)
            LF = self.sLF.pop()
            if not var[1] in LF:
                sys.exit(54)
            LF[var[1]] = value
            self.sLF.append(LF)
        ##### TEMPORARY FRAME ######
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovany ramec
                sys.exit(55)
            if not var[1] in self.TF: 
                sys.exit(54)
            self.TF[var[1]] = value
        else:
            sys.exit(32)
        return

    # přidání nové neinicializované proměnné do příslušného rámce
    def create_var(self, var):
        var = self.split_var(var)
        ####### GLOBAL FRAME #######
        if var[0] == 'GF':
            if var[1] in self.GF: # redefinice proměnné
                sys.exit(52)
            self.GF[var[1]] = None
        ######## LOCAL FRAME #######
        elif var[0] == 'LF':
            if len(self.sLF) == 0: # neinicializovaný rámec
                sys.exit(55)
            LF = self.sLF.pop()
            if var[1] in LF: # redefinice proměnné
                sys.exit(52)
            LF[var[1]] = None
            self.sLF.append(LF)
        ##### TEMPORARY FRAME ######
        elif var[0] == 'TF':
            if self.TF is None: # neinicializovaný rámec
                sys.exit(55)
            if var[1] in self.TF: #redefinice proměnné
                sys.exit(52)
            self.TF[var[1]] = None
        else:
            sys.exit(32)

    # přidání hodnoty na zásobník rámců
    def push_var(self, value):
        self.vStack.append(value)

    # odebrání hodnoty ze zásobníku
    def pop_var(self):
        if len(self.vStack) == 0:
            sys.exit(56)
        else:
            ret = self.vStack.pop()
        return ret
