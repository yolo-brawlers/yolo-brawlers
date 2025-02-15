#ifndef TRIGGER_SERVO_H
#define TRIGGER_SERVO_H

#include <ESP32Servo.h>

class TriggerServo {
private:
  Servo servo;
  int pin;
  int currentAngle;

public:
  TriggerServo(int servoPin);
  void init();
  void setAngle(int angle);
  int getCurrentAngle() const;
};

#endif