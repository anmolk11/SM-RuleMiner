from read_rule import read

cutoff = 0.5
def union_OR(rules):
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


def union_AND(rules):
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
    count = [0] * 24
    for rule in rules:
        for i in range(0,len(rule),3):
            if(rule[i] >= cutoff):
                count[i] += 1
                lb = min(rule[i + 1],rule[i + 2])
                ub = max(rule[i + 1],rule[i + 2])
                final_rule[i][0] = min(final_rule[i][0],lb)
                final_rule[i][1] = max(final_rule[i][0],ub)

    final_rule_vector = [i for i in range(24)]
    num_rules = len(rules)
    for k,v in final_rule.items():
        if(v[0] != 1e9 and v[1] != -1 and count[k] == num_rules):
            final_rule_vector[k] = 1
            final_rule_vector[k + 1] = v[0]
            final_rule_vector[k + 2] = v[1]
        else:
            final_rule_vector[k] = 0
            final_rule_vector[k + 1] = 0
            final_rule_vector[k + 2] = 0
    return final_rule_vector


def union_ave(rules):
    final_rule = {
        0 : [0,0,0],
        3 : [0,0,0],
        6 : [0,0,0],
        9 : [0,0,0],
        12 : [0,0,0],
        15 : [0,0,0],
        18 : [0,0,0],
        21 : [0,0,0]
    }

    for rule in rules:
        for i in range(0,len(rule),3):
            if(rule[i] >= cutoff):
                lb = min(rule[i + 1],rule[i + 2])
                ub = max(rule[i + 1],rule[i + 2])
                final_rule[i][0] += (final_rule[i][0] + lb) 
                final_rule[i][1] += (final_rule[i][0] + ub)
                final_rule[i][2] += 1

    final_rule_vector = [i for i in range(24)]

    for k,v in final_rule.items():
        if(v[0] != 0 and v[1] != 0):
            final_rule_vector[k] = 1
            final_rule_vector[k + 1] = v[0]/v[2]
            final_rule_vector[k + 2] = v[1]/v[2]
        else:
            final_rule_vector[k] = 0
            final_rule_vector[k + 1] = 0
            final_rule_vector[k + 2] = 0
    return final_rule_vector    


def calucale_len(rule):
    length = 0

    for i in range(0,len(rule),3):
        length += rule[i]

    return length

if __name__ == "__main__":
    rules = [[0.6281725801060586, 15.363347695589997, 2.246975874346128, 0.34296177591882016, 96.31650094714809, 107.98570116134385, 0.0, 78.68625673123587, 1.4338766926068764, 0.0, 29.06208705697353, 38.55695455878572, 0.07450784123528545, 487.08710136122704, 140.7537998341421, 0.0, 3.102126143035397, 46.5230768189988, 0.435849684743444, 0.078, 0.9808076733681486, 0.28535309958095373, 66.63032114822427, 47.351631981377786], [0.3389816584528996, 9.637204854903608, 9.122276697235726, 0.26183383790331816, 64.198225947435, 61.99878554306996, 0.006439732154587069, 35.70901288232212, 35.49137240483337, 0.2748392167878103, 34.688289450174366, 1.6594076135025162, 0.367846467970641, 23.33761919462954, 447.7018030818012, 0.1905050902579991, 47.169864236009985, 56.48769965765572, 0.0, 1.7651381496106437, 1.4595769710267126, 0.8630496548844123, 80.7565955807419, 29.069025302645557], [0.09296391334743315, 10.334747470245247, 14.829818232262573, 0.3292590350437784, 140.86474285511963, 189.61673581883974, 0.19613285156143512, 15.191797489858041, 23.631583239210034, 0.3243467074740063, 38.87851398870816, 78.29886276222857, 0.05230148507463017, 276.2189600169081, 335.2731061134531, 0.015273207915289966, 47.63090263798866, 47.322248374312466, 0.44928514467611314, 1.530280767762981, 1.1222692601580955, 0.547400337464908, 65.4341831431225, 36.612185640957314], [0.06533852737789592, 7.362297707749833, 14.389690812431436, 0.23718568149096964, 111.06418196289113, 121.40273960457013, 0.20455139436735303, 96.27947226626566, 71.02825375326036, 0.7446808518870045, 15.133790565313038, 63.02969968164799, 0.04071722316283588, 409.84456024902823, 335.44797927620255, 0.19102852316858032, 31.75319358537647, 1.4694790517257594, 0.20050363313407316, 1.7733798243936552, 0.5020920001652841, 0.3501697342070207, 26.295872971867784, 39.671636402329504]]
    rule_AND = union_AND(rules)
    read(rule_AND,1,True)
    print("\n---------------------------------------------------------\n")
    rule_OR = union_OR(rules)
    read(rule_OR,1,True)
    print("\n---------------------------------------------------------\n")
    rule_ave = union_ave(rules)
    read(rule_ave,1,True)


