from combined import *
import random

Pop_size = 50
Max_iterations = 3
Total_Run = 1
max_part = 5

def CalculateFitness(fun):
    result = 0
    if fun >= 0:
        result = 1/(fun + 1)
    else:
        result = 1 + abs(fun)

    return result

def create_group():
    global lo,hi
    global group
    g = 0
    while lo < Pop_size:
        hi = lo + Pop_size//part
        gpoint[g][0] = lo
        gpoint[g][1] = hi

        if (Pop_size - hi) < (Pop_size/part):
            gpoint[g][1] = Pop_size - 1
        
        g += 1
        group = g
        lo = hi + 1

def GlobalLearning():
    global GlobalMin
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
        for i in range(gpoint[k][0], gpoint[k][1] + 1):
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
        LocalMin[k] = fun_val[gpoint[k][0]]
        LocalLimitCount[k] = 0
        LocalLeaderPosition[k] = Population[gpoint[k][0]]

def LocalLeaderPhase(k):
    lo = int(gpoint[k][0])
    hi = int(gpoint[k][1])
    for i in range(lo, hi + 1):
        PopRand = i
        while PopRand == i:
            PopRand = int(random.uniform(lo, hi))

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
        if random.random() < prob[i]:
            l += 1
            PopRand = lo + int(random.random() * (hi - lo))
            while PopRand == i:
                PopRand = lo + int(random.random() * (hi - lo))
            param2change = int(random.random() * D)
            new_position = [x for x in Population[i]]
            new_position[param2change] = Population[i][param2change] + (GlobalLeaderPosition[param2change] - Population[i][param2change]) * (random.random()) + (Population[PopRand][param2change] - Population[i][param2change]) * (random.random() - 0.5) * 2
            if new_position[param2change] < lb[param2change]:
                new_position[param2change] = lb[param2change]
            if new_position[param2change] > ub[param2change]:
                new_position[param2change] = ub[param2change]
            ObjValSol = fun(new_position)
            FitnessSol = CalculateFitness(ObjValSol)
            if FitnessSol > fitness[i]:
                Population[i] = new_position
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


def GlobalLeaderDecision():
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

if __name__ == "__main__":
    initilize_params(1)
    LocalLimit = D * Pop_size
    GlobalLimit = Pop_size

    for run in range(Total_Run):
        initialize()
        GlobalLearning()
        LocalLearning()
        fevel = 0
        part = 1
        create_group()
        cr = 0.1

        for iter in range(Max_iterations):
            for k in range(group):
                LocalLeaderPhase(k)
            
            for k in range(group):
                GlobalLeaderPhase(k)
            
            GlobalLearning()
            LocalLearning()
            LocalLeaderPosition()
            GlobalLeaderDecision()

            if abs(GlobalMin - obj_val) <= acc_err:
                break

            cr = cr + 0.4/Max_iterations
            GlobalMins[run] = GlobalMin

    print(GlobalLeaderPosition)            


