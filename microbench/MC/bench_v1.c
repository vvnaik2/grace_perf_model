#include <stdio.h>
#include "common.h"

#define ASIZE   32768
#define STEP    128
#define ITERS   24

float arr1[ASIZE]; //each of 128 KB 
float arr2[ASIZE];
float arr3[ASIZE];
float arr4[ASIZE];
float arr5[ASIZE];
float arr6[ASIZE];
float arr7[ASIZE];
float arr8[ASIZE];
float arr9[ASIZE];

__attribute__ ((noinline)) 
float loop3(int zero) {
  float f = 0;
  for ( int j= 0; j < ITERS; j++) {
    for(int i = 0; i < ASIZE; i+=1) {
      int ind=i&(STEP-1);
      f+=arr1[ind];
      f+=arr2[ind];
      f+=arr3[ind];
      f+=arr4[ind];
      f+=arr5[ind];
      f+=arr6[ind];
      f+=arr7[ind];
      f+=arr8[ind];
      f+=arr9[ind];
    //f=f*f*f*f*f*f*f*f*f*f*f;
    }
  }
  return f;
}

int main(int argc, char* argv[]) {
   argc&=10000;
   ROI_BEGIN(); 
   float f =loop3(argc);
   ROI_END();
   volatile float a = f;
}