/* Name: main.c
 * Author: <insert your name here>
 * Copyright: <insert your copyright message here>
 * License: <insert your license reference here>
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>

#define NUM_BOARDS 50

//#define FOSC 11059200	// Clock Speed 
#define FOSC 16000000
//#define BAUD 9600		//230400
//#define MYUBRR (FOSC/(16*BAUD))-1		// Not valid in 2x serial mode 
#define MYUBRR 8
// Now 115.2k baud, was 5 for 230.4k baud, see page 198 of the datasheet

#define PWM_LEN 32

uint8_t pwm_interleave[PWM_LEN] = {212, 84, 228, 44, 204, 148, 244, 156, 12, 108, 124, 220, 68, 76, 164, 236, 100, 180, 196, 188, 140, 116, 28, 52, 36, 60, 132, 252, 20, 4, 172, 92};

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
}

void USART_Transmit(uint8_t data) {
	while (!( UCSR0A & (1<<UDRE0))) {}
	UDR0 = data;
}

uint8_t USART_Receive() {
	while (!(UCSR0A & (1<<RXC0))) {}
	return UDR0;
}

inline void push_one() {
    asm volatile("sbi 0x05, 0 \n sbi 0x05, 2 \n cbi 0x05, 2 \n cbi 0x05, 0");
}

inline void push_zero() {
    asm volatile("sbi 0x05, 2 \n cbi 0x05, 2");
}

inline void  __attribute__((flatten)) pushb(uint8_t b) {
    if (b) {
        push_one();
    } else {
        push_zero();
    }
}

inline void clock() {
    asm volatile("sbi 0x05, 2 \n cbi 0x05, 2");
}

inline void  __attribute__((flatten)) pushpix(uint8_t b1, uint8_t b2, uint8_t b3) {
    int p;
    p = (b1 << 2) | (b2 << 1) | b3;
    
    switch(p) {
        case 7:
        asm volatile("sbi 0x05, 0");
        clock();
        clock();
        clock();
        clock();
        asm volatile("cbi 0x05, 0");
        break;
        
        case 6:
        asm volatile("sbi 0x05, 0");
        clock();
        clock();
        asm volatile("cbi 0x05, 0");
        clock();
        clock();
        break;
        
        case 5:
        asm volatile("sbi 0x05, 0");
        clock();
        asm volatile("cbi 0x05, 0");
        clock();
        asm volatile("sbi 0x05, 0");
        clock();
        clock();
        asm volatile("cbi 0x05, 0");
        break;
        
        case 4:
        asm volatile("sbi 0x05, 0");
        clock();
        asm volatile("cbi 0x05, 0");
        clock();
        clock();
        clock();
        break;
        
        case 3:
        clock();
        asm volatile("sbi 0x05, 0");
        clock();
        clock();
        clock();
        asm volatile("cbi 0x05, 0");
        break;
        
        case 2:
        clock();
        asm volatile("sbi 0x05, 0");
        clock();
        asm volatile("cbi 0x05, 0");
        clock();
        clock();
        break;
        
        case 1:
        clock();
        clock();
        asm volatile("sbi 0x05, 0");
        clock();
        clock();
        asm volatile("cbi 0x05, 0");
        break;
        
        case 0:
        clock();
        clock();
        clock();
        clock();
        break;
        
    }
    
    /*if (b1) {
        if (b2) {
            if (b3) {
                asm volatile("sbi 0x05, 0");
                clock();
                clock();
                clock();
                clock();
                asm volatile("cbi 0x05, 0");
            } else {
                asm volatile("sbi 0x05, 0");
                clock();
                clock();
                asm volatile("cbi 0x05, 0");
                clock();
                clock();
            }
        } else {
            if (b3) {
                asm volatile("sbi 0x05, 0");
                clock();
                asm volatile("cbi 0x05, 0");
                clock();
                asm volatile("sbi 0x05, 0");
                clock();
                clock();
                asm volatile("cbi 0x05, 0");
           } else {
                asm volatile("sbi 0x05, 0");
                clock();
                asm volatile("cbi 0x05, 0");
                clock();
                clock();
                clock();
           }
       }
    } else {
        if (b2) {
            if (b3) {
                clock();
                asm volatile("sbi 0x05, 0");
                clock();
                clock();
                clock();
                asm volatile("cbi 0x05, 0");  
            } else {
                clock();
                asm volatile("sbi 0x05, 0");
                clock();
                asm volatile("cbi 0x05, 0");
                clock();
                clock();
            }
        } else {
            if (b3) {
                clock();
                clock();
                asm volatile("sbi 0x05, 0");
                clock();
                clock();
                asm volatile("cbi 0x05, 0");
            } else {
                clock();
                clock();
                clock();
                clock();
            }
        }
    }*/
}

inline void push(uint8_t c) {
	uint8_t i;
    uint8_t v;
	for (i = 0; i<8; i++) {
		v = (c>>i)&1;
		if (v) {
            push_one();
        } else {
            push_zero();
        }
	}
}

inline void latch_out() {
    asm volatile("sbi 0x05, 1 \n cbi 0x05, 1");
}

ISR(USART_RX_vect) {	//USART_RX for atmega48
	uint8_t c;
	c = UDR0;
	//USART_Transmit(c);
	if (c == 'B') {
		frame_addr = 0;
	} else {
		frame[frame_addr++] = c;
	}
}

int main(void) {
	register int16_t i, j;
	register uint8_t pwm_index;
	
	register uint8_t lred, lgreen, lblue;
	register uint8_t hred, hgreen, hblue;
	
	register uint8_t b;
	
	DDRB = 0x07;			//output on B0, latch on B1, clock on B2
	PORTB = 0x00;
	
	USART_Init(MYUBRR);
	
	uint8_t selftest[4] = {0xCC, 0x22, 0x11, 0x00};	// R, G, B, off
	
    j = 0;
    while (!(UCSR0A & (1<<RXC0))) {
		for (i = 0; i < NUM_BOARDS; i++) {
			push(selftest[j % 4]);
		}
		latch_out();
		_delay_ms(700);
        j = (j+1) % 4;
	}

    // Don't enable serial interrupt until here;
    // we want to keep doing the self-test until we get data,
    // but don't want to clutter the interrupt handler.
    
    // This has the annoying side-effect that we usually drop most of 
    // the first frame sent (because we're stuck in _delay_ms), but oh well.
	
	sei();			// Enable interrupts
	
	pwm_index = 0;
	
	for (;;) {
		pwm_index += 1;
		pwm_index %= PWM_LEN;
		
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
            
            //pushpix(lblue > b, lgreen > b, lred > b);
            pushb(lblue > b);
            pushb(lgreen > b);
            pushb(lred > b);
            pushb(lred > b);
            
            //pushpix(hblue > b, hgreen > b, hred > b);
            pushb(hblue > b);
            pushb(hgreen > b);
            pushb(hred > b);
            pushb(hred > b);
        }
		
		latch_out();
	}
	
	return 0;
}

