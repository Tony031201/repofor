; a2-signalling.asm
; CSC 230: Summer 2023
;
; Student name:weiting ye
; Student ID:V00999670
; Date of completed work:JUNE 13th
;
; *******************************
; Code provided for Assignment #2
;
; Author: Mike Zastre (2022-Oct-15)
; Modified: Sudhakar Ganti (2023-May-31)
 
; This skeleton of an assembly-language program is provided to help you
; begin with the programming tasks for A#2. As with A#1, there are "DO
; NOT TOUCH" sections. You are *not* to modify the lines within these
; sections. The only exceptions are for specific changes changes
; announced on Brightspace or in written permission from the course
; instructor. *** Unapproved changes could result in incorrect code
; execution during assignment evaluation, along with an assignment grade
; of zero. ****

.include "m2560def.inc"
.cseg
.org 0

; ***************************************************
; **** BEGINNING OF FIRST "STUDENT CODE" SECTION ****
; ***************************************************

	; initializion code will need to appear in this
    ; section
	ldi r17,0xff
	sts DDRL,r17
	out DDRB,r17
	clr r17

	ldi r16,LOW(RAMEND)
	out SPL,r16
	ldi r17,HIGH(RAMEND)
	out SPH,r17
	clr r17
	clr r16



; ***************************************************
; **** END OF FIRST "STUDENT CODE" SECTION **********
; ***************************************************

; ---------------------------------------------------
; ---- TESTING SECTIONS OF THE CODE -----------------
; ---- TO BE USED AS FUNCTIONS ARE COMPLETED. -------
; ---------------------------------------------------
; ---- YOU CAN SELECT WHICH TEST IS INVOKED ---------
; ---- BY MODIFY THE rjmp INSTRUCTION BELOW. --------
; -----------------------------------------------------

	rjmp test_part_b
	; Test code


test_part_a:
	ldi r16, 0b00100001
	rcall configure_leds
	rcall delay_long

	clr r16
	rcall configure_leds
	rcall delay_long

	ldi r16, 0b00111000
	rcall configure_leds
	rcall delay_short

	clr r16
	rcall configure_leds
	rcall delay_long

	ldi r16, 0b00100001
	rcall configure_leds
	rcall delay_long

	clr r16
	rcall configure_leds

	rjmp end


test_part_b:
	ldi r17, 0b00101010
	rcall slow_leds
	ldi r17, 0b00010101
	rcall slow_leds
	ldi r17, 0b00101010
	rcall slow_leds
	ldi r17, 0b00010101
	rcall slow_leds

	rcall delay_long
	rcall delay_long

	ldi r17, 0b00101010
	rcall fast_leds
	ldi r17, 0b00010101
	rcall fast_leds
	ldi r17, 0b00101010
	rcall fast_leds
	ldi r17, 0b00010101
	rcall fast_leds
	ldi r17, 0b00101010
	rcall fast_leds
	ldi r17, 0b00010101
	rcall fast_leds
	ldi r17, 0b00101010
	rcall fast_leds
	ldi r17, 0b00010101
	rcall fast_leds

	rjmp end

test_part_c:
	ldi r16, 0b11111000
	push r16
	rcall leds_with_speed
	pop r16

	ldi r16, 0b11011100
	push r16
	rcall leds_with_speed
	pop r16

	ldi r20, 0b00100000
test_part_c_loop:
	push r20
	rcall leds_with_speed
	pop r20
	lsr r20
	brne test_part_c_loop

	rjmp end


test_part_d:
	ldi r21, 'E'
	push r21
	rcall encode_letter
	pop r21
	push r25
	rcall leds_with_speed
	pop r25

	rcall delay_long

	ldi r21, 'A'
	push r21
	rcall encode_letter
	pop r21
	push r25
	rcall leds_with_speed
	pop r25

	rcall delay_long


	ldi r21, 'M'
	push r21
	rcall encode_letter
	pop r21
	push r25
	rcall leds_with_speed
	pop r25

	rcall delay_long

	ldi r21, 'H'
	push r21
	rcall encode_letter
	pop r21
	push r25
	rcall leds_with_speed
	pop r25

	rcall delay_long

	rjmp end


test_part_e:
	ldi r25, HIGH(WORD02 << 1)
	ldi r24, LOW(WORD02 << 1)
	rcall display_message_signal
	rjmp end

end:
    rjmp end






; ****************************************************
; **** BEGINNING OF SECOND "STUDENT CODE" SECTION ****
; ****************************************************

