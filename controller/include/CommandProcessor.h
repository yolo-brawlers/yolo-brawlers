#pragma once
#include "ServoManager.h"

struct ServoCommand {
  uint8_t toy_id;     // 0 or 1 for toy1/toy2
  uint8_t servo_type; // 0=trigger1, 1=trigger2, 2=weave
  uint8_t angle;      // 0-180
};

class CommandProcessor {
public:
  CommandProcessor(ServoManager &servo_manager);
  void processSerialCommand(const String &command);
  void processNetworkCommand(uint8_t *buffer, size_t length);

private:
  ServoManager &servo_manager;
  void executeCommand(const ServoCommand &cmd);
};