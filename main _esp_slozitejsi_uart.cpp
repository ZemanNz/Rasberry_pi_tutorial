#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

// Parametry Wi‑Fi AP
const char* AP_SSID = "ESP32-Server";
const char* AP_PASS = "esp32pass";

// Web server na portu 80
WebServer server(80);

// UART1 piny a rychlost
const int RX1_PIN = 16;
const int TX1_PIN = 17;
const unsigned long BAUD_RATE = 115200;

// Pole pro ukládání přijatých zpráv (maximálně např. 100)
#define MAX_MESSAGES 100
String messages[MAX_MESSAGES];
int messageCount = 0;

// Obsluha hlavní stránky
void handleRoot() {
  String html = "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "<title>ESP32 UART Server</title>"
                "<style>table{border-collapse:collapse;}td,th{border:1px solid #666;padding:4px;}</style>"
                "</head><body>"
                "<h1>ESP32 UART Server</h1>"
                "<p>Tabulka přijatých barev:</p>"
                "<table><tr><th>#</th><th>Barva</th></tr>";
  for (int i = 0; i < messageCount; ++i) {
    html += "<tr><td>" + String(i+1) + "</td><td>" + messages[i] + "</td></tr>";
  }
  html += "</table>"
          "<p>Obnov stránku pro nové hodnoty.</p>"
          "</body></html>";
  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Inicializuj UART1 pro příjem dat z PC
  Serial1.begin(BAUD_RATE, SERIAL_8N1, RX1_PIN, TX1_PIN);
  Serial.println("Serial1 ready.");

  // Spusť Wi‑Fi v režimu AP
  WiFi.softAP(AP_SSID, AP_PASS);
  IPAddress ip = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(ip);

  // Nastaví obsluhu HTTP GET /
  server.on("/", handleRoot);
  server.begin();
  Serial.println("Web server started.");
}

void loop() {
  // Čti data z UART1
  if (Serial1.available()) {
    String msg = Serial1.readStringUntil('\n');
    msg.trim();
    if (msg.length() > 0) {
      // Ulož do pole, přemaž nejstarší, pokud je plno
      if (messageCount < MAX_MESSAGES) {
        messages[messageCount++] = msg;
      } else {
        // posunout všechny o jeden dolů a přidat novou na konec
        for (int i = 1; i < MAX_MESSAGES; ++i) {
          messages[i-1] = messages[i];
        }
        messages[MAX_MESSAGES-1] = msg;
      }
      Serial.print("Received via UART1: ");
      Serial.println(msg);
    }
  }

  // Zpracuj HTTP požadavky
  server.handleClient();
}
