#include "CommandProcessor.h"

CommandProcessor::CommandProcessor(ServoManager &sm) : servo_manager(sm) {}

void CommandProcessor::processSerialCommand(const String &command) {
  int separator = command.indexOf(':');
  if (separator <= 0)
    return;

  String prefix = command.substring(0, separator);
  int angle = command.substring(separator + 1).toInt();
  ServoCommand cmd = {0, 0, (uint8_t)angle};

  if (prefix.startsWith("toy1_")) {
    cmd.toy_id = 0;
  } else if (prefix.startsWith("toy2_")) {
    cmd.toy_id = 1;
  } else {
    Serial.println("Invalid toy prefix");
    return;
  }

  if (prefix.endsWith("_t1")) {
    cmd.servo_type = 0;
  } else if (prefix.endsWith("_t2")) {
    cmd.servo_type = 1;
  } else if (prefix.endsWith("_w")) {
    cmd.servo_type = 2;
  } else {
    Serial.println("Invalid servo type");
    return;
  }

  executeCommand(cmd);
}

void CommandProcessor::processNetworkCommand(uint8_t *buffer, size_t length) {
  if (length != 3)
    return;

  ServoCommand cmd = {
      .toy_id = buffer[0], .servo_type = buffer[1], .angle = buffer[2]};
  executeCommand(cmd);
}

void CommandProcessor::executeCommand(const ServoCommand &cmd) {
  servo_manager.setServoAngle(cmd.toy_id, cmd.servo_type, cmd.angle);
}