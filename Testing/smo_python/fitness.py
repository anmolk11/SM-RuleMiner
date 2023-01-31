import pandas as pd
import numpy as np
import math

df = pd.read_csv("diabetes.csv")

col = df.columns.tolist()

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
    
    for i in range(0,df.shape[0]):
        rule_satisfied = True
        for k,v in spiderMonkey.items():
            if v[0] == 1:
                inside = True
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])
                if df.iloc[i][col[k]] < mn or df.iloc[i][col[k]] > mx:
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
    Tp,Fp = fitness(args,0)
    Tn,Fn = fitness(args,1)
    
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
    
    for i in range(0,len(args),3):
        num_attr += args[i]
    
    return (num_attr - 1)/8     
    
def fun(args):
    rule = np.zeros(24)
    atr = 0
    for i in range(0,24):
        if i % 3 == 0:
            if args[i] >= 0.3:
                atr += 1
                rule[i] = 1
            else:
                rule[i] = 0
        else:
            rule[i] = args[i] 

    
    if(atr == 0):
        return 0.0

    fit_score = w3 * G_measure_ave(rule) + w4 * MIR() - w5 * Comprehensibility(rule)

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
