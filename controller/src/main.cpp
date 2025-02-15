#include "Controller.h"
#include <Arduino.h>

// Define pins for servos
const int TRIGGER1_PIN = 18;
const int TRIGGER2_PIN = 10;
const int WEAVER_PIN = 11;

Controller controller(TRIGGER1_PIN, TRIGGER2_PIN, WEAVER_PIN);

void setup() {
  Serial.begin(921600);

  // Wait for serial to connect (important for some boards)
  while (!Serial) {
    delay(100);
  }

  controller.init();
  Serial.println("Controller initialized!");
  Serial.println("Commands:");
  Serial.println("T1:angle - Set Trigger 1 (0-180)");
  Serial.println("T2:angle - Set Trigger 2 (0-180)");
  Serial.println("W:angle  - Set Weaver (0-180)");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any whitespace/newlines

    Serial.print("Received command: ");
    Serial.println(command);

    if (command.startsWith("T1:")) {
      int angle = command.substring(3).toInt();
      Serial.print("Setting Trigger 1 to angle: ");
      Serial.println(angle);
      controller.updateTrigger1(angle);
    } else if (command.startsWith("T2:")) {
      int angle = command.substring(3).toInt();
      Serial.print("Setting Trigger 2 to angle: ");
      Serial.println(angle);
      controller.updateTrigger2(angle);
    } else if (command.startsWith("W:")) {
      int angle = command.substring(2).toInt();
      Serial.print("Setting Weaver to angle: ");
      Serial.println(angle);
      controller.updateWeaver(angle);
    } else {
      Serial.println(
          "Invalid command format! Use T1:, T2:, or W: followed by angle");
    }
  }
}