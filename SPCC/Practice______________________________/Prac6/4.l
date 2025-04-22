%option noyywrap

%{
    #include<stdio.h>
    #include<stdlib.h>
    #include<string.h>

    char keywords[50][50];
    int count = 0;
%}

%%

"int"|"if"|"else"|"include" {
    strcpy(keywords[count++], yytext);
}

[ \t\n\r]+  {
    /* Skip whitespace characters */;
    // Need this because it will print empty lines to the console
}

 . {
    // Do nothing hehe
 }

%%

int main() {
    yylex();

    for(int i = 0; i < count ; i++) {
        printf("%s\n", keywords[i]);
    }


    return 0;
}