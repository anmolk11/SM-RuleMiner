import pandas as pd
import numpy as np

from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN

def handle_outliers(df):
    z_threshold = 3
    
    # numeric_columns = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
    numeric_columns = df.columns.tolist()[:-1]

    for column in numeric_columns:
        z_scores = (df[column] - df[column].mean()) / df[column].std()
        outliers = np.abs(z_scores) > z_threshold
        df.loc[outliers, column] = df[column].median()  

    return df

def over_sample(whole_data):
    col = whole_data.columns.tolist()

    X = whole_data[col[:-1]]
    y = whole_data["Outcome"]

    # ros = RandomOverSampler()
    # X_resampled, y_resampled = ros.fit_resample(X, y)

    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # adasyn = ADASYN()
    # X_resampled, y_resampled = adasyn.fit_resample(X, y)


    X_resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
    y_resampled_df = pd.DataFrame(y_resampled, columns=['Outcome'])

    whole_data = pd.concat([X_resampled_df, y_resampled_df], axis=1)

    return whole_data

if __name__ == "__main__":
    df = pd.read_csv("Data/diabetes.csv")
    print("\n--------------------------------\n")
    preprocessed_df = handle_outliers(df)
    
    