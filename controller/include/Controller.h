#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "TriggerServo.h"
#include "WeaveServo.h"

class Controller {
private:
  TriggerServo trigger1;
  TriggerServo trigger2;
  WeaveServo weaver;

public:
  Controller(int trigger1Pin, int trigger2Pin, int weaverPin);
  void init();
  void updateTrigger1(int angle);
  void updateTrigger2(int angle);
  void updateWeaver(int angle);
};

#endif