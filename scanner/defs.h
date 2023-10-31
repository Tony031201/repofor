#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

struct token{
	int token;
	int intvalue;
};

enum {
	T_EOF,T_PLUS,T_MINUS,T_STAR,T_SLASH,T_INTLIT
};

enum {
	A_ADD, A_SUBTRACT, A_MULTIPLY, A_DIVIDE, A_INTLIT
};

struct ASTnode {
	int op;				// "Operation" to be performed on this tree
	struct ASTnode *left;		// Left and right child trees
	struct ASTnode *right;
	int intvalue;			// For A_INTLIT, the integer value
};
