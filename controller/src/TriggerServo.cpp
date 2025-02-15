#include "TriggerServo.h"

TriggerServo::TriggerServo(int servoPin) : pin(servoPin), currentAngle(0) {}

void TriggerServo::init() {
  servo.attach(pin);
  servo.write(currentAngle);
}

void TriggerServo::setAngle(int angle) {
  currentAngle = angle;
  servo.write(angle);
}

int TriggerServo::getCurrentAngle() const { return currentAngle; }