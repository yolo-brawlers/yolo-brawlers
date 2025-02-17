#include "ServoManager.h"

ServoManager::ServoManager() {}

void ServoManager::init() {
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90); // Set to center position
    Serial.printf("Initialized servo %d on pin %d\n", i, servoPins[i]);
  }
}

bool ServoManager::setServoAngle(uint8_t toy_id, uint8_t servo_type,
                                 uint8_t angle) {
  if (toy_id >= TOTAL_TOYS || servo_type >= 3) {
    Serial.println("Invalid servo parameters");
    return false;
  }

  int servo_index = getServoIndex(toy_id, servo_type);
  int constrained_angle = constrain(angle, 0, 180);
  if (servo_index == 2) {
    servos[servo_index].write(constrained_angle);
  } else {
    servos[servo_index].writeMicroseconds(
      map(constrained_angle, 0, 180, 500, 2400));
  }
  
  

  const char *servo_names[] = {"Trigger1", "Trigger2", "Weave"};
  Serial.printf("Toy%d %s set to angle %d\n", toy_id + 1,
                servo_names[servo_type], constrained_angle);
  return true;
}

int ServoManager::getServoIndex(uint8_t toy_id, uint8_t servo_type) {
  return (toy_id * 3) + servo_type;
}