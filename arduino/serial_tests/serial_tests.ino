#include <Adafruit_NeoPixel.h>

#define PACKET_SIZE 8

byte packet[8];
int packet_index = 0;

Adafruit_NeoPixel greenLineD = Adafruit_NeoPixel(76, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineB = Adafruit_NeoPixel(78, 3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineCE_blueLine = Adafruit_NeoPixel(107, 4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel orangeLine = Adafruit_NeoPixel(85, 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel redLine = Adafruit_NeoPixel(146, 6, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel *strips[5] = {
  &greenLineD, &greenLineB, &greenLineCE_blueLine, &orangeLine, &redLine
};

void setup() {
  Serial.begin(9600);
  delay(2000);
  for(int i=0;i<5;i++) {
    strips[i]->begin();
    strips[i]->setBrightness(50);
    strips[i]->show();
  }
}

void loop() {
  while(Serial.available()) {
    byte b = Serial.read();
    if(b == 0xFF && packet_index == 0) {
      // Special byte to tell lights to actually update
      Serial.write(0xFF);
      do_work();
    } else {
      // Just doing normal stuff
      packet[packet_index] = b;
      packet_index++;
      if(packet_index == PACKET_SIZE) {
        // That's a whole packet
        packet_index = 0;
        for(int i=0;i<PACKET_SIZE;i++) {
          Serial.write(packet[i]);
        }
      }
    }
  }
}

void do_work() {
  delay(100);
}

