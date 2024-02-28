#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 65536 // number of possible values

int main()
{
    int arr[N] = {0}; // array to keep track of generated values
    int count = 0, num, i;

    // initialize random number generator
    srand(time(NULL));

    // generate non-repeated random numbers
    do {
        num = rand() % N;
        if (arr[num] == 0) {
            arr[num] = 1;
            count++;
            printf("%d ", num);
        }
    } while (count < N);

    printf("\n");

    return 0;
}