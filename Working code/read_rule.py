import os
from data import *

cutoff = 0.5

def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,24,3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

num_rule = 1

def delRows(args,sign,displayRules = True):
    df = pd.DataFrame()
    if sign == 0:
        df = df_neg_train
    else:
        df = df_pos_train

    global num_rule
    file = open("Logs/rules.txt","a")
    file.write(f"Rule num : {num_rule}\n")
    file.write(f"Class : {sign}\n")
    num_rule += 1
    # print("\n\n")
    args = makeMonkey(args)
    # print("If ")
    for k,v in args.items():
        if v[0] >= cutoff:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            if displayRules:
                 print(f"{mn} <= {col[k]} <= {mx} \n")
            file.write(f"{mn} <= {col[k]} <= {mx} \n")
    if displayRules:
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
        if rule_satisfied:
            score += 1
            drop_ind.append(ind)

    df.drop(drop_ind,axis = 0,inplace = True)
    file.write(f"Hits scored : {score}\n")
    file.write("\n--------------\n")
    return score



