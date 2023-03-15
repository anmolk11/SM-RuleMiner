from data import *
import pandas as pd

df = df_all

def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,24,3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

def support(args,cls = 0):
    args = makeMonkey(args)
    size = df.shape[0]
    for i,r in df.iterrows():
        for k,v in args.items():
            if(v[0] >= 0.5):
                mx = max(v[1],v[2])
                mn = min(v[1],v[2])
                if r[col[k]] >= mn and r[col[k]] <= mx and r["Outcome"] == cls:
                    count += 1
    
    return count/size