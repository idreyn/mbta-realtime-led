#include <Adafruit_NeoPixel.h>

#define PACKET_SIZE 8

byte packet[PACKET_SIZE];
int packet_index = 0;
int total_bytes = 0;
boolean is_running = 1;

unsigned long last_data;

Adafruit_NeoPixel greenLineD = Adafruit_NeoPixel(76, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineB = Adafruit_NeoPixel(78, 3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel greenLineCE_blueLine = Adafruit_NeoPixel(107, 4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel orangeLine = Adafruit_NeoPixel(85, 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel redLine = Adafruit_NeoPixel(146, 6, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel *strips[5] = {
  &greenLineD, &greenLineB, &greenLineCE_blueLine, &orangeLine, &redLine
};

void setup() {
  pinMode(13,OUTPUT);
  Serial.begin(115200);
  for(int i=0;i<5;i++) {
    strips[i]->begin();
    strips[i]->setPixelColor(0,0x664400);
    strips[i]->show();
  }
}

void loop() {
  if(millis() - last_data > 2000) {
    packet_index = 0;
  }
  while(Serial.available()) {
    byte b = Serial.read();
    last_data = millis();
    if(b == 0xFF && packet_index == 0) {
      // Special byte to tell lights to actually update
      greenLineD.show();
      greenLineB.show();
      greenLineCE_blueLine.show();
      orangeLine.show();
      redLine.show();
    } else {
      // Just doing normal stuff
      packet[packet_index] = b;
      packet_index++;
      total_bytes++;
      if(packet_index == PACKET_SIZE) {
        handle_packet(packet);
        // I can't believe I ate the whole thing
        packet_index = 0;
      }
    }
  }
}

void handle_packet(byte *packet) {
  int index = packet[0];
  int16_t start = (int16_t) packet[1] << 8 | (int16_t) packet[2];
  int16_t end = (int16_t) packet[3] << 8 | (int16_t) packet[4];
  int32_t color = (int32_t) packet[5] << 16 | (int32_t) packet[6] << 8 | (int32_t) packet[7];
  for(int16_t j=start;j<=end;j++) {
    strips[index]->setPixelColor(j,color);
  }
}

