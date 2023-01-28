from a import *

def read_rule(dict):
    print("If ")
    for k,v in dict.items():
        if v[0] == 1:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            print(f"{mn} <= {col[k]} <= {mx} and ")
    print("Then Class = Positive")

    print(f"Score :  {fitness(dict,0)}")

with open("final_rule.txt","r") as file:
    a = [float(x.rstrip()) for x in file]

a = makeMonkey(a)

print("\n ---------------------------------------------- \n")
read_rule(a)
print("\n ---------------------------------------------- \n")

