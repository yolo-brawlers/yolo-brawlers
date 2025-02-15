#include "Controller.h"

Controller::Controller(int trigger1Pin, int trigger2Pin, int weaverPin)
    : trigger1(trigger1Pin), trigger2(trigger2Pin), weaver(weaverPin) {}

void Controller::init() {
  trigger1.init();
  trigger2.init();
  weaver.init();
}

void Controller::updateTrigger1(int angle) { trigger1.setAngle(angle); }

void Controller::updateTrigger2(int angle) { trigger2.setAngle(angle); }

void Controller::updateWeaver(int angle) { weaver.updateAngle(angle); }