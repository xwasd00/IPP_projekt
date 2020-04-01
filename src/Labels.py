
class Label:
    labels = []
    def set_label(self, arg, pos):
        for l in self.labels:
            if l[0] == arg:
                return(-1)
        self.labels.append((arg, pos))
        return(0)
    def get_label(self, name):
        for l in self.labels:
            if(l[0] == name):
                return(l[1])
        else:
            return(-1)
