import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

from main import smo

ratio = 0.2
bootstraps = 5

if __name__ == "__main__":
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
    
    positive_rules = []

    for i in range(bootstraps):
        X_bs, y_bs = resample(df_pos_train, y_pos_train, replace=True)
        rules = smo(X_bs,1)
        positive_rules.append(rules)
    

    for rule in positive_rules:
        print(len(rule))    



