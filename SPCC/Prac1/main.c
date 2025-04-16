#include <stdio.h>
#include "cal.h" 

int main() {

    int x, y, ans1, ans2, option;
	double a, b;  
	
	option = 1;
	while (option != 0) {
		printf("1.Addition\t2.Subtraction \t3.Multiplication\t");
		printf("4.Division \n5.Exponent (a^b) \t6.Square\t");
		printf("7.Cube\t8.Square Root\t9.Cube Root\n\n");

		printf("Enter Your Option: ");		
		scanf("%d", &option);
		
		switch (option) {
		    case 1: {
			    printf("Enter Value 1: ");
				scanf("%d", &x);
				printf("Enter Value 2: ");
				scanf("%d", &y);
				printf("\tAnswer : %d\n", add(x, y));
				break; 
			}
			case 2: {
			    printf("Enter Value 1: ");
				scanf("%d", &x);
				printf("Enter Value 2: ");
				scanf("%d", &y);
				printf("\tAnswer : %d\n", sub(x, y));
				break; 
			}
			case 3: {
			    printf("Enter Value 1: ");
				scanf("%d", &x);
				printf("Enter Value 2: ");
				scanf("%d", &y);
				printf("\tAnswer : %d\n", multiply(x, y));
				break; 
			}
			case 4: {
			    printf("Enter Value 1: ");
				scanf("%lf", &a);
				printf("Enter Value 2: ");
				scanf("%lf", &b);
				if (b == 0) {
					printf("Error! Division by zero.\n");
				} else {
					printf("\tAnswer : %lf\n", divide(a, b));
				}
				printf("\tAnswer : %lf\n", divide(a, b));
				break; 
			}
			case 5: {
			    printf("Enter Value 1: ");
				scanf("%lf", &a);
				printf("Enter Value 2: ");
				scanf("%lf", &b);
				printf("\tAnswer : %lf\n", power(a, b));
				break; 
			}
			case 6: {
			    printf("Enter Value 1: ");
				scanf("%lf", &a); 
				printf("\tAnswer : %lf\n", square(a));
				break; 
			}
			case 7: {
			    printf("Enter Value 1: ");
				scanf("%lf", &a); 
				printf("\tAnswer : %lf\n", cube(a));
				break; 
			}
			case 8: {
				printf("Enter Value 1: ");
				scanf("%lf", &a); 
				printf("\tAnswer : %lf\n", root2(a));
				break; 
			}
			case 9: {
				printf("Enter Value 1: ");
				scanf("%lf", &a); 
				printf("\tAnswer : %lf\n", root3(a));
				break; 
			}
			default: {
			    option = 0;
				break;
			}
		}
		printf("\n");
	}
	
	
	return 0;
}

