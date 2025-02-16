// ESP32 Server Code (main.cpp)
#include <ESP32Servo.h>
#include <WiFi.h>

// WiFi Configuration
const char *ssid = "ESP32_Servo_Control";
const char *password = "your_password_here";
WiFiServer server(8080);

// Servo Definitions
#define TOTAL_TOYS 2
#define TRIGGERS_PER_TOY 2
#define TOTAL_SERVOS (TOTAL_TOYS * (TRIGGERS_PER_TOY + 1)) // 2 triggers + 1 weave per toy

// Servo pins configuration
const int toy1_trigger1_pin = 18;
const int toy1_trigger2_pin = 12;
const int toy1_weave_pin = 14;
const int toy2_trigger1_pin = 27;
const int toy2_trigger2_pin = 26;
const int toy2_weave_pin = 25;

// Servo objects
Servo servos[TOTAL_SERVOS];
const int servoPins[] = {toy1_trigger1_pin, toy1_trigger2_pin, toy1_weave_pin,
                         toy2_trigger1_pin, toy2_trigger2_pin, toy2_weave_pin};

// Command structure for better organization
struct ServoCommand {
  uint8_t toy_id;     // 0 or 1 for toy1/toy2
  uint8_t servo_type; // 0=trigger1, 1=trigger2, 2=weave
  uint8_t angle;      // 0-180
};

void setup() {
  Serial.begin(921600);

  // Configure Access Point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  // Initialize all servos
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90); // Set to center position
    Serial.printf("Initialized servo %d on pin %d\n", i, servoPins[i]);
  }

  server.begin();
}

int getServoIndex(uint8_t toy_id, uint8_t servo_type) {
  return (toy_id * 3) + servo_type; // 3 servos per toy
}

void handleServoCommand(ServoCommand cmd) {
  if (cmd.toy_id >= TOTAL_TOYS || cmd.servo_type >= 3) {
    Serial.println("Invalid servo command parameters");
    return;
  }

  int servo_index = getServoIndex(cmd.toy_id, cmd.servo_type);
  int angle = constrain(cmd.angle, 0, 180);

  servos[servo_index].writeMicroseconds(map(angle, 0, 180, 500, 2400));

      const char *servo_names[] = {"Trigger1", "Trigger2", "Weave"};
  Serial.printf("Toy%d %s set to angle %d\n", cmd.toy_id + 1,
                servo_names[cmd.servo_type], angle);
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    while (client.connected()) {
      if (client.available() >= 3) {
        uint8_t buffer[3];
        size_t bytesRead = client.read(buffer, 3);

        if (bytesRead == 3) {
          ServoCommand cmd = {
              .toy_id = buffer[0], .servo_type = buffer[1], .angle = buffer[2]};

          handleServoCommand(cmd);
          client.write("OK");
        }
      }
      delay(1);
    }
    client.stop();
    Serial.println("Client disconnected");
  }

  // Also handle serial commands for direct control
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse commands like "toy1_t1:90" or "toy2_w:45"
    int separator = command.indexOf(':');
    if (separator > 0) {
      String prefix = command.substring(0, separator);
      int angle = command.substring(separator + 1).toInt();

      ServoCommand cmd = {0, 0, (uint8_t)angle};

      if (prefix.startsWith("toy1_")) {
        cmd.toy_id = 0;
      } else if (prefix.startsWith("toy2_")) {
        cmd.toy_id = 1;
      } else {
        Serial.println("Invalid toy prefix");
        return;
      }

      if (prefix.endsWith("_t1")) {
        cmd.servo_type = 0;
      } else if (prefix.endsWith("_t2")) {
        cmd.servo_type = 1;
      } else if (prefix.endsWith("_w")) {
        cmd.servo_type = 2;
      } else {
        Serial.println("Invalid servo type");
        return;
      }

      handleServoCommand(cmd);
    }
  }
}