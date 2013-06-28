#include <wiringPi.h>
#include <stdint.h>

#define PIN 1

int blink(int x)
{
	wiringPiSetup();
	pinMode(PIN, OUTPUT);
	int j;
	for(j = 0; j < 10; j++)
	{
		digitalWrite(PIN, HIGH); delayMicrosecondsHard(x);
		digitalWrite(PIN, LOW); delayMicrosecondsHard(x);
	}
	return 0;
}

static inline void write_begin() {
	wiringPiSetup();
	pinMode(PIN, OUTPUT);
	digitalWrite(PIN, HIGH); 
	delayMicrosecondsHard(10);
	digitalWrite(PIN, LOW);
}

static inline void
write_one() {
	digitalWrite(PIN, LOW);
	delayMicrosecondsHard(19);
	digitalWrite(PIN, HIGH); 
	delayMicrosecondsHard(9);
	digitalWrite(PIN, LOW);
}

static inline void
write_zero() {
	digitalWrite(PIN, LOW);
	delayMicrosecondsHard(9);
	digitalWrite(PIN, HIGH); 
	delayMicrosecondsHard(19);
	digitalWrite(PIN, LOW);
}

static inline void
write_end() {
	digitalWrite(PIN, LOW);
	delayMicrosecondsHard(40);
}

int set_color(int led, int intensity, int r, int g, int b) {
	uint16_t color = ((r)+((g)<<4)+((b)<<8));
	int i;
	write_begin();
	for (i=6; i; i--, (led <<= 1)) {
		if (led&(1<<5)) {
			write_one();
		} else {
			write_zero();
		}
	}
	for (i=8; i; i--, (intensity<<=1)) {
		if (intensity&(1<<7)) {
			write_one();
		} else {
			write_zero();
		}
	}
	for (i=12; i; i--, (color<<=1)) {
		if (color&(1<<11)) {
			write_one();
		} else {
			write_zero();
		}
	}
	write_end();
	return 0;
}

int fill_color(int begin, int count, int intensity, int r, int g, int b) {
	while (count--) {
		set_color(begin++, intensity, r, g, b);
	}
	return 0;
}

