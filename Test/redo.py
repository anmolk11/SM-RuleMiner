import pandas as pd

df = pd.read_csv("diabetes.csv")

col = df.columns.tolist()

threshold = 50

def makeMonkey(args):
    monkey = {}
    
    i = 0
    
    for j in range(0,len(args),3):
        monkey[i] = args[j:j+3]
        i += 1
    
    return monkey

def read_rule(dict):
    dict = makeMonkey(dict)
    print("\nIf ")
    for k,v in dict.items():
        if v[0] == 1:
            mx = max(v[1],v[2])
            mn = min(v[1],v[2])
            print(f"{mn} <= {col[k]} <= {mx} and ")
    print("Then Class = Positive\n")


def delRows(args):
    drop_ind = []
    args = makeMonkey(args)
    score = 0
    for i in range(0,df.shape[0]):
        rule_satisfied = True
        for k,v in args.items():
            if v[0] == 1:
                mn = min(v[1],v[2])
                mx = max(v[1],v[2])

                if df.iloc[i][col[k]] < mn or df.iloc[i][col[k]] > mx:
                    rule_satisfied = False
                    break
        if rule_satisfied:
            score += 1
            drop_ind.append(i)

    df.drop(drop_ind,axis = 0,inplace = True)
    return score


with open('in.txt','r') as F:
    args = [float(x.rstrip()) for x in F]


if df.shape[0] > threshold:
    read_rule(args)
    print(F"Data set size : {df.shape[0]}\n\n")
    score = delRows(args)
    print(f"Hits scored : {score}\n\n")
    with open('flag.txt','w') as F:
        F.write('1')

else:
    print("Size of Data set is below the threshold\n\n")
    with open('flag.txt','w') as F:
        F.write('0')


#['0 Pregnancies', '1 Glucose', '2 BloodPressure', '3 SkinThickness', '4 Insulin', '5 BMI', '6 DiabetesPedigreeFunction', '7 Age', '8 Outcome']