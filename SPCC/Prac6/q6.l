%option noyywrap

%{
#include <stdio.h>
#include <string.h>

int coord_conj_found = 0;
int clause_count = 0;

// Coordinating conjunctions list
char *conjs[] = {"and", "but", "or", "nor"};

int is_conj(char *word) {
    for(int i = 0; i < sizeof(conjs)/sizeof(conjs[0]); i++) {
        if(strcmp(word, conjs[i]) == 0)
            return 1;
    }
    return 0;
}

void print_sentence_type() {
    printf("\n--- Sentence Type ---\n");
    if (coord_conj_found)
        printf("This is a Compound Sentence.\n");
    else
        printf("This is a Simple Sentence.\n");
    // Reset for next line
    coord_conj_found = 0;
    clause_count = 0;
}
%}

WORD    [a-zA-Z]+
%%

{WORD} {
    if (is_conj(yytext)) {
        coord_conj_found = 1;
    }
    clause_count++;
}

[ \t]+     ; // Ignore spaces and tabs

\n         { print_sentence_type(); }

.          ; // Ignore punctuation

%%

int main() {
    printf("Enter sentences (press Ctrl+D or Ctrl+Z to exit):\n");
    yylex();
    return 0;
}
