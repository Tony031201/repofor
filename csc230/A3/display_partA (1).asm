#define LCD_LIBONLY
.include "lcd.asm"

.cseg
#define DELAY 1


#define CLOCK 16.0e6
.equ PRESCALE_DIV=1024  ; implies CS[2:0] is 0b101

;Write timer below:
.equ dly=int(0.5+(CLOCK/PRESCALE_DIV*DELAY))
.if dly>65535
.error "dly is out of range"
.endif

	; set Timer 3
	;
	ldi r17, high(dly)
	ldi r16, low(dly)
	sts OCR3AH, r17
	sts OCR3AL, r16

	ldi r19, 0
	sts TCCR3A, r19

	ldi r19, (1 << WGM32) | (1 << CS32) | (1 << CS30)
	sts TCCR3B, r19
	sei


	call lcd_init			; call lcd_init to Initialize the LCD
	call init_strings
	ldi r24,0
	begin:
	in r19,TIFR3
	sbrc r19,OCF3A
	call blink

	rjmp begin



lp:	jmp lp

blink:

	; This subroutine controll the blink of the lcd

	ldi r19, 1<<OCF3A ;clear bit 1 in TIFR3 by writing logical one to its bit position, P163 of the Datasheet
	out TIFR3, r19

	cpi r24,0				;if r24=0,it means now is the beginning, and jump to case1
	breq case1
	cpi r24,1				;if r24=1,it means now is the 2nd second, and jump to case2
	breq case2
	cpi r24,2				;if r24=2,it means now is the 3rd second, and jump to case3
	breq case3				
	cpi r24,3				;if r24=3,it means we finish one iteration, reset to the begining
	breq case4
	case1:					;the beginning of lcd blink,each line should be display
	call lcd_clr 
	call display_strings1
	call display_strings2
	rjmp end3
	case2:					;the 2nd second,display the first line AND turn off the second line
	call lcd_clr
	call display_strings1
	rjmp end3
	case3:					;the 3rd second,display the second line AND turn off the first line
	call lcd_clr
	call display_strings2
	rjmp end3
	case4:
	clr r24
	rjmp case1
	end3:
	inc r24					;after one blink, r24 increase which means go into the next step
	ret

init_strings:
	push r16
	; copy strings from program memory to data memory
	ldi r16, high(msg1)		; this the destination
	push r16
	ldi r16, low(msg1)
	push r16
	ldi r16, high(msg1_p << 1) ; this is the source
	push r16
	ldi r16, low(msg1_p << 1)
	push r16
	call str_init			; copy from program to data
	pop r16					; remove the parameters from the stack
	pop r16
	pop r16
	pop r16

	ldi r16, high(msg2)
	push r16
	ldi r16, low(msg2)
	push r16
	ldi r16, high(msg2_p << 1)
	push r16
	ldi r16, low(msg2_p << 1)
	push r16
	call str_init
	pop r16
	pop r16
	pop r16
	pop r16

	pop r16
	ret

display_strings1:

	; This subroutine display the string1

	push r16

	; Now move the cursor to the first line (ie. 0,0)
	ldi r16, 0x00
	push r16
	ldi r16, 0x00
	push r16
	call lcd_gotoxy
	pop r16
	pop r16

	; Now display msg1 on the first line
	ldi r16, high(msg1)
	push r16
	ldi r16, low(msg1)
	push r16
	call lcd_puts
	pop r16
	pop r16

	pop r16 
	ret


display_strings2:

	; This subroutine display the string2

	push r16
	; Now move the cursor to the second line (ie. 0,1)
	ldi r16, 0x01
	push r16
	ldi r16, 0x00
	push r16
	call lcd_gotoxy
	pop r16
	pop r16

	; Now display msg2 on the second line
	ldi r16, high(msg2)
	push r16
	ldi r16, low(msg2)
	push r16
	call lcd_puts
	pop r16
	pop r16

	pop r16
	ret


msg1_p:	.db "Weiting Ye", 0	,0
msg2_p: .db "CSC 230: Summer 2023", 0

.dseg
;
; The program copies the strings from program memory
; into data memory.  These are the strings
; that are actually displayed on the lcd
;
msg1:	.byte 200
msg2:	.byte 200
