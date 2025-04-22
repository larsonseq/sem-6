%option noyywrap

%{
    #include<stdio.h>
    int vowels = 0;
    int consonants = 0;
%}

VOWELS [aeiouAEIOU]
CONSONANTS [qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM]

%%

{VOWELS} {
    vowels++;
}

{CONSONANTS} {
    consonants++;
}

\n {
    printf("Consonants: %d\t Vowels: %d\n", consonants, vowels);
}

. {}

%%

int main() {
    printf("Enter input: ");

    yylex();

    return 0;
}