#include <Keyboard.h>

void sendSpecialChar(char c) {
  switch (c) {
    case '"':  // double quote
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write('\'');  // shift + apostrophe
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case '\'':  // single quote
      Keyboard.write('\'');
      break;
    case ':':
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write(';');
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case '?':
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write('/');
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case '!':
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write('1');
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case '(':
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write('9');
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case ')':
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.write('0');
      Keyboard.release(KEY_LEFT_SHIFT);
      break;
    case '\n':
      Keyboard.write(KEY_RETURN);
      break;
    default:
      Keyboard.write(c);
      break;
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial
  }
  Serial.println("Ready for typing input...");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    sendSpecialChar(c);
  }
}