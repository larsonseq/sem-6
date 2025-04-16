#include <stdio.h>
#include "Area.h"
int main() {
    int x, y, ans1, ans2, option;
	double a, b;   
	option = 1;
	while (option != 0) {
		printf("1.Square\t2.Rectangle\t");
		printf("3.Triangle \t4.Circle\n"); 

		printf("Enter Your Option: ");		
		scanf("%d", &option);
		
		switch (option) {
		    case 1: {
			    printf("Enter Length of Side: ");
				scanf("%lf", &a);  
				printf("\tAnswer : %lf\n", areaOfSquare(a));
				break; 
			}
			case 2: {
			    printf("Enter Length: ");
				scanf("%lf", &a);
				printf("Enter Breadth: ");
				scanf("%lf", &b);
				printf("\tAnswer : %lf\n", areaOfRectangle(a, b));
				break; 
			}
			case 3: {
			    printf("Enter base: ");
				scanf("%lf", &a);
				printf("Enter height: ");
				scanf("%lf", &b);
				printf("\tAnswer : %lf\n", areaOfTriange(a, b));
				break; 
			}
			case 4: {
			    printf("Enter Radius: ");
				scanf("%lf", &a); 
				printf("\tAnswer : %lf\n", areaOfCircle(a));
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