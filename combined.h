#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <conio.h>
#include <time.h>

/* Control Parameters of ASM algorithm*/

#define D_max 200 // Max number of dimensions of the search space
#define S_max 200 // Max swarm size
#define R_max 200 // Max number of runs

int D;
int LocalLimit;  // Spider Monkey
int GlobalLimit; // Spider Monkey
int limit;       // ABC
double Population[S_max][D_max];
double fun_val[S_max];
double fitness[S_max];
double prob[S_max];
double new_position[D_max];
double ObjValSol;
double FitnessSol;
int neighbour, param2change;
double GlobalMin;
double GlobalLeaderPosition[D_max];
double LocalMin[S_max / 2];
double LocalLeaderPosition[S_max / 2][D_max];
int LocalLimitCount[S_max / 2];
double GlobalMins[R_max];
int GlobalLimitCount;
int gpoint[S_max][2];
double r, r1, r2;
FILE *f_run, *f_run1;
int Pr;
double part;
double acc_err;
double lb[D_max], ub[D_max];
double feval;
double mean_feval, total_feval, mean_error;
int lo, hi, group, iter;
double obj_val;
double cr;
double Foods[S_max][D_max];   /*Foods is the population of food sources. Each row of Foods matrix is a vector holding D parameters to be optimized. The number of rows of Foods matrix equals to the FoodNumber*/
double f[S_max];              /*f is a vector holding objective function values associated with food sources */
double fitness_abc[S_max];    /*fitness is a vector holding fitness (quality) values associated with food sources*/
double trial[S_max];          /*trial is a vector holding trial numbers through which solutions can not be improved*/
double prob_abc[S_max];       /*prob is a vector holding probabilities of food sources (solutions) to be chosen*/
double solution[D_max];       /*New solution (neighbour) produced by v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij}) j is a randomly chosen parameter and k is a randomlu chosen solution different from i*/
double GlobalParams[D_max];   /*Parameters of the optimum solution*/
double GlobalMins_abc[R_max]; /*GlobalMins holds the GlobalMin of each run in multiple runs*/
// double pi;
// double E;

// double fun(double x[])
// {
    
//     feval++;
//     double f =  5 * x[0] - x[0] * x[0] + 2;
//     return -1 * f;
    
// } 

// void initilize_params(int Pr)
// {
//     int d;
//     system("color 70");
//     if (Pr == 0) // Parabola (Sphere)
//     {
//         D = 1;
//         obj_val = 0;
//         acc_err = 1.0e-5;
//         for (d = 0; d < D; d++)
//         {
//             lb[d] = -10;
//             ub[d] = 10;
//         }
//     }
// }


void initilize_params(int Pr)
{
    int d;
    double LB[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.078,0.078,0,21,21};
    double UB[] = {1,17,17,1,199,199,1,122,122,1,99,99,1,846,846,1,67.1,67.1,1,2.42,2.42,1,81,81};
    if (Pr == 0) 
    {
        D = 24;
        obj_val = 0;
        acc_err = 1.0e-5;
        for (d = 0; d < D; d++)
        {
            lb[d] = LB[d];
            ub[d] = UB[d];
        }
    }
}



// cd C:\Users\ADMIN\Desktop\SMO_Git\SM_RuleMiner\SMO Code C++