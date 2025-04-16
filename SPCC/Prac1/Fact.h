#define fact(num) \
    for(i = 1; i <= num; i++) { \
        f *= i; \
    } \
    printf("Factorial of %d is %ld", num, f);
