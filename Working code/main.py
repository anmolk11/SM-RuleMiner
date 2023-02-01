import numpy as np
import random
from fitness import fun
from read_rule import *
import time
import os

threshold = 30
Pop_size = 80
Max_iterations = 3
Total_Run = 1
max_part = 6

D_max = 200
S_max = 200
R_max = 200

D = 0
LocalLimit = 0
GlobalLimit = 0
limit = 0

Population = np.zeros((S_max,D_max))
fun_val = np.zeros(S_max)
fitness = np.zeros(S_max)
prob = np.zeros(S_max)
new_position = np.zeros(D_max)
ObjValSol = 0
FitnessSol = 0
neighbour = 0
param2change = 0
GlobalMin = 0
GlobalLeaderPosition = np.zeros(D_max)
LocalMin = np.zeros(S_max//2)
LocalLeaderPosition = np.zeros((S_max//2,D_max))
LocalLimitCount = np.zeros(S_max//2)
GlobalMins = np.zeros(R_max)
GlobalLimitCount = 0
gpoint = np.zeros((S_max,2))
r,r1,r2 = 0,0,0
Pr = 0
part = 0
acc_err = 0
lb = np.zeros(D_max)
ub = np.zeros(D_max)
fevel = 0

lo,hi,group,iter = 0,0,0,0
obj_val = 0
cr = 0


def initilize_params():
    global obj_val,acc_err,D,lb,ub
    LB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.078,0.078,0,21,21]
    UB = [1,17,17,1,199,199,1,122,122,1,99,99,1,846,846,1,67.1,67.1,1,2.42,2.42,1,81,81]
    D = 24
    obj_val = 0
    acc_err = 1.0e-5

    for d in range(D):
        lb[d] = LB[d]
        ub[d] = UB[d]

def CalculateFitness(fun):
    result = 0
    if fun >= 0:
        result = 1/(fun + 1)
    else:
        result = 1 + abs(fun)

    return result

def create_group():
    g = 0
    global lo,hi,gpoint,group
    while lo < Pop_size:
        hi = lo + Pop_size//part
        gpoint[g][0] = lo
        gpoint[g][1] = hi

        if (Pop_size - hi) < (Pop_size/part):
            gpoint[g][1] = Pop_size - 1
        
        g += 1
        lo = hi + 1
    group = g

def GlobalLearning():
    global GlobalMin,GlobalLimitCount
    G_trial = GlobalMin
    for i in range(Pop_size):
        if fun_val[i] < GlobalMin:
            GlobalMin = fun_val[i]
            for j in range(D):
                GlobalLeaderPosition[j] = Population[i][j]
    if abs(G_trial - GlobalMin) < acc_err:
        GlobalLimitCount += 1
    else:
        GlobalLimitCount = 0


def LocalLearning():
    OldMin = np.zeros(Pop_size//2)
    for k in range(group):
        OldMin[k] = LocalMin[k]

    for k in range(group):
        for i in range(int(gpoint[k][0]), int(gpoint[k][1]) + 1):
            if fun_val[i] < LocalMin[k]:
                LocalMin[k] = fun_val[i]
                for j in range(D):
                    LocalLeaderPosition[k][j] = Population[i][j]

    for k in range(group):
        if abs(OldMin[k] - LocalMin[k]) < acc_err:
            LocalLimitCount[k] += 1
        else:
            LocalLimitCount[k] = 0

def initialize():
    global GlobalMin
    global GlobalLeaderPosition
    global GlobalLimitCount
    for i in range(Pop_size):
        for j in range(D):
            Population[i][j] = random.uniform(0, 1) * (ub[j] - lb[j]) + lb[j]
            new_position[j] = Population[i][j]
        fun_val[i] = fun(new_position)
        fitness[i] = CalculateFitness(fun_val[i])

    GlobalMin = fun_val[0]
    GlobalLeaderPosition = Population[0]
    GlobalLimitCount = 0

    for k in range(group):
        LocalMin[k] = fun_val[int(gpoint[k][0])]
        LocalLimitCount[k] = 0
        LocalLeaderPosition[k] = Population[int(gpoint[k][0])]

def LocalLeaderPhase(k):
    global lo,hi,cr
    lo = int(gpoint[k][0])
    hi = int(gpoint[k][1])
    for i in range(lo, hi + 1):
        PopRand = i
        while PopRand == i:
            PopRand = int(random.uniform(0, 1) * (hi - lo) + lo)

        for j in range(D):
            if random.uniform(0, 1) >= cr:
                new_position[j] = Population[i][j] + (LocalLeaderPosition[k][j] - Population[i][j]) * random.uniform(0, 1) + (Population[PopRand][j] - Population[i][j]) * (random.uniform(0, 1) - 0.5) * 2
            else:
                new_position[j] = Population[i][j]
            if new_position[j] < lb[j]:
                new_position[j] = lb[j]
            if new_position[j] > ub[j]:
                new_position[j] = ub[j]

        ObjValSol = fun(new_position)
        FitnessSol = CalculateFitness(ObjValSol)
        if FitnessSol > fitness[i]:
            for j in range(D):
                Population[i][j] = new_position[j]
            fun_val[i] = ObjValSol
            fitness[i] = FitnessSol
    

def GlobalLeaderPhase(k):
    lo = int(gpoint[k][0])
    hi = int(gpoint[k][1])
    i = lo
    l = lo
    while l < hi:
        if random.uniform(0,1) < prob[i]:
            l += 1
            PopRand = int(random.uniform(0,1) * (hi - lo) + lo)
            while PopRand == i:
                PopRand = int(random.uniform(0,1) * (hi - lo) + lo)
            param2change = int(random.uniform(0,1) * D)
            
            for j in range(D):
                new_position[j] = Population[i][j]

            new_position[param2change] = Population[i][param2change] + (GlobalLeaderPosition[param2change] - Population[i][param2change]) * (random.random()) + (Population[PopRand][param2change] - Population[i][param2change]) * (random.random() - 0.5) * 2
            if new_position[param2change] < lb[param2change]:
                new_position[param2change] = lb[param2change]
            if new_position[param2change] > ub[param2change]:
                new_position[param2change] = ub[param2change]
            ObjValSol = fun(new_position)
            FitnessSol = CalculateFitness(ObjValSol)
            if FitnessSol > fitness[i]:
                for j in range(D):
                    Population[i][j] = new_position[j]
                fun_val[i] = ObjValSol
                fitness[i] = FitnessSol
        i += 1
        if i == hi:
            i = lo

def CalculateProbabilities():
    maxfit = fitness[0]
    for i in range(1,Pop_size):
        if fitness[i] > maxfit:
            maxfit = fitness[i]
    
    for i in range(Pop_size):
        prob[i] = 0.9 * (fitness[i] / maxfit) + 0.1


def LocalLeaderDecision():
    for k in range(group):
        if LocalLimitCount[k] > LocalLimit:
            for i in range(gpoint[k][0], gpoint[k][1]+1):
                for j in range(D):
                    if random.uniform(0, 1) >= cr:
                        Population[i][j] = random.uniform(lb[j], ub[j])
                    else:
                        Population[i][j] = Population[i][j] + (GlobalLeaderPosition[j] - Population[i][j]) * random.uniform(0, 1) + (Population[i][j] - LocalLeaderPosition[k][j]) * random.uniform(0, 1)
                    if Population[i][j] < lb[j]:
                        Population[i][j] = lb[j]
                    if Population[i][j] > ub[j]:
                        Population[i][j] = ub[j]

                fun_val[i] = fun(Population[i])
                fitness[i] = CalculateFitness(fun_val[i])

            LocalLimitCount[k] = 0


def GlobalLeaderDecision():
    global GlobalLimitCount
    if GlobalLimitCount > GlobalLimit:
        GlobalLimitCount = 0

        if part < max_part:
            part += 1
            create_group()
            LocalLearning()
        else:
            part = 1
            create_group()
            LocalLearning()


def printVector():
    print("\n-----------------------------------------------------------\n")
    for i in range(0,D):
        if(i % 3 == 2):
            print(GlobalLeaderPosition[i])
        else:
            print(GlobalLeaderPosition[i],end="   ")
    print("\n-----------------------------------------------------------\n")

if __name__ == "__main__":
    try:
        os.remove("rules.txt")
    except OSError:
        pass
    initilize_params()
    LocalLimit = 200
    GlobalLimit = 80
    run = 0
    while df[df["Outcome"] == 0].shape[0] > threshold:
        start_time = time.time()
        initialize()
        GlobalLearning()
        LocalLearning()
        fevel = 0
        part = 1
        create_group()
        cr = 0.3

        for iter in range(Max_iterations):
            for k in range(group):
                LocalLeaderPhase(k)

            CalculateProbabilities()

            for k in range(group):
                GlobalLeaderPhase(k)
            
            GlobalLearning()
            LocalLearning()
            LocalLeaderDecision()
            GlobalLeaderDecision()

            if abs(GlobalMin - obj_val) <= acc_err:
                break

            cr = cr + 0.4/Max_iterations
            GlobalMins[run] = GlobalMin
        
        # printVector()
        # print(GlobalLeaderPosition[:24],end="\n\n")
        print(f"Data set size : {df.shape[0]}\n")
        read_rule(GlobalLeaderPosition)
        score = delRows(GlobalLeaderPosition)
        print(f"Hits scored : {score}")
        print("\n---------------------------------\n")
        print("Execution time : ",end=" ")
        print(" %s seconds " % (time.time() - start_time))
        print("\n---------------------------------\n")
    
    print("End of Mining task")

        