configure_leds:
	; pushing registers in use
	push r16
	push r17
	push r18
	nop
	ldi r18,0x00
	ldi r17,0x00
	check0:
	sbrc r16,0	;checking if bit position 0 in r16 is set
	ldi r18,0b10000000
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 7
	clr r18
	nop
	check1:
	sbrc r16,1	;checking if bit position 1 in r16 is set
	ldi r18,0b00100000
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 5
	clr r18
	nop
	nop
	check3:
	sbrc r16,2	;checking if bit position 2 in r16 is set
	ldi r18,0b00001000
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 3
	clr r18
	nop
	check4:
	sbrc r16,3	;checking if bit position 3 in r16 is set
	ldi r18,0b00000010
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 1
	sts PORTL,r17	;sending r17 to PortL to output results for check 0, 1, 3, and 4
	ldi r17,0x00
	clr r18
	nop
	check5:
	sbrc r16,4	;checking if bit position 4 in r16 is set
	ldi r18,0b00001000
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 3
	clr r18
	nop
	check6:
	sbrc r16,5	;checking if bit position 5 in r16 is set
	ldi r18,0b00000010
	nop
	nop
	add r17,r18	;if it is set, we add value of r18 to r17 in order to set bit 1
	clr r18
	nop
	out PORTB,r17	;sending r17 to PortB to output results for check 5 and 6
	nop
	;popping registers used
	pop r18
	pop r17
	pop r16
	;returning call
	ret


slow_leds:
	;pushing registers in use
	push r16
	push r17
	push r18
	nop
	mov r16,r17	;copy r17 to r16 so we can call set_leds with the correct register
	call configure_leds	;calling configure_leds
	call delay_long	;calling delay_long to delay about 1 sec
	close:
	;sending empty register to PortL and PortB to turn off all the LEDS
	ldi r18,0x00
	sts PORTL,r18
	out PORTB,r18
	nop
	;popping registers used
	pop r18
	pop r17
	pop r16
	;returning call
	ret


fast_leds:
	;pushing registers in use
	push r16
	push r17
	push r18
	nop
	mov r16,r17	;copy r17 to r16 so we can call set_leds with the correct register
	call configure_leds	;calling configure_leds
	call delay_short	;calling delay_short to delay about 0.25 of a sec
	close2:
	;sending empty register to PortL and PortB to turn off all the LEDS
	ldi r18,0x00
	sts PORTL,r18
	out PORTB,r18
	nop
	;popping registers used
	pop r18
	pop r17
	pop r16
	;returning call
	ret


leds_with_speed:
	;pushing registers in use
	push r16
	push r17
	push r30
	push r31
	ldi r17,0x00
	;loading stack pointer to z register
	in r30,SPL
	in r31,SPH

	;loading highest memory addres of stack into r16 - finding the first thing that was pushed onto the stack through the position of the stack pointer
	ldd r16,Z+8
	checksignal:
	;checking if bit 7 and 6 are set in r16
	sbrc r16,6
	inc r17	;using r17 as a counter - incrementing each time the bit is set
	nop
	nop
	checksignal2:
	;checking if bit 7 and 6 are set in r16
	sbrc r16,7
	inc r17
	;using r17 as a counter - incrementing each time the bit is set
	nop
	nop
    check:
		cpi r17,2	;if r17 is 2, call slow_leds to get a 1 sec delay
		brne long
		nop
		nop
		rjmp short	;if r17 is not 2, call long_leds to get a 0.25 sec delay
	short:
		mov r17,r16
		call slow_leds
		rjmp end2
	long:
		mov r17,r16
		call fast_leds
		rjmp end2
	end2:
		nop
	;popping registers used
	pop r31
	pop r30
	pop r17
	pop r16
	ret


; Note -- this function will only ever be tested
; with upper-case letters, but it is a good idea
; to anticipate some errors when programming (i.e. by
; accidentally putting in lower-case letters). Therefore
; the loop does explicitly check if the hyphen/dash occurs,
; in which case it terminates with a code not found
; for any legal letter.

