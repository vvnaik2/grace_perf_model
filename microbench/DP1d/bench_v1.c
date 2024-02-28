#include <stdio.h>
#include "common.h"

#define ASIZE  8192
#define ITERS   256 

double arrA[ASIZE];
double arrB[ASIZE];

__attribute__ ((noinline)) 
double loop(int zero) {
  int i, iters;
  double t1;

  for(iters=0; iters < ITERS; iters+=1) {
    for(i=0; i < ASIZE; i+=1) {
      arrA[i]=arrA[i]* 3.2 + arrB[i];
    }
    t1+=arrA[ASIZE-1];
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
