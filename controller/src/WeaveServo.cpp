#include "WeaveServo.h"

WeaveServo::WeaveServo(int servoPin) : pin(servoPin), currentAngle(0) {}

void WeaveServo::init() {
  servo.attach(pin);
  servo.write(currentAngle);
}

void WeaveServo::updateAngle(int angle) {
  currentAngle = angle;
  servo.write(angle);
}

int WeaveServo::getCurrentAngle() const { return currentAngle; }