%option noyywrap

%{
    #include <stdio.h>

    int uppercount = 0;
    int lowercount = 0;

    void incrementCounter(int *count) {
        (*count)++;
    }
%}

UC  [A-Z]
LC  [a-z]

%%

{UC} { incrementCounter(&uppercount); }
{LC} { incrementCounter(&lowercount); }

%% 

int main() {
    printf("Give Input: ");
    yylex();
    printf("\nUppercase Words: %d\n", uppercount);
    printf("Lowercase Words: %d\n", lowercount);
    return 0;
}
