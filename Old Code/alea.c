double alea (double a, double b) 
{				// random number (uniform distribution) in  [a b]
	// randOption is a global parameter (see also param.rand)
	double r;

		r=a+(double)rand_kiss()*(b-a)/RAND_MAX_KISS;

	return r; 
}

// ===========================================================
int alea_integer (int a, int b) 
{				// Integer random number in [a b]
	int ir;
	double r;

r=alea(0,1);
	ir = (int) (a + r * (b + 1 - a));

	if (ir > b)	ir = b; 
	return ir;  
}

// ===========================================================
double alea_normal (double mean, double std_dev) 
{ 
	/*
	 Use the polar form of the Box-Muller transformation to obtain a pseudo
	 random number from a Gaussian distribution 
	 */ 
	double x1, x2, w, y1;  
	// double y2;

	do  
	{
		x1 = 2.0 * alea (0, 1) - 1.0;
		x2 = 2.0 * alea (0, 1) - 1.0;
		w = x1 * x1 + x2 * x2;     
	}
	while (w >= 1.0);

	w = sqrt (-2.0 * log (w) / w);
	y1 = x1 * w;
	// y2 = x2 * w;
	if(alea(0,1)<0.5) y1=-y1; 
	y1 = y1 * std_dev + mean;
	return y1;  
}

// ===========================================================
struct velocity alea_sphere(int D, double radius1,double radius2,
							int randType, double randGamma)
{
/*  ******* Random point in a hypersphere ********
 Maurice Clerc 2003-07-11
Last update 2010-02-15

Put  a random point inside the hypersphere S (center 0 
  between radius1 and radius2
  
*/

int 	j;
double   length;
double      r;
struct	velocity	v;

v.size=D;

// ----------------------------------- Step 1.  Direction
    length=0;
   for (j=0;j<D;j++)
   {
          v.v[j]=alea_normal(0,1);
          length=length+v.v[j]*v.v[j];
   }

   length=sqrt(length);
   
if(length>0 && radius2>0)
{
 //----------------------------------- Step 2.   Random radius
  switch(randType)
  {
	default:
	      r=alea(0,1);
	  break;
	  
	  case 1:
	  r=fabs(alea_normal(0,randGamma));
  }

   for (j=0;j<D;j++)
   {
     v.v[j]=r*(radius2-radius1)*v.v[j]/length;
   }
 }
 else
 {
    for (j=0;j<D;j++) v.v[j]=0;
 }  
return v;
}

//==================================================
int aleaInformant(double tab[],int S)
{
	/*
		Define at random an informant, but according to a non uniform distribution
		which is given by the table tab[]
		Note 1: tab doesn't need to be normalised 
	*/
	
	int t;
	double tabCumul[SMax];
	double r;

	tabCumul[0]=tab[0];
	for(t=1;t<S;t++) tabCumul[t]=tabCumul[t-1]+tab[t];

	r=alea(0,tabCumul[t-1]);
	
	for(t=0;t<S;t++)
	{
		if(tabCumul[t]>=r) return t;
	}

return S-1;
}

//==================================================
void aleaIndex(int index[], int S)
{
		int indexTemp[SMax];
	int length;
	int rank;
	int s;
	int t;
	
	length=S;
			for (s=0;s<S;s++) indexTemp[s]=s; //=index[s];

			for (s=0;s<S;s++)
			{
				rank=alea_integer(0,length-1);
				index[s]=indexTemp[rank];
//printf("\nalea152 s %i rank %i",s,rank);//printf("  ");
				if (rank<length-1)	// Compact
				{
					for (t=rank;t<length-1;t++)
						indexTemp[t]=indexTemp[t+1];
				}					
				length=length-1;
			}
}
//============================================================= COEFF_SC
double coeff_SC(int D)
{

	//  The D-cube whose edge is a
	// and  the D-sphere whose radius is r=a*coeff_S_C
	// have the same volume
	double coeff;
	double	c1,c2;
	int		d;
	double	d3;
	double	x;

	int option=0; // 0 => exact value
				// 1 => mean value

if (D==1) return 0.5; // The radius is just the half intervall

	x=(double)D;
	if ((2*(int)(D/2)==D) || option==1) // D even
	{
		d3=1; for (d=2;d<=D/2;d++) d3=d3*d; // (D/2)!
		c1=pow(d3,1/x)/sqrt(pi);
		if (option==0) return c1;
	}

	 // D odd
	{
		d3=1; for (d=2;d<=D;d++) d3=d3*d; // D!
		c2=0.5*pow(d3,1/x)/pow(pi,0.5-0.5/x);
		if (option==0) return c2;
	}

	coeff=(c1+c2)/2;

return coeff;
}
//================================================== KISS
/*
 A good pseudo-random numbers generator

 The idea is to use simple, fast, individually promising
 generators to get a composite that will be fast, easy to code
 have a very long period and pass all the tests put to it.
 The three components of KISS are
 x(n)=a*x(n-1)+1 mod 2^32
 y(n)=y(n-1)(I+L^13)(I+R^17)(I+L^5),
 z(n)=2*z(n-1)+z(n-2) +carry mod 2^32
 The y's are a shift register sequence on 32bit binary vectors
 period 2^32-1;
 The z's are a simple multiply-with-carry sequence with period
 2^63+2^32-1.  The period of KISS is thus
 2^32*(2^32-1)*(2^63+2^32-1) > 2^127
 */

static ulong kiss_x = 1;
static ulong kiss_y = 2;
static ulong kiss_z = 4;
static ulong kiss_w = 8;
static ulong kiss_carry = 0;
static ulong kiss_k;
static ulong kiss_m;


void seed_rand_kiss(ulong seed) 
{
	kiss_x = seed | 1;
	kiss_y = seed | 2;
	kiss_z = seed | 4;
	kiss_w = seed | 8;
	kiss_carry = 0;
}

ulong rand_kiss() 
{
	kiss_x = kiss_x * 69069 + 1;
	kiss_y ^= kiss_y << 13;
	kiss_y ^= kiss_y >> 17;
	kiss_y ^= kiss_y << 5;
	kiss_k = (kiss_z >> 2) + (kiss_w >> 3) + (kiss_carry >> 2);
	kiss_m = kiss_w + kiss_w + kiss_z + kiss_carry;
	kiss_z = kiss_w;
	kiss_w = kiss_m;
	kiss_carry = kiss_k >> 30;
	return kiss_x + kiss_y + kiss_w;
}
