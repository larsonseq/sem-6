%option noyywrap

%{
    #include<stdio.h>
%}

%% 

[ \n] { printf("Hello World");}

%% 

int main() {
    yylex();

    return 0;
}