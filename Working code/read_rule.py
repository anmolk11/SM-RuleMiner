cutoff = 0.5
def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,24,3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

def read(args,sign,col,display = False):
    file = open(f"Logs/rule_{sign}.txt","w")
    if(display):
        print(f"Class : {sign}\n")
    file.write(f"Class : {sign}\n")
    args = makeMonkey(args)
    for k,v in args.items():
        if v[0] >= cutoff:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            file.write(f"{mn} <= {col[k]} <= {mx} \n")
            if(display):
                print(f"{mn} <= {col[k]} <= {mx} \n")
