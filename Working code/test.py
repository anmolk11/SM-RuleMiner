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
        rule_sat =True
        for k,v in rule.items():
            if v[0] >= cutoff:
                if (row[col[k]] < v[1]) or (row[col[k]] > v[2]):
                    rule_sat = False
                    break
        if rule_sat:
            hits += 1

    return hits/N

def accuracy(rule_set,sign):
    acc = 0
    N = len(rule_set)
    for rule in rule_set:
        acc += score(rule,sign)
    
    return (acc/N) * 100
