import pandas as pd

df = pd.read_csv("diabetes.csv")

col = df.columns.tolist()

def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,len(args),3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

# spiderMonkey : args vector of 24 dimensions, sign : outcome (0 for positive and 1 for negative)
def fitness(spiderMonkey,sign):
    
    spiderMonkey = makeMonkey(spiderMonkey)
    
    T,F = 0,0
    
    for i in range(0,df.shape[0]):
        rule_satisfied = True
        for k,v in spiderMonkey.items():
            if v[0] == 1:
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

import math
def G_measure_ave(args):
    Tp,Fp = fitness(args,0)
    Tn,Fn = fitness(args,1)
    
    recall = Tp/(Tp + Fn)
    precision = Tp/(Tp + Fp)
    
    G_measure_pos = math.sqrt(recall * precision)
    
    inverse_recall = Tn/(Tn + Fp)
    inverse_precision = Tn/(Tn + Fn)
    
    G_measure_neg = math.sqrt(inverse_recall * inverse_precision)
    
    return w1 * G_measure_pos + w2 * G_measure_neg
    
    
def MIR():
    return 1
    
def Comprehensibility(args):
    num_attr = 0
    
    for i in range(0,len(args),3):
        num_attr += args[i]
    
    return (num_attr - 1)/8
    
    
    
def novelFitness(args):
    return w3 * G_measure_ave(args) + w4 * MIR() - w5 * Comprehensibility(args)

with open("in.txt","r") as file:
    a = [float(x.rstrip()) for x in file]
    
fit_score = fitness(a,0)

with open("res.txt","w") as f:
    f.write(str(fit_score))