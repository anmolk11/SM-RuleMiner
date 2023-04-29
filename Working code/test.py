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
    T,F = 0,0
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
            if row["Outcome"] == sign:
                T += 1
            else:
                F += 1
    return T,F
