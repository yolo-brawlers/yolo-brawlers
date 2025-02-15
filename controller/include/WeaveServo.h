#ifndef WEAVE_SERVO_H
#define WEAVE_SERVO_H

#include <ESP32Servo.h>

class WeaveServo {
private:
  Servo servo;
  int pin;
  int currentAngle;

public:
  WeaveServo(int servoPin);
  void init();
  void updateAngle(int angle);
  int getCurrentAngle() const;
};

#endif