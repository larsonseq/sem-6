%option noyywrap

%{
    // count the number of lines in source program
    #include<stdio.h>
    int count;
%}

%%

\n {count++;}

. {}

%% 

int main() {
    yylex();
    printf("No of Lines are : %d", count);
    return 0;
}