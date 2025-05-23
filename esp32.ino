#include <ESP32Servo.h>

Servo servo1, servo2, servo3;
String inputString = "";

void setup() {
  Serial.begin(115200);
  servo1.attach(32);   // Replace with your actual pins
  servo2.attach(34);
  servo3.attach(35);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      handleInput(inputString);
      inputString = "";
    } else {
      inputString += c;
    }
  }
}

void handleInput(String data) {
  int angles[3];
  int index = 0;
  for (int i = 0; i < 3; i++) {
    int commaIndex = data.indexOf(',');
    if (commaIndex == -1 && i < 2) return;
    angles[i] = data.substring(0, commaIndex).toInt();
    data = data.substring(commaIndex + 1);
  }

  servo1.write(angles[0]);
  servo2.write(angles[1]);
  servo3.write(angles[2]);

  Serial.println("Angles received and applied.");
}
