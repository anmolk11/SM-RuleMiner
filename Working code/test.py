from data import *
from fitness import *
import pandas as pd

def printVector(GlobalLeaderPosition):
    print("\n-----------------------------------------------------------\n")
    for i in range(0,24):
        if(i % 3 == 2):
            print(GlobalLeaderPosition[i])
        else:
            print(GlobalLeaderPosition[i],end="   ")
    print("\n-----------------------------------------------------------\n")

def score(rule,sign):
    # printVector(rule)
    df = pd.DataFrame()
    rule = makeMonkey(rule) 
    print(rule)
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
                if (row[col[k]] < v[1]) or (row[col[k]] > v[2]):
                    rule_sat = False
                    break
        if rule_sat:
            hits += 1
    print(f"{sign} Hits : {hits}\n\n")
    return hits/N

def accuracy(rule_set,sign):
    acc = 0
    N = len(rule_set)
    for rule in rule_set:
        acc += score(rule,sign)
    
    return (acc/N) * 100