encode_letter:
	;pushing registers in use
	push r16
	push r17
	push r18
	push r30
	push r31
	ldi r25,0x00
	ldi r18,0x00
	;loading stack pointer to z register
	in r30,SPL
	in r31,SPH
	;loading highest memory addres of stack into r16 - finding the first thing that was pushed onto the stack through the position of the stack pointer
	ldd r16,Z+9
	;initializing the z-pointer to access databytes in PATTERNS
	ldi r30,low(PATTERNS<<1)
	ldi r31,high(PATTERNS<<1)
	find:
	;looping through to find letter in memory that corresponds to the value in r17
	lpm r17,Z+
	cp r16,r17
	breq define	;once the correct letter in memory is found,
	rjmp find
	
	define:
	;check which LED should be turn on
	cpi r17,0x01
	breq long2	;define how long the LED light
	cpi r17,0x02 
	;define how long the LED light
	breq short2
	lpm r17,Z+
	cpi r17,0x01
	breq long2
	cpi r17,0x02
	breq short2
	cpi r17,0x6f
	breq on ;if r17 is 'o'£¬turn on the light
	lsl r18
	rjmp define

	on:
	;switch on the LED by left shift the digit in r18
	inc r18
	lsl r18
	rjmp define

	long2:
	lsr r18
	ldi r16,0b11000000 
	add r18,r16	;let the LED light for 1 second.
	mov r25,r18
	rjmp encodefinish

	short2:
	lsr r18 ;let the LED light for 0.25 second.
	mov r25,r18
	rjmp encodefinish

	encodefinish:
	;finish all and pop the stack
	pop r31
	pop r30
	pop r18
	pop r17
	pop r16
	nop
	;return
	ret


display_message_signal:
	;push the data into the stack
	push ZH
	push ZL
	push r24
	push r25
	push r16
	push r17
	;initialize the z pointer
	mov ZH, r25
	mov ZL, r24


	checking:
	;find each letter we need
	lpm r16, Z+	 ;the value store in r16	
	cpi r16, 0x00	
	breq final	;if get 0, we finish	
		
	mov r17, r16			
	push r17				
	rcall encode_letter	;	find letter		
	pop r17							
	push r25				
	rcall leds_with_speed	;define pattern
	rcall delay_long	;wait for a while
	;pop the stack
	pop r25				

	rjmp checking			

	final:
	;pop the stack
	pop r17
	pop r16
	pop r25
	pop r24

	pop ZL
	pop ZH
	;return
	ret


; ****************************************************
; **** END OF SECOND "STUDENT CODE" SECTION **********
; ****************************************************




; =============================================
; ==== BEGINNING OF "DO NOT TOUCH" SECTION ====
; =============================================

; about one second
delay_long:
	push r16

	ldi r16, 14
delay_long_loop:
	rcall delay
	dec r16
	brne delay_long_loop

	pop r16
	ret


; about 0.25 of a second
delay_short:
	push r16

	ldi r16, 4
delay_short_loop:
	rcall delay
	dec r16
	brne delay_short_loop

	pop r16
	ret

; When wanting about a 1/5th of a second delay, all other
; code must call this function
;
delay:
	rcall delay_busywait
	ret


; This function is ONLY called from "delay", and
; never directly from other code. Really this is
; nothing other than a specially-tuned triply-nested
; loop. It provides the delay it does by virtue of
; running on a mega2560 processor.
;
delay_busywait:
	push r16
	push r17
	push r18

	ldi r16, 0x08
delay_busywait_loop1:
	dec r16
	breq delay_busywait_exit

	ldi r17, 0xff
delay_busywait_loop2:
	dec r17
	breq delay_busywait_loop1

	ldi r18, 0xff
delay_busywait_loop3:
	dec r18
	breq delay_busywait_loop2
	rjmp delay_busywait_loop3

delay_busywait_exit:
	pop r18
	pop r17
	pop r16
	ret


; Some tables
;.cseg
;.org 0x800

PATTERNS:
	; LED pattern shown from left to right: "." means off, "o" means
    ; on, 1 means long/slow, while 2 means short/fast.
	.db "A", "..oo..", 1
	.db "B", ".o..o.", 2
	.db "C", "o.o...", 1
	.db "D", ".....o", 1
	.db "E", "oooooo", 1
	.db "F", ".oooo.", 2
	.db "G", "oo..oo", 2
	.db "H", "..oo..", 2
	.db "I", ".o..o.", 1
	.db "J", ".....o", 2
	.db "K", "....oo", 2
	.db "L", "o.o.o.", 1
	.db "M", "oooooo", 2
	.db "N", "oo....", 1
	.db "O", ".oooo.", 1
	.db "P", "o.oo.o", 1
	.db "Q", "o.oo.o", 2
	.db "R", "oo..oo", 1
	.db "S", "....oo", 1
	.db "T", "..oo..", 1
	.db "U", "o.....", 1
	.db "V", "o.o.o.", 2
	.db "W", "o.o...", 2
	.db "W", "oo....", 2
	.db "Y", "..oo..", 2
	.db "Z", "o.....", 2
	.db "-", "o...oo", 1   ; Just in case!

WORD00: .db "Welcome", 0
WORD01: .db "ALL", 0
WORD02: .db "ROADS", 0
WORD03: .db "LEAD", 0, 0
WORD04: .db "TO", 0, 0
WORD05: .db "ROME", 0,0

; =======================================
; ==== END OF "DO NOT TOUCH" SECTION ====
; =======================================

