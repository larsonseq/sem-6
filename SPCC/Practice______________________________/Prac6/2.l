%option noyywrap

%{
    #include<stdio.h>
    int count = 0;
%}

REGEX [a-z]*[A-Z]+[A-Za-z]*

%%

{REGEX} {
    count++;
}

\n {
    printf("Count : %d", count);
}

. {
    
}

%%

int main() {
    yylex();
    return 0;
}