#include <stdio.h>
#include "Convert.h"
int main() {
    int x, y, ans1, ans2, option;
	double a, b;  
	option = 1;
	while (option != 0) {
		printf("1.Celcius To Farhenheit\t2.Farhenheit to Celcius\t");
		printf("3.Metre To Feet \n4.Feet to Metre\t"); 
        printf("5.Litre to Cubic Feet \t6.Cubic Feet to Litre\n"); 
		printf("Enter Your Option: ");		
		scanf("%d", &option);
		switch (option) {
		    case 1: {
			    printf("Enter Celcius: ");
				scanf("%lf", &a);  
				printf("\tFarhenheit : %lf\n", celciusToFarhenheit(a));
				break; 
			}
			case 2: {
			    printf("Enter Farhenheit: ");
				scanf("%lf", &a);  
				printf("\tCelcius : %lf\n", farhenheitToCelcius(a));
				break; 
			}
			case 3: {
			    printf("Enter Metre: ");
				scanf("%lf", &a);  
				printf("\tFeet : %lf\n", metreToFeet(a));
				break; 
			}
			case 4: {
			    printf("Enter Feet: ");
				scanf("%lf", &a);  
				printf("\tMetre : %lf\n", feetToMetre(a));
				break; 
			}
            case 5: {
			    printf("Enter Litre: ");
				scanf("%lf", &a);  
				printf("\tCubic Feet : %lf\n", litreToCubicFoot(a));
				break; 
			}
            case 6: {
			    printf("Enter Cubic Feet: ");
				scanf("%lf", &a);  
				printf("\tLitre : %lf\n", cubicFootToLitre(a));
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