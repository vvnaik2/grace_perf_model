#include <stdio.h>
#include <stdlib.h>
#include "common.h"

#define ASIZE 4096
#define ITERS 512

double loop(int zero) {
  int i, iters;
  double t1;
  float *src = (float*) malloc(sizeof(float) * ASIZE);
  float *dest = (float*) malloc(sizeof(float) * ASIZE);
  for(iters=zero; iters < ITERS; iters+=1) {
    for(i=zero; i < ASIZE; i+=1) {
      dest[i] += 2 * src[i];
    }
    t1 = dest[ASIZE-1];
  }
  return t1;
}

int main(int argc, char* argv[]) {
   argc&=1000;
   ROI_BEGIN();
   int t=loop(argc);
   ROI_END();
   volatile int a = t;
}
