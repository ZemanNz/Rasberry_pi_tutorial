#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 16, 17);
  Serial.println("ESP32 UART2 připraven...");
}

void loop() {
  if (Serial2.available()) {
    String msg = Serial2.readStringUntil('\n');
    Serial.print("Dostáno z Pi: ");
    Serial.println(msg);
    Serial2.println("Echo: " + msg);
  }
  delay(100);
  Serial2.println("Ping from ESP32");    
}