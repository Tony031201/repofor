#include "defs.h"
#include "decl.h"
#include "data.h"

//set a function to manipulate the add and subtract oprator
struct ASTnode *additive_expr(void){
	struct ASTnode *left,*right;
	int tokentype;

	//get the left sub tree
	left=multiplicative_expr();
	tokentype=Token.token;
	if(tokentype==T_EOF){
		return left;
	}

	//loop to create a tree
	while(1){
		//fetch the integer
		scan(&Token);

		//get right sub tree
		right=multiplicative_expr();

		//join two tree
		left=mkastnode(arithop(tokentype),left,right,0);

		//get next token and judge]
		tokentype=Token.token;
		if(tokentype==T_EOF)
			break;
	}
	return left;
}

struct ASTnode *multiplicative_expr(void){
	struct ASTnode *left,*right;
	int tokentype;
	
	//get integer on the left
	//fetch the next token at the same time
	left=primary();

	//get operator
	tokentype=Token.token;
	if(tokentype==T_EOF)
		return left;

	while((tokentype==T_STAR) || (tokentype==T_SLASH)){
		//fetch next integer
		scan(&Token);
		right=pimary();

		//join
		left=mkastnode(arithop(tokentype),left,right,0);

		//update information from Token
		tokentype=Token.token;
		if(tokentype==T_EOF){
			break;
		}
	}

	return left;
}
