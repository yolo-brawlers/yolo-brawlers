#pragma once
#include "CommandProcessor.h"
#include "config.h"
#include <WiFi.h>

class NetworkManager {
public:
  NetworkManager(CommandProcessor &command_processor);
  void init();
  void handleClients();

private:
  WiFiServer server;
  CommandProcessor &command_processor;
};