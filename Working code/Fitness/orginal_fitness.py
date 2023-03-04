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
            T += 1
        else:
            F += 1

    return T,F

w1,w2,w3,w4,w5 = 0.5,0.5,0.5,0.2,0.3

def G_measure_ave(args,sign):

    if sign == 1:
        Tp,Fn = fitness(args,1)
        Fp,Tn = fitness(args,0)
    else:
        Fn,Tp = fitness(args,1)
        Tn,Fp = fitness(args,0)
        
    recall = Tp/(Tp + Fn) if Tp > 0 else 0
    precision = Tp/(Tp + Fp) if Tp > 0 else 0
    
    G_measure_pos = math.sqrt(recall * precision)
    
    inverse_recall = Tn/(Tn + Fp) if Tn > 0 else 0
    inverse_precision = Tn/(Tn + Fn) if Tn > 0 else 0
    
    G_measure_neg = math.sqrt(inverse_recall * inverse_precision)
    
    return w1 * G_measure_pos + w2 * G_measure_neg
    
    
# Mean Interval Range    
def MIR(args):
    attMax = [13, 197, 122, 60, 744, 57.3, 2.329, 72]
    
    attMin = [0,    0,   0,   0,  0,  0.0,   0.078, 21]

    mir = 0
    
    colInd = 0
    
    D = 0

    for i in range(0,len(args),3):
        if args[i] >= cutoff:
            D += 1
            ubi = max(args[i + 1],args[i + 2])
            lbi = min(args[i + 1],args[i + 2])
            attr_max = attMax[colInd]
            attr_min = attMin[colInd]
            mir += (ubi - lbi)/(attr_max - attr_min)
        colInd += 1

    if D == 0:
        return 0
    return mir/D
    
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

    fit_score = w3 * G_measure_ave(args,sign) + w4 * MIR() - w5 * Comprehensibility(args)

    return -1 * fit_score