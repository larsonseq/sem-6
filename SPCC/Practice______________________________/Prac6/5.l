%option noyywrap

%{
    #include<stdio.h>
    #include<stdlib.h>
    #include<string.h>
    int lowercase = 0;
    int upper = 0;
%}

%%

[a-z]+ {
    lowercase++;
}

[a-z]*[A-Z]+[a-z]* {
    upper++;
}

[ \t\r] {

}

\n {
    printf("Lowercase: %d\t Uppercase: %d\n", lowercase, upper);
}

. {

}


%%

int main() {
    yylex();

    return 0;
}