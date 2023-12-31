#include "defs.h"
#include "data.h"
#include "decl.h"

//get the next character from the input file
static int next(void){
	int c;

	if(Putback){
		c=Putback;	//use the character put
		Putback=0;	//back if there is one
		return c;
	}

	c=fgetc(Infile);	//read from inpit file
	if('\n' == c)
		Line++;		//increment line count;
	return c;
}

//put back an unwanted character
static void putback(int c){
	Putback=c;
}

//skip past input that we don't need to deal with,
//i.e. whitesoace, newlines. return the first
//character we do need to deal with
static int skip(void){
	int c;
	c=next();
	while(' ' == c || '\t' == c || '\n' == c || '\r' == c || '\f' == c){
		c=next();

	}
	return(c);
}

//return the position of character c
//in string s, or -1 if c not found
static int chrops(char *s,int c){
	char *p;
	p=strchr(s,c);
	return (p ? p-s : -1);
}

//scan and return an integer literal
//value from the input file. Store
//the value as a string in Text.
static int scanint(int c){
	int k,val=0;
	//covert each character into an int value
	while((k=chrops("0123456789",c))>=0){
		val=val*10+k;
		c=next();
	}
	
	//we hit a non-integer character,put it back
	putback(c);
	return val;
}

//scan an identifier from the input file and
//store it in buf[]. return the identifier's length
static int scanident(int c,char *buf, int lim){
	int i = 0;
	//allow digit, alpha and underscores
	//else append to buf[] and get next character
	while (isalpha(c) || isdigit(c) || c == '_') {
		if (lim - 1 ==i){
			printf("identifier too long on line%d\n",Line);
			exit(1);
		}else if(i < lim - 1){
			buf[i++]=c;
		}
		c=next();	
	}
	//when hit a non-valid character, put it back.
	//null-terminate the buf[] and return the length
	putback(c);
	buf[i]='\0';
	return i;
}

//scan and return the next token found in the input.
//Return 1 if token valid, 0 if no tokens left.
int scan(struct token *t){
	int c;

	//skip whitespace
	c=skip();
	//determine the token based on
	//the input character
	switch(c){
		case EOF:
			t->token=T_EOF;
			return 0;
		case '+':
			t->token=T_PLUS;
			break;
		case '-':
			t->token=T_MINUS;
			break;
		case '*':
			t->token=T_STAR;
			break;
		case '/':
			t->token=T_SLASH;
			break;
		default:
			//If it's a digit, scan the
			//literal integer value in
			if(isdigit(c)){
				t->intvalue=scanint(c);
				t->token=T_INTLIT;
				break;
			}

			printf("Unrecognised character %c on line %d\n",c,Line);
			exit(1);
	}

	//when the code reach here, it means
	//we get a valid token
	return 1;
}
