#pragma once

// WiFi Configuration
extern const char *WIFI_SSID;
extern const char *WIFI_PASSWORD;
extern const int WIFI_PORT;

// Servo Configuration
#define TOTAL_TOYS 2
#define TRIGGERS_PER_TOY 2
#define TOTAL_SERVOS (TOTAL_TOYS * (TRIGGERS_PER_TOY + 1))

// Pin Definitions
struct PinConfig {
  static const int toy1_trigger1 = 18;
  static const int toy1_trigger2 = 19;
  static const int toy1_weave = 22;
  static const int toy2_trigger1 = 27;
  static const int toy2_trigger2 = 26;
  static const int toy2_weave = 25;
};