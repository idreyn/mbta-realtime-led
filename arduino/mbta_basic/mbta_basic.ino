#include <Adafruit_NeoPixel.h>
#include <math.h>

#define SPEED 10
#define SIZE 88

#define RED 0x660000
#define GREEN 0x006600
#define BLUE 0x000066
#define ORANGE 0xDD2C00

typedef struct Segment {
  Adafruit_NeoPixel *strip;
  unsigned int start;
  unsigned int end;
  uint32_t color;
} Segment;

Adafruit_NeoPixel greenLineD = Adafruit_NeoPixel(76, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineB = Adafruit_NeoPixel(78, 3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineCE_blueLine = Adafruit_NeoPixel(107, 4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel orangeLine = Adafruit_NeoPixel(85, 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel redLine = Adafruit_NeoPixel(146, 6, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel *strips[5] = {
  &greenLineD, &greenLineB, &greenLineCE_blueLine, &orangeLine, &redLine
};

Segment rl_A = {&redLine,0,22,RED};
Segment rl_B = {&redLine,23,65,RED};
Segment rl = {&redLine,66,145,RED};
Segment ol = {&orangeLine,0,84,ORANGE};
Segment gl_B_main = {&greenLineB,0,77,GREEN};
Segment gl_D = {&greenLineD,0,75,GREEN};
Segment gl_C = {&greenLineCE_blueLine,0,30,GREEN};
Segment gl_E = {&greenLineCE_blueLine,31,57,GREEN};
Segment bl = {&greenLineCE_blueLine,58,106,BLUE};

Segment *segments[9] = {
  &rl, &rl_A, &rl_B, &ol, &gl_B_main, &gl_C, &gl_D, &gl_E, &bl
};

void setup() {
  delay(3000);
  for(int i=0;i<5;i++) {
    strips[i]->begin();
    strips[i]->setBrightness(50);
    strips[i]->show();
  }
}

int tick = 0;

void loop() {
  for(int i=0;i<9;i++) {
    int start = segments[i]->start;
    int end = segments[i]->end;
    uint32_t baseColor = segments[i]->color;
    for(int j=start;j<=end;j++) {
      int r = red(baseColor);
      int g = green(baseColor);
      int b = blue(baseColor);
      float brightness = 0.5 + 0.5 * cos((float)(j - tick) / 100.0);
      segments[i]->strip->setPixelColor(j,Color(
        r * brightness,
        g * brightness,
        b * brightness
      ));
    }
    segments[i]->strip->show();
    ++tick;
  }
}

