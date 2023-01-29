import pandas as pd

df = pd.read_csv("diabetes.csv")

def delRows(args):
    drop_ind = []
    """for i in range(0,df.shape[0]):
        if (df.iloc[i]["Outcome"] == 1) & (df.iloc[i]["Age"] >= 33.0375) & (df.iloc[i]["Age"] <= 75.0304):
            drop_ind.append(i)"""

    

    df.drop(drop_ind,axis = 0,inplace = True)



with open('in.txt','r') as F:
    args = [float(x.rstrip()) for x in F]

