from data import *
from fitness import *
import pandas as pd

def score(rule,sign):
    df = pd.DataFrame()
    rule = makeMonkey(rule) 

    if sign == 0:
        df = df_neg_test
    else:
        df = df_pos_test
    hits = 0
    N = df.shape[0]
    for ind,row in df.iterrows():
        rule_sat = True
        for k,v in rule.items():
            if v[0] >= cutoff:
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])
                if (row[col[k]] < mn) or (row[col[k]] > mx):
                    rule_sat = False
                    break
        if rule_sat:
            hits += 1
    # print(f"{sign} Hits : {hits}\n\n")
    return hits/N

def accuracy(rule_set,sign):
    acc = 0
    best = 0
    N = len(rule_set)
    for rule in rule_set:
        s = score(rule,sign)
        best = max(s,best)
        acc += s
    
    return (acc/N) * 100,best * 100
