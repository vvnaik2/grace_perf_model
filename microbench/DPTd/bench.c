#include <stdio.h>
#include "common.h"
#include "math.h"

#define ASIZE   8192
#define ITERS   128 

double arrA[ASIZE];
double arrB[ASIZE];

__attribute__ ((noinline))
double loop(int zero) {
  double t1 = zero * zero + zero + 1 ;

  for(int iters=0; iters < ITERS; iters+=1) {
    for(int i=0; i < ASIZE; i+=1) {
      arrB[i] = (arrA[i])/t1 ;
    }
    t1 += arrB[ASIZE-1];
  }

  return t1;
}

int main(int argc, char* argv[]) {
   argc&=10000;
   ROI_BEGIN(); 
   int t=loop(argc); 
   ROI_END();
   volatile double a = t;
}
