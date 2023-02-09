import pandas as pd
from sklearn.model_selection import train_test_split

pd.set_option('mode.chained_assignment', None)
df_all = pd.read_csv("diabetes.csv")

col = df_all.columns.tolist()

# df_pos_train = df_all[df_all["Outcome"] == 1]
# df_neg_train = df_all[df_all["Outcome"] == 0]


# X_pos = df_pos_train[col[:len(col) - 1]]
# X_neg = df_neg_train[col[:len(col) - 1]] 
# Y_pos = df_pos_train[col[-1]]
# Y_neg = df_neg_train[col[-1]]



# df_pos_train, df_pos_test, y_train, y_test = train_test_split(X_pos, Y_pos, test_size=0.3, random_state=0)
# df_neg_train, df_neg_test, y_train, y_test = train_test_split(X_neg, Y_neg, test_size=0.3, random_state=0)

df_neg_train = pd.read_csv("data/df_neg_train.csv")
df_pos_train = pd.read_csv("data/df_pos_train.csv")
df_neg_test = pd.read_csv("data/df_neg_test.csv")
df_pos_test = pd.read_csv("data/df_pos_test.csv")