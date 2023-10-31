#include "defs.h"
#include "data.h"
#include "decl.h"

// Convert a token into an AST operation.
int arithop(int tok) {
	switch (tok) {
		case T_PLUS:
			return (A_ADD);
		case T_MINUS:
			return (A_SUBTRACT);
		case T_STAR:
			return (A_MULTIPLY);
		case T_SLASH:
			return (A_DIVIDE);
		default:
			fprintf(stderr,"unknown token is in arithop() on line %d\n",Line);
			exit(1);
	}
}

//parse a primary factor and retrun an 
//AST node representing it
static struct ASTnode *primary(void){
	struct ASTnode *n;

	//for an INTLIT token, make a leaf AST node for it
	//and scan in the next token. Otherwise,a syntax error
	//for any other token type.
	switch(Token.token){
		case T_INTLIT:
			n=mkastleaf(A_INTLIT,Token.intvalue);
			scan(&Token);
			return(n);
		default:
			fprintf(stderr,"syntax erro on line %d\n",Line);
			exit(1);
	}

}

//Operator precedentce for each token
static int OpPrec[]={   0,      10,     10,     20,     20,     0};
//                      EOF     +       -       *       /       INTLIT
//check there is a binary operator and return its precedence
static int op_precedence(int tokentype) {
	int prec = OpPrec[tokentype];
	if (prec == 0) {
		fprintf(stderr, "syntax error on line %d, token %d\n", Line, tokentype);
		exit(1);
	}
	return prec;
}

//return an AST tree whose root is a binary operator
struct ASTnode *binexpr(int ptp){
	struct ASTnode *left,*right;
	int tokentype;

	//Get the integer literal on the left.
	//fetch the next token at the same time.
	left=primary();

	//if no tokens left,return just the left node
	tokentype=Token.token;
	if(tokentype==T_EOF)
		return(left);

	//while the precedence of this token is
	//more than that of the previous token precedence
	while(op_precedence(tokentype)>ptp){
		//Fetch in the next integer literal
		scan(&Token);
		
		//recursively call binexpr() to build right tree
		right=binexpr(OpPrec[tokentype]);
		
		//join two tree
		left=mkastnode(arithop(tokentype),left,right,0);
		
		//update the details of the current token
		tokentype=Token.token;
		if(tokentype==T_EOF)
			return left;
	}

	//return the tree we have when the precedence
	return(left);
}



