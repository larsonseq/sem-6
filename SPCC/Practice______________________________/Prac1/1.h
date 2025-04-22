#ifndef mathh
#include<math.h>
#endif

#ifndef stdlibh
#include<stdlib.h>
#endif

#define fact(num) \
    for (i = 1; i <= num; i++) { \
        fact *= i; \
    }

#define areaOfSquare(a) a * a 

#define areaOfRectangle(a, b) a * b

#define greater(a, b) (a > b ? a : b)

// #define DEC_TO_BIN(input) { \
//     { \
//         int temp[64]; \
//         int counter = 0; \
//         if (input == 0) { \
//             printf("0"); \
//         } \
//         else { \
//             int i = 0; \
//             while (input > 0) { \
//                 temp[i] = input % 2; \
//                 input /= 2; \
//                 counter++; \
//                 i++; \
//             } \
//             while(counter > 0) { \
//                 printf("%d", temp[counter - 1]); \
//                 counter--; \
//             } \
//             printf("\n"); \
//         } \
//     } \
// }

// #define DEC_TO_HEX(input) \
// printf("Hello\n");

// #define BIN_TO_DEX(input) { \
//     strtol(input, NULL, 2); \
// }


#define factors(num) { \
    for (int i = 1; i <= num; i++) { \
        if (num % i == 0) { \
            printf("%d is a factor of %d\n", i, num); \
        } \
    } \
}