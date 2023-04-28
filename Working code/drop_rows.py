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

def delRows(args,df,sign):
    global num_rule    
    num_rule += 1
    args = makeMonkey(args)

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
    return score


