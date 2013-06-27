#include <wiringPi.h>

int blink(int x)
{
	wiringPiSetup();
	pinMode(1, OUTPUT);
	int j;
	for(j = 0; j < 10; j++)
	{
		digitalWrite(1, HIGH); delayMicrosecondsHard(x);
		digitalWrite(1, LOW); delayMicrosecondsHard(x);
	}
	return 0;
}
