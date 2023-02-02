from fitness import *
import os

num_rule = 0

def delRows(args,sign = 0):
    global num_rule
    file = open("rules.txt","a")
    file.write(f"Rule num : {num_rule}\n")
    file.write(f"Class : {sign}\n")
    num_rule += 1
    print("\n\n")
    args = makeMonkey(args)
    print("If ")
    for k,v in args.items():
        if v[0] >= cutoff:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            print(f"{mn} <= {col[k]} <= {mx} \n")
            file.write(f"{mn} <= {col[k]} <= {mx} \n")
    if(sign == 1):
        print("Then Class = Positive")
    else:
        print("Then Class = Negative")
    print("\n")

    drop_ind = []
    score = 0
    for ind,row in df.iterrows():
        rule_satisfied = True
        for k,v in args.items():
            if v[0] >= cutoff:
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])

                if row[col[k]] < mn or row[col[k]] > mx:
                    rule_satisfied = False
                    break
        if rule_satisfied and row["Outcome"] == sign:
            score += 1
            drop_ind.append(ind)

    df.drop(drop_ind,axis = 0,inplace = True)
    file.write(f"Hits scored : {score}\n")
    file.write("\n--------------\n")
    return score



