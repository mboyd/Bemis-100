/* Name: main.c
 * Author: <insert your name here>
 * Copyright: <insert your copyright message here>
 * License: <insert your license reference here>
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>

#define NUM_BOARDS 100

#define FOSC 11059200	// Clock Speed 
//#define BAUD 9600		//230400
//#define MYUBRR (FOSC/(16*BAUD))-1		// Not valid in 2x serial mode 
#define MYUBRR 5						// 230.4k baud, see page 198 of the datasheet

#define PWM_LEN 8
const uint8_t pwm_interleave[PWM_LEN] = {0, 4, 1, 5, 2, 6, 3, 7};
/*const uint8_t pwm_interleave[PWM_LEN] = 
   {0x00, 0x80, 0x01, 0x81, 0x02, 0x82, 0x03, 0x83, 0x04, 0x84, 0x05, 0x85, 0x06, 0x86,
	0x07, 0x87, 0x08, 0x88, 0x09, 0x89, 0x0a, 0x8a, 0x0b, 0x8b, 0x0c, 0x8c, 0x0d, 0x8d, 
	0x0e, 0x8e, 0x0f, 0x8f, 0x10, 0x90, 0x11, 0x91, 0x12, 0x92, 0x13, 0x93, 0x14, 0x94,
	0x15, 0x95, 0x16, 0x96, 0x17, 0x97, 0x18, 0x98, 0x19, 0x99, 0x1a, 0x9a, 0x1b, 0x9b,
	0x1c, 0x9c, 0x1d, 0x9d, 0x1e, 0x9e, 0x1f, 0x9f, 0x20, 0xa0, 0x21, 0xa1, 0x22, 0xa2,
	0x23, 0xa3, 0x24, 0xa4, 0x25, 0xa5, 0x26, 0xa6, 0x27, 0xa7, 0x28, 0xa8, 0x29, 0xa9,
	0x2a, 0xaa, 0x2b, 0xab, 0x2c, 0xac, 0x2d, 0xad, 0x2e, 0xae, 0x2f, 0xaf, 0x30, 0xb0,
	0x31, 0xb1, 0x32, 0xb2, 0x33, 0xb3, 0x34, 0xb4, 0x35, 0xb5, 0x36, 0xb6, 0x37, 0xb7,
	0x38, 0xb8, 0x39, 0xb9, 0x3a, 0xba, 0x3b, 0xbb, 0x3c, 0xbc, 0x3d, 0xbd, 0x3e, 0xbe,
	0x3f, 0xbf, 0x40, 0xc0, 0x41, 0xc1, 0x42, 0xc2, 0x43, 0xc3, 0x44, 0xc4, 0x45, 0xc5,
	0x46, 0xc6, 0x47, 0xc7, 0x48, 0xc8, 0x49, 0xc9, 0x4a, 0xca, 0x4b, 0xcb, 0x4c, 0xcc,
	0x4d, 0xcd, 0x4e, 0xce, 0x4f, 0xcf, 0x50, 0xd0, 0x51, 0xd1, 0x52, 0xd2, 0x53, 0xd3,
	0x54, 0xd4, 0x55, 0xd5, 0x56, 0xd6, 0x57, 0xd7, 0x58, 0xd8, 0x59, 0xd9, 0x5a, 0xda,
	0x5b, 0xdb, 0x5c, 0xdc, 0x5d, 0xdd, 0x5e, 0xde, 0x5f, 0xdf, 0x60, 0xe0, 0x61, 0xe1,
	0x62, 0xe2, 0x63, 0xe3, 0x64, 0xe4, 0x65, 0xe5, 0x66, 0xe6, 0x67, 0xe7, 0x68, 0xe8,
	0x69, 0xe9, 0x6a, 0xea, 0x6b, 0xeb, 0x6c, 0xec, 0x6d, 0xed, 0x6e, 0xee, 0x6f, 0xef,
	0x70, 0xf0, 0x71, 0xf1, 0x72, 0xf2, 0x73, 0xf3, 0x74, 0xf4, 0x75, 0xf5, 0x76, 0xf6,
	0x77, 0xf7, 0x78, 0xf8, 0x79, 0xf9, 0x7a, 0xfa, 0x7b, 0xfb, 0x7c, 0xfc, 0x7d, 0xfd,
	0x7e, 0xfe, 0x7f, 0xff};*/

const uint8_t bitmask[8] = {0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80};

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
		PORTA |= 2;
		PORTA &=~2;
	}
}

void latch_out() {
	PORTA |= 4;
	PORTA &=~4;
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
	int i, j;
	uint8_t pwm_index;
	
	uint8_t lred, lgreen, lblue;
	uint8_t hred, hgreen, hblue;
	
	uint8_t ln, hn;
	uint8_t b;
	
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
	
	while (1) {
		pwm_index = 0;
		for (pwm_index = 0; pwm_index < 8; pwm_index++){
			for (i = NUM_BOARDS*6-6; i >= 0; i-=6) {
				// Onboard
				hred = frame[i];
				hgreen = frame[i+1];
				hblue = frame[i+2];
				// Slave
				lred = frame[i+3];
				lgreen = frame[i+4];
				lblue = frame[i+5];
				
				b = pwm_interleave[pwm_index];
				
				ln = (lred&bitmask[b]) ? RED_MASK : 0;
				ln |= (lgreen&bitmask[b]) ? GREEN_MASK : 0;
				ln |= (lblue&bitmask[b]) ? BLUE_MASK : 0;
				
				hn = (hred&bitmask[b]) ? RED_MASK : 0;
				hn |= (hgreen&bitmask[b]) ? GREEN_MASK : 0;
				hn |= (hblue&bitmask[b]) ? BLUE_MASK : 0;
				
				b = hn<<4 | ln;
				
				push(b);
			}
			latch_out();
		}
	}
}

