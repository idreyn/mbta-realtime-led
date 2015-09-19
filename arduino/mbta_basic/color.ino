uint8_t red(uint32_t color) {
  return 0xFF & (color >> 16);
}

uint8_t green(uint32_t color) {
  return 0xFF & (color >> 8);
}

uint8_t blue(uint32_t color) {
  return 0xFF & color;
}

uint32_t Color(uint8_t r, uint8_t g, uint8_t b) {
  return ((uint32_t)r << 16) | ((uint32_t)g <<  8) | b;
}
