from fitness import *
import os

threshold = 30
def read_rule(dict):
    print("\n------------------------------------------------\n")
    print(f"\nScore : {-1 * fun(dict)}\n")
    dict = makeMonkey(dict)
    print("If ")
    for k,v in dict.items():
        if v[0] == 1:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            print(f"{mn} <= {col[k]} <= {mx} and ")
    print("Then Class = Positive")
    
    print("\n------------------------------------------------\n")

def delRows(args,sign):
    drop_ind = []
    args = makeMonkey(args)
    score = 0
    index = df.index.tolist()
    for i in index:
        rule_satisfied = True
        for k,v in args.items():
            if v[0] == 1:
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])

                if df.loc[i][col[k]] < mn or df.loc[i][col[k]] > mx:
                    rule_satisfied = False
                    break
        if rule_satisfied and df.loc[i]["Outcome"] == sign:
            score += 1
            drop_ind.append(i)

    df.drop(drop_ind,axis = 0,inplace = True)
    os.remove("diabetes.csv")
    df.to_csv("diabetes.csv")
    return score



