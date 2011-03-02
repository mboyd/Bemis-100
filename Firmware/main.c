/* Name: main.c
 * Author: <insert your name here>
 * Copyright: <insert your copyright message here>
 * License: <insert your license reference here>
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>

#define NUM_BOARDS 83

#define FOSC 11059200	// Clock Speed 
//#define BAUD 9600		//230400
//#define MYUBRR (FOSC/(16*BAUD))-1		// Not valid in 2x serial mode 
#define MYUBRR 5						// 230.4k baud, see page 198 of the datasheet

#define PWM_LEN 16
/* const uint8_t pwm_interleave[PWM_LEN] = {0, 4, 1, 5, 2, 6, 3, 7}; */

static const uint8_t pwm_interleave[PWM_LEN] = {8, 136,  72, 200,  40, 168, 104, 232,  24, 152,  88, 216,  56, 184, 120, 248};

/* const uint8_t bitmask[8] = {0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80}; */

#define RED_MASK 0xC
#define GREEN_MASK 0x2
#define BLUE_MASK 0x1

uint8_t frame[NUM_BOARDS*6];
uint16_t frame_addr = 0;

void USART_Init(uint16_t ubrr) {
	UBRR0H = (uint8_t)(ubrr>>8);		//Set baud
	UBRR0L = (uint8_t) ubrr;
											//Enable receiver and transmitter
	UCSR0A |= (1<<U2X0) |					//Double data rate
			  (0<<MPCM0);					//We wont need this
	
	UCSR0B = (1<<RXEN0)|(1<<TXEN0) |		//Enable tx, rx
				(1<<RXCIE0);				//Enable rx interrupt
	
	UCSR0C = (0<<UMSEL01) | (0<<UMSEL00) |	//Async USART mode
		(0<<UPM01)  | (0<<UPM00)  |			//No parity
		(0<<USBS0)  |						//1 stop bit										
		(1<<UCSZ01) | (1<<UCSZ00);			//8 data bits
	
	sei();			// Enable interrupts
}

void USART_Transmit(uint8_t data) {
	while (!( UCSR0A & (1<<UDRE0))) {}
	UDR0 = data;
}

uint8_t USART_Receive() {
	while (!(UCSR0A & (1<<RXC0))) {}
	return UDR0;
}

void push(uint8_t c) {
	uint8_t i;
	for (i = 0; i<8; i++) {
		PORTA = (c>>i)&1;
		PORTA = 2;
		PORTA = 0; //&=~2;
	}
	// Assuming loop unrolling, 8 * (3+1+1) = 40 cycles
}

void latch_out() {
	PORTA = 4;
	PORTA = 0; //&=~4;
}

ISR(USART0_RX_vect) {	//USART_RX for atmega48
	uint8_t c;
	c = UDR0;
	if (c == 'B') {
		frame_addr = 0;
	} else {
		frame[frame_addr++] = c;
	}
}

int main(void) {
	register uint8_t i, j;
	register uint8_t pwm_index;
	
	register uint8_t lred, lgreen, lblue;
	register uint8_t hred, hgreen, hblue;
	
	register uint8_t ln, hn;
	register uint8_t b;
	
	PORTA = 0;
	DDRA = 0x07;			//output on C0, clock on C1, C2 is output latch
	USART_Init(MYUBRR);
	
	uint8_t selftest[4] = {0xCC, 0x22, 0x11, 0x00};	// R, G, B, off
	for (j = 0; j < 4; j++) {
		for (i = 0; i < NUM_BOARDS; i++) {
			push(selftest[j]);
		}
		latch_out();
		_delay_ms(700);
	}
	
	pwm_index = 0;
	
	for (;;) {
		pwm_index += 1;
		pwm_index %= 16;
		
		for (i = NUM_BOARDS*6-6; i >= 0; i-=6) {
			// Onboard
			hred = frame[i];
			hgreen = frame[i+1];
			hblue = frame[i+2];
			// Slave
			lred = frame[i+3];
			lgreen = frame[i+4];
			lblue = frame[i+5];
			// 5 adds + 6 ram hits @ 2 cycles each => 17 cycles
			
			b = pwm_interleave[pwm_index];
			
			ln = (lred > b) ? RED_MASK : 0;
			ln |= (lgreen > b) ? GREEN_MASK : 0;
			ln |= (lblue > b) ? BLUE_MASK : 0;
			
			hn = (hred > b) ? RED_MASK : 0;
			hn |= (hgreen > b) ? GREEN_MASK : 0;
			hn |= (hblue > b) ? BLUE_MASK : 0;
			
			b = hn<<4 | ln;
			// 2 * (3+4+4) + 3 = 25 cycles
			
			push(b);
			// 40 cycles IO
		}
			// Total: approx 80 cycles / board
			// 83*80 = 6640 cycles / pwm frame
			// 12MHz / 6640 = 1807 Hz PWM
		
		latch_out();
	}
	
	return 0;
}

