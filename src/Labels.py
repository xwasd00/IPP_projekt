## třída pro prácí s návěštími
class Label:
    # tvar [návěští, pozice]
    labels = []
    label_stack = [] # zásobník pořadí (instrukce CALL a RETURN)

    # nastavení návěští + zjištění duplicit
    def set_label(self, arg, pos):
        for l in self.labels:
            if l[0] == arg:
                return(-1)
        self.labels.append((arg, pos))
        return(0)

    # získání návěští
    def get_label(self, name):
        for l in self.labels:
            if(l[0] == name):
                return(l[1])
        else:
            return(-1)

    # přidání návratové hodnoty na zásobník
    def pushL(self, i):
        self.label_stack.append(i)

    # odebrání hodnoty z vrcholu zásobníku (pokud lze)
    def popL(self):
        if len(self.label_stack) == 0:
            return -1
        return self.label_stack.pop()
