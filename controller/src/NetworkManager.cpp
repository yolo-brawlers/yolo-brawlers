#include "NetworkManager.h"

NetworkManager::NetworkManager(CommandProcessor &cp)
    : server(WIFI_PORT), command_processor(cp) {}

void NetworkManager::init() {
  WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Access Point Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());
  server.begin();
}

void NetworkManager::handleClients() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    while (client.connected()) {
      if (client.available() >= 3) {
        uint8_t buffer[3];
        size_t bytesRead = client.read(buffer, 3);
        if (bytesRead == 3) {
          command_processor.processNetworkCommand(buffer, bytesRead);
          client.write("OK");
        }
      }
      delay(1);
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}