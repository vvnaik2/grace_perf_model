#include <stdio.h>
#include "common.h"

#define STEP    10
#define ITERS   12800
#define ITER2   12

__attribute__ ((noinline))
int loop(int zero) {
  int t;
  for (int k = 0 ; k < ITER2; k++) {
    t = 0;
    int i,iter;
    for(iter=0; iter < ITERS+zero; ++iter) {
      for(i=zero; i < STEP; ++i) {
        switch(i) {
          case 0: t+=1; t|=2; break;
          case 1: t+=4; t|=4; break;
          case 2: t-=4; t|=3; break;
          case 3: t+=2; t|=4; break;
          case 4: t-=3; t|=5; break;
          case 5: t+=2; t|=3; break;
          case 6: t-=3; t|=2; break;
          case 7: t-=1; t|=2; break;
          case 8: t-=2; t|=3; break;
          case 9: t-=1; t|=1; break;
        }
      }
    }
  }
  return t;
}

int main(int argc, char* argv[]) {
   argc&=10000;
   ROI_BEGIN(); 
   int t=loop(argc); 
   ROI_END();
   volatile int a = t;
}
