import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN

from main import smo
from union import *
from read_rule import read
from test import score
from log import log 
from preprocess import *
from confusion_mat import compute_confusion_matrix

ratio = 0.2
bootstraps = 5

whole_data = pd.read_csv("Data/diabetes.csv")
col = whole_data.columns.tolist()

whole_data = handle_outliers(whole_data)
whole_data = over_sample(whole_data)

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
        scr,pred = score(df,rule,sign)
        if scr > best:
            best = scr
            pick = rule

    return pick,best


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
        union_positive.append(union_OR(rules))
    

    union_negative = []
    for rules in negative_rules:
        print(len(rules))
        union_negative.append(union_OR(rules))
    
    
    final_pos_rule_or = union_OR(union_positive)
    final_neg_rule_or = union_OR(union_negative)
    read(final_pos_rule_or,1,display=False,text="OR M1")
    read(final_neg_rule_or,0,display=False,text="OR M1")

    final_pos_rule_and = union_AND(union_positive)
    final_neg_rule_and = union_AND(union_negative)
    read(final_pos_rule_and,1,display=False,text="AND M1")
    read(final_neg_rule_and,0,display=False,text="AND M1")

    final_pos_rule_ave = union_ave(union_positive)
    final_neg_rule_ave = union_ave(union_negative)
    read(final_pos_rule_ave,1,display=False,text="AVE M1")
    read(final_neg_rule_ave,0,display=False,text="AVE M1")

    pos_rule_acc_or = score(df_pos_test,final_pos_rule_or,1)
    neg_rule_acc_or = score(df_neg_test,final_neg_rule_or,0)

    pos_rule_acc_and = score(df_pos_test,final_pos_rule_and,1)
    neg_rule_acc_and = score(df_neg_test,final_neg_rule_and,0)

    pos_rule_acc_ave = score(df_pos_test,final_pos_rule_ave,1)
    neg_rule_acc_ave = score(df_neg_test,final_neg_rule_ave,0)


    print(f"Postive OR: {pos_rule_acc_or * 100} %")
    print(f"Negative OR: {neg_rule_acc_or * 100} %")
    print(f"Overall OR: {(pos_rule_acc_or + neg_rule_acc_or)/2 * 100} %")

    print("\n---------------------------------------\n")

    
    print(f"Postive and: {pos_rule_acc_and * 100} %")
    print(f"Negative and: {neg_rule_acc_and * 100} %")
    print(f"Overall and: {(pos_rule_acc_and + neg_rule_acc_and)/2 * 100} %")

    print("\n---------------------------------------\n")

    print(f"Postive ave: {pos_rule_acc_ave * 100} %")
    print(f"Negative ave: {neg_rule_acc_ave * 100} %")
    print(f"Overall ave: {(pos_rule_acc_ave + neg_rule_acc_ave)/2 * 100} %")

def method2(log_result = True):
    negative_rules = []

    for i in range(bootstraps):
        X_bs, y_bs = resample(df_neg_train, y_neg_train, replace=True)
        rules = smo(X_bs,0)
        negative_rules.append(rules)

    positive_rules = []
    
    for i in range(bootstraps):
        X_bs, y_bs = resample(df_pos_train, y_pos_train, replace=True)
        rules = smo(X_bs,1)
        positive_rules.append(rules)

    union_positive = []
    for rules in positive_rules:
        best,accuracy = pickBest(rules,df_pos_test,1)
        if log_result:
            log(best,accuracy,"pos_picked")
        union_positive.append(best)
    

    union_negative = []
    for rules in negative_rules:
        best,accuracy = pickBest(rules,df_neg_test,0)
        if log_result: 
            log(best,accuracy,"neg_picked")
        union_negative.append(best)

    final_pos_rule_or = union_OR(union_positive)
    final_neg_rule_or = union_OR(union_negative)
    read(final_pos_rule_or,1,display=False,text="OR M2")
    read(final_neg_rule_or,0,display=False,text="OR M2")

    # final_pos_rule_and = union_AND(union_positive)
    # final_neg_rule_and = union_AND(union_negative)
    # read(final_pos_rule_and,1,display=False,text="AND M2")
    # read(final_neg_rule_and,0,display=False,text="AND M2")

    # final_pos_rule_ave = union_ave(union_positive)
    # final_neg_rule_ave = union_ave(union_negative)
    # read(final_pos_rule_ave,1,display=False,text="AVE M2")
    # read(final_neg_rule_ave,0,display=False,text="AVE M2")

    pos_rule_acc_or,pred_pos = score(df_pos_test,final_pos_rule_or,1)
    neg_rule_acc_or,pred_neg = score(df_neg_test,final_neg_rule_or,0)

    pos_true = df_pos_test.shape[0] * [1] 
    neg_true = df_neg_test.shape[0] * [0] 

    cm, classes, accuracy_pos, precision_pos, recall_pos, f1_score_pos = compute_confusion_matrix(pos_true,pred_pos)
    cm, classes, accuracy_neg, precision_neg, recall_neg, f1_score_neg = compute_confusion_matrix(neg_true,pred_neg)
        

    # pos_rule_acc_and = score(df_pos_test,final_pos_rule_and,1)
    # neg_rule_acc_and = score(df_neg_test,final_neg_rule_and,0)

    # pos_rule_acc_ave = score(df_pos_test,final_pos_rule_ave,1)
    # neg_rule_acc_ave = score(df_neg_test,final_neg_rule_ave,0)

    if log_result:
        log(final_neg_rule_or,neg_rule_acc_or,"neg_final")
        log(final_pos_rule_or,pos_rule_acc_or,"pos_final")


    print(f"Postive OR: {pos_rule_acc_or * 100} %")
    print(f"Accuracy: {accuracy_pos}")
    print(f"Precision: {precision_pos}")
    print(f"Recall: {recall_pos}")
    print(f"F1-Score: {f1_score_pos}")
    print("\n---------------------------------------\n")

    print(f"Negative OR: {neg_rule_acc_or * 100} %")
    print(f"Accuracy: {accuracy_neg}")
    print(f"Precision: {precision_neg}")
    print(f"Recall: {recall_neg}")
    print(f"F1-Score: {f1_score_neg}")
    print("\n---------------------------------------\n")    

    print(f"Overall OR: {(pos_rule_acc_or + neg_rule_acc_or)/2 * 100} %")


    # print("\n---------------------------------------\n")

    
    
    # print(f"Postive and: {pos_rule_acc_and * 100} %")
    # print(f"Negative and: {neg_rule_acc_and * 100} %")
    # print(f"Overall and: {(pos_rule_acc_and + neg_rule_acc_and)/2 * 100} %")

    # print("\n---------------------------------------\n")

    # print(f"Postive Ave: {pos_rule_acc_ave * 100} %")
    # print(f"Negative Ave: {neg_rule_acc_ave * 100} %")
    # print(f"Overall Ave: {(pos_rule_acc_ave + neg_rule_acc_ave)/2 * 100} %")


if __name__ == "__main__":
    start_time = time.time()
    # method1()
    method2(log_result=False)

    print("\n--------------------------------------------\n")
    print(f"\nTotal execution time : { round((time.time() - start_time)/60,2) } min")