// GE Christmas light control for Arduino  
 // Ported by Scott Harris <scottrharris@gmail.com>  
 // scottrharris.blogspot.com  
   
   
 // Based on this code:  
   
 /*!     Christmas Light Control  
 **     By Robert Quattlebaum <darco@deepdarc.com>  
 **     Released November 27th, 2010  
 **  
 **     For more information,  
 **     see <http://www.deepdarc.com/2010/11/27/hacking-christmas-lights/>.
 **  
 **     Originally intended for the ATTiny13, but should  
 **     be easily portable to other microcontrollers.  
 */  
#define F_CPU 16000000
#include "delay_x.h"

#define MYUBRR 3			// 230.4k baudrate, F_CPU = 16MHz
   
 #define xmas_color_t uint16_t // typedefs can cause trouble in the Arduino environment  
   

   
 #define XMAS_LIGHT_COUNT          50
 #define XMAS_CHANNEL_MAX          (0xF)  
 #define XMAS_DEFAULT_INTENSITY     (0xCC)  
 #define XMAS_HUE_MAX               ((XMAS_CHANNEL_MAX+1)*6-1)  
 #define XMAS_COLOR(r,g,b)     ((r)+((g)<<4)+((b)<<8))  
 #define XMAS_COLOR_WHITE     XMAS_COLOR(XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX)  
 #define XMAS_COLOR_BLACK     XMAS_COLOR(0,0,0)  
 #define XMAS_COLOR_RED          XMAS_COLOR(XMAS_CHANNEL_MAX,0,0)  
 #define XMAS_COLOR_GREEN     XMAS_COLOR(0,XMAS_CHANNEL_MAX,0)  
 #define XMAS_COLOR_BLUE          XMAS_COLOR(0,0,XMAS_CHANNEL_MAX)  
 #define XMAS_COLOR_CYAN          XMAS_COLOR(0,XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX)  
 #define XMAS_COLOR_MAGENTA     XMAS_COLOR(XMAS_CHANNEL_MAX,0,XMAS_CHANNEL_MAX)  
 #define XMAS_COLOR_YELLOW     XMAS_COLOR(XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX,0)  
   
#define sbi(x,y)	x|=(1<<y)
#define cbi(x,y)	x&=~(1<<y)

#define XMAS_PIN	4
#define XMAS_PORT	PORTD
#define XMAS_DDR	DDRD

#define FRAME_SIZE 32

#define DIAL_PIN A0
int dial_value = 0;
int brightness = 0;
// 
static void
xmas_begin() {
	sbi(XMAS_DDR,XMAS_PIN);
	sbi(XMAS_PORT,XMAS_PIN);
	_delay_us(10);
	cbi(XMAS_PORT,XMAS_PIN);
}

static inline void
xmas_one() {
	cbi(XMAS_PORT,XMAS_PIN);
	_delay_us(20);
	sbi(XMAS_PORT,XMAS_PIN);
	_delay_us(10);
	cbi(XMAS_PORT,XMAS_PIN);
}

static inline void
xmas_zero() {
	cbi(XMAS_PORT,XMAS_PIN);
	_delay_us(9);
	sbi(XMAS_PORT,XMAS_PIN);
	_delay_us(20);
	cbi(XMAS_PORT,XMAS_PIN);
}

static inline void
xmas_end() {
	cbi(XMAS_PORT,XMAS_PIN);
	_delay_us(40);
}
   
   
 // The rest of Robert's code is basically unchanged  
   
 void xmas_fill_color(uint8_t begin, uint8_t count, uint8_t intensity, xmas_color_t color)  
 {  
      while(count--)  
      {  
           xmas_set_color(begin++,intensity,color);  
      }  
 }  
   
 void xmas_fill_color_same(uint8_t begin,uint8_t count,uint8_t intensity,xmas_color_t color)  
 {  
      while(count--)  
      {  
           xmas_set_color(0,intensity,color);  
      }  
 }  
   
   
 void xmas_set_color(uint8_t led,uint8_t intensity,xmas_color_t color) {  
      uint8_t i;  
      xmas_begin();  
      for(i=6;i;i--,(led<<=1))  
           if(led&(1<<5))  
                xmas_one();  
           else  
                xmas_zero();  
      for(i=8;i;i--,(intensity<<=1))  
           if(intensity&(1<<7))  
                xmas_one();  
           else  
                xmas_zero();  
      for(i=12;i;i--,(color<<=1))  
           if(color&(1<<11))  
                xmas_one();  
           else  
                xmas_zero();  
      xmas_end();  
 }  
   
   
 xmas_color_t  
 xmas_color(uint8_t r,uint8_t g,uint8_t b) {  
      return XMAS_COLOR(r,g,b);  
 }  
   
 xmas_color_t  
 xmas_color_hue(uint8_t h) {  
      switch(h>>4) {  
           case 0:     h-=0; return xmas_color(h,XMAS_CHANNEL_MAX,0);  
           case 1:     h-=16; return xmas_color(XMAS_CHANNEL_MAX,(XMAS_CHANNEL_MAX-h),0);  
           case 2:     h-=32; return xmas_color(XMAS_CHANNEL_MAX,0,h);  
           case 3:     h-=48; return xmas_color((XMAS_CHANNEL_MAX-h),0,XMAS_CHANNEL_MAX);  
           case 4:     h-=64; return xmas_color(0,h,XMAS_CHANNEL_MAX);  
           case 5:     h-=80; return xmas_color(0,XMAS_CHANNEL_MAX,(XMAS_CHANNEL_MAX-h));  
      }  
 }  

uint8_t color_index = 0;

uint8_t current_frame[FRAME_SIZE];
// uint8_t bytes_since_ack = 0;

void handle_char(uint8_t c) {
  uint8_t i;
  // bytes_since_ack++;
  current_frame[color_index] = c;
  color_index++;
	brightness = XMAS_DEFAULT_INTENSITY;
  if (color_index >= FRAME_SIZE) {
    for(i=0; i < int(FRAME_SIZE / 4); i++) {
    	xmas_set_color(current_frame[i*4], brightness,
  								xmas_color(current_frame[i*4 + 1]>>4, 
  								current_frame[i*4 + 2]>>4, current_frame[i*4 + 3]>>4));
    }
          color_index = 0;
    for(i=0; i<FRAME_SIZE; i++) {
      Serial.write(current_frame[i]);
    }
  }
  // if (bytes_since_ack >= 4) {
  //   bytes_since_ack = 0;
  //   uint8_t i;
  // }
}
   

void setup()  
{  
    xmas_fill_color(0,XMAS_LIGHT_COUNT,XMAS_DEFAULT_INTENSITY,XMAS_COLOR_BLACK); //Enumerate all the lights
    Serial.begin(115200);
    // Serial.begin(9600);
    uint8_t i;
    uint8_t j;
    brightness = XMAS_DEFAULT_INTENSITY;
		for(i = 0; i < XMAS_LIGHT_COUNT; i++) {
			xmas_set_color(i, brightness, xmas_color(int(i*15/50), 0, 15-int(i*15/50)));
		}
}  
 
   
void loop()  
{  
    if (Serial.available() > 0) {
        handle_char(Serial.read());
    }
}   

