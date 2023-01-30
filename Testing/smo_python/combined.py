import numpy as np

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
mean_fevel,total_feval,mean_error = 0,0,0
lo,hi,group,iter = 0,0,0,0
obj_val = 0
cr = 0

Foods = np.zeros((S_max,D_max))
f = np.zeros(S_max)
fitness_abc = np.zeros(S_max)
trial = np.zeros(S_max)
prob_abc = np.zeros(S_max)
solution = np.zeros(D_max)
GlobalParams = np.zeros(D_max)
GlobalMins_abc = np.zeros(R_max)

iter_i = 0

def fun(args):
    global iter_i
    print(type(args))
    iter_i += 1
    return args[0] * args[0] + 4 * args[0] - 2

def initilize_params(Pr):
    LB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.078,0.078,0,21,21]
    UB = [1,17,17,1,199,199,1,122,122,1,99,99,1,846,846,1,67.1,67.1,1,2.42,2.42,1,81,81]

    if Pr == 0:
        D = 24
        obj_val = 0
        acc_err = 1.0e-5

        for d in range(D):
            lb[d] = LB[d]
            ub[d] = UB[d]
    if Pr == 1:
        D = 1
        obj_val = 0
        acc_err = 1.0e-5
        lb[0] = -10
        ub[0] = 10 