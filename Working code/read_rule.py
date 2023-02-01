from fitness import *
import os

def read_rule(dict):
    file = open("rules.txt","a")
    # print("\n------------------------------------------------\n")
    # print(f"\nScore : {-1 * fun(dict)}\n")
    print("\n\n")
    dict = makeMonkey(dict)
    print("If ")
    for k,v in dict.items():
        if v[0] >= 0.3:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            print(f"{mn} <= {col[k]} <= {mx} \n")
            file.write(f"{mn} <= {col[k]} <= {mx} \n")
    print("Then Class = Positive")
    print("\n")
    file.write("\n--------------\n")
    # print("\n------------------------------------------------\n")

def delRows(args,sign = 0):
    drop_ind = []
    args = makeMonkey(args)
    score = 0
    index = df.index.tolist()
    for i in index:
        rule_satisfied = True
        for k,v in args.items():
            if v[0] >= 0.3:
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])

                if df.loc[i][col[k]] < mn or df.loc[i][col[k]] > mx:
                    rule_satisfied = False
                    break
        if rule_satisfied and df.loc[i]["Outcome"] == sign:
            score += 1
            drop_ind.append(i)

    df.drop(drop_ind,axis = 0,inplace = True)
    return score



