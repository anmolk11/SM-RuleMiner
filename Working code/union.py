cutoff = 0.5
def union(rules):
    """ Takes the rule set and returns its union """
    final_rule = {
        0 : [1e9,-1],
        3 : [1e9,-1],
        6 : [1e9,-1],
        9 : [1e9,-1],
        12 : [1e9,-1],
        15 : [1e9,-1],
        18 : [1e9,-1],
        21 : [1e9,-1]
    }

    for rule in rules:
        for i in range(0,len(rule),3):
            if(rule[i] >= cutoff):
                lb = min(rule[i + 1],rule[i + 2])
                ub = max(rule[i + 1],rule[i + 2])
                final_rule[i][0] = min(final_rule[i][0],lb)
                final_rule[i][1] = max(final_rule[i][0],ub)

    final_rule_vector = [i for i in range(24)]

    for k,v in final_rule.items():
        if(v[0] != 1e9 and v[1] != -1):
            final_rule_vector[k] = 1
            final_rule_vector[k + 1] = v[0]
            final_rule_vector[k + 2] = v[1]
        else:
            final_rule_vector[k] = 0
            final_rule_vector[k + 1] = 0
            final_rule_vector[k + 2] = 0
    return final_rule_vector

if __name__ == "__main__":
    pass