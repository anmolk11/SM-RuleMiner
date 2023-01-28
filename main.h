
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define ulong unsigned long // To generate pseudo-random numbers with KISS
#define RAND_MAX_KISS ((unsigned long) 4294967295)

#define	DMax 32			// Max number of dimensions of the search space
										// Limited because of the "orthogonal learning" option,
										// which may make use of a predefined orthogonal array
										// read on a file. Of course, it could be increased
										// but you have then to define new (and bigger) orthogonal
										// arrays
#define fMax 6			// Max number of constraints +1
#define RMax 101		// Max number of runs
#define	SMax 200		// Max swarm size

#define zero  1.0e-30	// To avoid numerical instabilities with some compilers
#define infinity 1.0e30
#define MMax 500 // Max size of a "memory" list (cf Lennard-Jones problem)
#define NMax 1000		// Max number of points when the landscape is read on a file

#define ERROR(a) {printf("\nERROR: %s\n", a);exit(-1);}

//-------------------- Structures
struct quantum 
{
	double q[DMax];
	int size; 
};

struct SS 
{ 
	int D;
	double max[DMax];  	// Initialisation, and feasible space
	double maxInit[DMax];
	double min[DMax]; 
	double minInit[DMax];
	struct quantum q;		// Quantisation step size. 0 => continuous problem
	double maxS[DMax];	// Search space
	double minS[DMax];
	int valueNb; 		 	// if >0, the search space is a list of "valueNb"values.
};

struct param 
{

	double w; 			// Inertial weight
	double c1;			// Confidence coefficient
	double c2;			// Idem		
	int formula; 		// Formula for stagnation
	int S;				// Initial swarm size 
	double spreadProba; // probability threshold
	int rule1;			// To use different options for Rule 1
	int rule2;
};

struct fitness 
{
	int size; 
	double f[fMax];
};

struct position 
{ 
	struct fitness f;				// Fitness value  + constraints <=0
	int size;				// Number of dimensions  D
	double x[DMax];		// Coordinates
};

struct archive {
	struct position M[MMax]; // Memorise positions
	int rank;
	int size;
	};

struct velocity 
{  
	int size;				// Number of dimensions D  
	double v[DMax]; 		// Components
};

struct problem 
{ 
	int constraint;			// Number of constraints
	double epsilon; 		// Admissible error
	double epsConstr;  // Admissible error for each constraint
	int evalMax; 			// Maximum number of fitness evaluations
	int function; 		// Function code
	double objective; 	// Objective value					
	struct position solution; // Solution position (if known, just for tests)	
	struct SS SS;			// Search space
};


struct swarm 
{ 
	int best; 				// Rank of the best particle
	struct position P[SMax];	// Previous best positions found by each particle
	int S; 					// Swarm size 
	struct velocity V[SMax];	// Velocities
	struct position X[SMax];	// Positions
//	int worst;				// Rank of the worst particle
};

struct result 
{  
	double nEval; 			// Number of evaluations  
	struct swarm SW;			// Final swarm
	struct fitness error;				// Numerical result of the run
	double convRate; 			// For information: how fast was the convergence
};

//struct sF{int s; double f;}; // To sort the positions according to the fitness

//struct lBest {int rank; double x[DMax];}; // To sort the local bests

struct xv // For move and confinement subprograms
{
	struct position x; 
	struct velocity v;
}; 

// Spefific to some uses  
struct landscape {int N;double x[NMax];double fx[NMax];}; // 1D-landscape


// -------------------- Sub-programs
double alea (double a, double b);
void aleaIndex(int index[], int S);
int aleaInformant(double tab[],int S);
double alea_normal (double mean, double stdev);
int alea_integer (int a, int b);
struct velocity alea_sphere(int D, double radius1,double radius2,
							int randType, double randGamma);
							
int betterThan(struct fitness f1, struct fitness f2);
int best(struct swarm SW);

double cEdge(double w);
double coeff_SC(int D);
static int compareDoubles (void const *a, void const *b); // To sort a list
struct xv confinement(struct xv xv, struct problem pb);
struct fitness constraint(struct position x, int functCode, double eps);

struct position discrete(struct position pos, struct problem pb);
double distanceL(struct position x1, struct position x2, double L);

double errorFC(struct fitness f); // Total error, including constraints

double max(double a,double b);
void memSave(struct position P);
double min(double a,double b);

double normL (struct velocity v,double L);	

struct position initFar(struct problem pb, struct param param);
struct position initPos(struct SS SS);
struct velocity initVel(struct position pos, struct SS SS);

double lennard_jones (struct position x) ;

struct xv move(struct result R, int s, int g, struct problem pb, struct param param);

struct fitness perf (struct position x, struct problem pb);	// Fitness evaluation
double potentiel(struct position X, struct archive list);
struct problem problemDef(int functionCode, FILE *data);
struct result PSO ( struct param param, struct problem problem, int level);
struct result PSO_A ( struct param param, struct problem problem, int level);
ulong	rand_kiss(); // For the pseudo-random number generator KISS

struct position quantis (struct position x, struct SS SS);
void	seed_rand_kiss(ulong seed); 
int sign (double x);
int spreadIter(double spreadProba, int S,int formula);

struct position valueAccept(struct position x, int valueNb);

int worst(struct swarm SW);

// Global variables
int dLBest; 			// For information 
long double E;			// exp(1). Useful for some test functions
struct landscape funct; // When (x,f(x)) is read from a file
//int iter;
struct archive memPos;
double nEval;			// Number of fitness evaluations
long double pi;			// Useful for some test functions
int run;


// For Cutting stock
// http://en.wikipedia.org/wiki/Cutting_stock_problem
static float valueList[5]=
{1380, 1820, 1930, 2050, 2150};
static int pieceNb[5]={15,6,3,12,15};
static float toCut=5600;

// File(s);
//FILE * f_run;
FILE * f_synth;
FILE * f_expl;
FILE * fLandscape;
FILE * f_init;
FILE * f_init_save;

FILE * f_coeff;

FILE *f_swarm; // For information about the variable swarm size

