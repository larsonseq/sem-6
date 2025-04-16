%option noyywrap

%{
    #include <stdio.h>
 
    int consonants = 0;
    int vowels = 0;

    void incrementCounter(int *count) {
        (*count)++;
    }

    void printCount () {
        printf("\nConsonants: %d\n", consonants);
        printf("Vowels: %d\n", vowels);
    }
%}

VOWELS  [aeiouAEIOU]
CONSONANTS  [qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM]

%%

{CONSONANTS} { incrementCounter(&consonants); }
{VOWELS} { incrementCounter(&vowels); }
\n { printCount(); }

%% 

int main() {
    printf("Give Input: ");
    yylex();
    printf("\nConsonants: %d\n", consonants);
    printf("Vowels: %d\n", vowels);

    return 0;
}