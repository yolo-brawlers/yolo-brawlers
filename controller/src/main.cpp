#include "CommandProcessor.h"
#include "NetworkManager.h"
#include "ServoManager.h"
#include <Arduino.h>

ServoManager servo_manager;
CommandProcessor command_processor(servo_manager);
NetworkManager network_manager(command_processor);

void setup() {
  Serial.begin(921600);

  servo_manager.init();
  network_manager.init();
}

void loop() {
  network_manager.handleClients();

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command_processor.processSerialCommand(command);
  }
}