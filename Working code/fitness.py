import pandas as pd
import numpy as np
import math
from data import *

cutoff = 0.5


def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,24,3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

def fitness(spiderMonkey,sign):
    spiderMonkey = makeMonkey(spiderMonkey)
    
    T,F = 0,0
    
    df = pd.DataFrame()

    if sign == 0:
        df = df_neg_train
    else:
        df = df_pos_train

    for ind,row in df.iterrows():
        rule_satisfied = True
        for k,v in spiderMonkey.items():
            if v[0] >= cutoff:
                inside = True
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])
                if row[col[k]] < mn or row[col[k]] > mx:
                    rule_satisfied = False
                    break
        if rule_satisfied: 
            if df.Outcome is sign:
                T += 1
            else:
                F += 1

    return T,F

w1,w2,w3,w4,w5 = 0.5,0.5,0.5,0.2,0.3

def G_measure_ave(args):
    Tn,Fp = fitness(args,0)
    Tp,Fn = fitness(args,1)
    
    recall = Tp/(Tp + Fn) if Tp > 0 else 0
    precision = Tp/(Tp + Fp) if Tp > 0 else 0
    
    G_measure_pos = math.sqrt(recall * precision)
    
    inverse_recall = Tn/(Tn + Fp) if Tn > 0 else 0
    inverse_precision = Tn/(Tn + Fn) if Tn > 0 else 0
    
    G_measure_neg = math.sqrt(inverse_recall * inverse_precision)
    
    return w1 * G_measure_pos + w2 * G_measure_neg
    
    
def MIR():
    return 1
    
def Comprehensibility(args):
    num_attr = 0
    
    for i in range(0,24,3):
        num_attr += (1 if args[i] >= cutoff else 0)
    
    return (num_attr - 1)/8     
    
def fun(args,sign):
    atr = 0
    for i in range(0,24):
        if i % 3 == 0:
            if args[i] >= cutoff:
                atr += 1 

    if(atr == 0):
        return 0.0

    fit_score = w3 * G_measure_ave(args) + w4 * MIR() - w5 * Comprehensibility(args)

    # print(fit_score)

    return -1 * fit_score


# def fun(spiderMonkey,sign = 0):
    
#     spiderMonkey = makeMonkey(spiderMonkey)
    
#     hits = 0
    
#     for i in range(0,df.shape[0]):
#         ok = True
#         inside = False
#         for k,v in spiderMonkey.items():
#             if v[0] == 1:
#                 inside = True
#                 if df.iloc[i][col[k]] < v[1] or df.iloc[i][col[k]] > v[2]:
#                     ok = False
#                     break
#         if ok and df.iloc[i]["Outcome"] == sign and inside:
#             hits += 1

#     # print(hits)

#     return -1 * hits

# def fun(spiderMonkey,sign = 0):
#     hits = 0
#     df = pd.DataFrame()
#     if sign == 0:
#         df = df_neg_train
#     else:
#         df = df_pos_train
        
#     spiderMonkey = makeMonkey(spiderMonkey)
#     for ind,row in df.iterrows():
#         rule_satisfied = True
#         inside = False
#         for k,v in spiderMonkey.items():
#             if v[0] >= cutoff:
#                 inside = True
#                 if (row[col[k]] < v[1]) or (row[col[k]] > v[2]):
#                     rule_satisfied = False
#                     break
#         if inside and rule_satisfied:
#             hits += 1

#         return -1 * hits