#ifndef COMMON_H
#define COMMON_H

#ifdef FF //Ignore this.
#include <stdlib.h>

#define ROI_BEGIN() \
  __asm__ __volatile__(".byte 0x0f\n\t.byte 0x27\n\t.byte 0x00\n\t.byte 0x0b")
#define ROI_END() \
  exit(0)
  //_exit(0)

#elif MAGIC //current default

//Magic only works for X86 right now
#define ROI_BEGIN() \
  __asm__ __volatile__ ("xchg %bx,%bx");
#define ROI_END() \
  __asm__ __volatile__ ("xchg %cx,%cx");


#define DETAILED_SIM_STOP() \
    _exit(0)
#else // Ignore this for now -- put working timing code here
#define ROI_BEGIN() \
    clock_t start, end;\
    start = clock();
#define ROI_END() \
    end = clock(); \
    double duration = ((double)end - start)/CLOCKS_PER_SEC;\
    printf("_ticks: %f s\n",duration);

#include <time.h>


// typedef unsigned long long ticks;
// static inline __attribute__((always_inline)) ticks _ClockGetTime()
// {
//   //return -1;
//   //struct timespec ts;
//   //clock_gettime(CLOCK_REALTIME, &ts);
//   //return (ticks)(ts.tv_sec) * 1000000LL + (ticks)(ts.tv_nsec) / 1000LL;
// }

#endif // NO MAGIC

#endif //define COMMON_H
