#pragma once
#include "config.h"
#include <ESP32Servo.h>

class ServoManager {
public:
  ServoManager();
  void init();
  bool setServoAngle(uint8_t toy_id, uint8_t servo_type, uint8_t angle);
  static int getServoIndex(uint8_t toy_id, uint8_t servo_type);

private:
  Servo servos[TOTAL_SERVOS];
  const int servoPins[TOTAL_SERVOS] = {
      PinConfig::toy1_trigger1, PinConfig::toy1_trigger2,
      PinConfig::toy1_weave,    PinConfig::toy2_trigger1,
      PinConfig::toy2_trigger2, PinConfig::toy2_weave};
};
