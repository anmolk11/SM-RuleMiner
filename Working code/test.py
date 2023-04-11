cutoff = 0.5

def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,24,3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

def score(df,rule,sign):
    col = df.columns
    rule = makeMonkey(rule) 
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
    return hits/N

def accuracy(df,rule_set,sign):
    acc = 0
    best = 0
    N = len(rule_set)
    for rule in rule_set:
        s = score(df,rule,sign)
        best = max(s,best)
        acc += s
    
    return (acc/N) * 100,best * 100
