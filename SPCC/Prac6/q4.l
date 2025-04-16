%option noyywrap

%{
    #include <stdio.h>
    #include <string.h>

    int keyword_count = 0;
    int identifier_count = 0;
    int number_count = 0;
    int operator_count = 0;
    int special_count = 0;

    char *keywords[] = {
        "if", "else", "while", "for", "return",
        "int", "float", "char", "double", "void"
    };

    int is_keyword(const char *str) {
        for (int i = 0; i < sizeof(keywords)/sizeof(keywords[0]); i++) {
            if (strcmp(str, keywords[i]) == 0)
                return 1;
        }
        return 0;
    }
%}

IDENT      [a-zA-Z_][a-zA-Z0-9_]*
NUMBER     [0-9]+
OPERATOR   [+\-*/=<>!]+
SPECIAL    [(){};,]
WHITESPACE [ \t\n]+

%%

{NUMBER}      { number_count++; printf("NUMBER: %s\n", yytext); }
{IDENT}       {
                  if (is_keyword(yytext)) {
                      keyword_count++;
                      printf("KEYWORD: %s\n", yytext);
                  } else {
                      identifier_count++;
                      printf("IDENTIFIER: %s\n", yytext);
                  }
              }
{OPERATOR}    { operator_count++; printf("OPERATOR: %s\n", yytext); }
{SPECIAL}     { special_count++; printf("SPECIAL SYMBOL: %s\n", yytext); }
{WHITESPACE}  ; // Ignore spaces, tabs, newlines
.             { printf("UNKNOWN TOKEN: %s\n", yytext); }

%%

int main() { 
    yylex();
    printf("\n--- Token Summary ---\n");
    printf("Keywords: %d\n", keyword_count);
    printf("Identifiers: %d\n", identifier_count);
    printf("Numbers: %d\n", number_count);
    printf("Operators: %d\n", operator_count);
    printf("Special Symbols: %d\n", special_count);
    return 0;
}
