class Variables:

    def check(self, args, ref):
        count = 0
        while(count < len(ref)):
            if len(args[count]) < 2:
                return(-1)
            elif args[count][1] != ref[count]:
                return(-1)
            count += 1
        while count < 3:
            if args[count].count(None) < 1:
                return(-1)
            count += 1
        return(0)
