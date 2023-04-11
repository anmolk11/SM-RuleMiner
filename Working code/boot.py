import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.utils import resample



from main import smo
from union import union
from read_rule import read
from test import score

ratio = 0.2
bootstraps = 5


whole_data = pd.read_csv("Data/diabetes.csv")
col = whole_data.columns.tolist()

positive_data = whole_data[whole_data["Outcome"] == 1]
negative_data = whole_data[whole_data["Outcome"] == 0]

X_pos = positive_data[col[:len(col) - 1]]
X_neg = negative_data[col[:len(col) - 1]] 
Y_pos = positive_data[col[-1]]
Y_neg = negative_data[col[-1]]


df_pos_train, df_pos_test, y_pos_train, y_pos_test = train_test_split(X_pos, Y_pos, test_size= ratio, random_state=0)
df_neg_train, df_neg_test, y_neg_train, y_neg_test = train_test_split(X_neg, Y_neg, test_size= ratio, random_state=0) 


def pickBest(ruleset,df,sign):
    best = 0
    pick = []
    for rule in ruleset:
        scr = score(df,rule,sign)
        if scr > best:
            best = scr
            pick = rule

    return pick


def method1():
    """  
         make union of all the rules in the rule set and then again makes the union for each united the rules 
         of the bootstrappes. 
    """
    positive_rules = []
    
    for i in range(bootstraps):
        X_bs, y_bs = resample(df_pos_train, y_pos_train, replace=True)
        rules = smo(X_bs,1)
        positive_rules.append(rules)


    negative_rules = []

    for i in range(bootstraps):
        X_bs, y_bs = resample(df_neg_train, y_neg_train, replace=True)
        rules = smo(X_bs,0)
        negative_rules.append(rules)
    

    union_positive = []
    for rules in positive_rules:
        print(len(rules))
        union_positive.append(union(rules))
    

    union_negative = []
    for rules in negative_rules:
        print(len(rules))
        union_negative.append(union(rules))
    
    
    final_pos_rule = union(union_positive)
    final_neg_rule = union(union_negative)

    read(final_pos_rule,1,col,display=False)
    read(final_neg_rule,0,col,display=False)

    pos_rule_acc = score(df_pos_test,final_pos_rule,1)
    neg_rule_acc = score(df_neg_test,final_neg_rule,0)

    print(f"Postive : {pos_rule_acc * 100} %")
    print(f"Negative : {neg_rule_acc * 100} %")

def method2():
    positive_rules = []
    
    for i in range(bootstraps):
        X_bs, y_bs = resample(df_pos_train, y_pos_train, replace=True)
        rules = smo(X_bs,1)
        positive_rules.append(rules)


    negative_rules = []

    for i in range(bootstraps):
        X_bs, y_bs = resample(df_neg_train, y_neg_train, replace=True)
        rules = smo(X_bs,0)
        negative_rules.append(rules)
    

    union_positive = []
    for rules in positive_rules:
        union_positive.append(pickBest(rules,df_pos_test,1))
    

    union_negative = []
    for rules in negative_rules:
        union_negative.append(pickBest(rules,df_neg_test,0))
    
    
    final_pos_rule = union(union_positive)
    final_neg_rule = union(union_negative)

    read(final_pos_rule,1,col,display=False)
    read(final_neg_rule,0,col,display=False)

    pos_rule_acc = score(df_pos_test,final_pos_rule,1)
    neg_rule_acc = score(df_neg_test,final_neg_rule,0)

    print(f"Postive : {pos_rule_acc * 100} %")
    print(f"Negative : {neg_rule_acc * 100} %")


if __name__ == "__main__":
    start_time = time.time()

    # method1()
    method2()

    print("\n--------------------------------------------\n")
    print(f"\nTotal execution time : {(time.time() - start_time)/60} min")