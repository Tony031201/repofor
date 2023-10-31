#include "defs.h"
#define extern_
#include "data.h"
#undef extern_
#include "decl.h"
#include <errno.h>

//initialise global variables
static void init(){
	Line=1;
	Putback='\n';
}

//print out a usage if started incorrectly
static void usage(char *prog){
	fprintf(stderr,"Usage: %s infile\n",prog);
	exit(1);
}

//list of printable tokens
char *tokstr[]={"+","-","*","/","intlit"};

//Loop scanning in all the tokens in the input file.
//print out details of each token found;
static void scanfile(){
	struct token T;

	while(scan(&T)){
		printf("Token %s",tokstr[T.token]);
		if(T.token==T_INTLIT){
			printf(", value %d",T.intvalue);
		}
		printf("\n");
				
	}
}

void main(int argc,char *argv[]){
	if(argc!=2){
		usage(argv[0]);
	}

	init();
	if((Infile = fopen(argv[1],"r"))==NULL){
		fprintf(stderr,"Unable to open %s: %s",argv[1],strerror(errno));
		exit(1);
	}
	
	if((Outfile = fopen("out.s","w"))==NULL){
		fprintf(stderr, "Unable to create out.s: %s\n", strerror(errno));
		exit(1);
	}

	scan(&Token);				//get the first token from the input
	struct ASTnode *n=binexpr(0);		//parse the expression in the file
	printf("%d\n",interpretAST(n));		//calculate the final result
	generatecode(n);

	fclose(Outfile);
	exit(0);
}
