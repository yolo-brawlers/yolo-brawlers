// // server.cpp
// #include <WiFi.h>
// #include <ESP32Servo.h>

// #define MAX_SERVOS 4

// const char* ssid = "ESP32_GPIO_Control";
// const char* password = "your_password_here";

// WiFiServer server(8080);
// Servo servos[4];  // Array to hold up to 4 servo objects

// // GPIO pins for servos
// const int servoPins[] = {18, 12, 14, 27};  // Adjust pins as needed
// // const int MAX_SERVOS = 4;

// void setup() {
//     Serial.begin(921600);
    
//     // Configure Access Point
//     WiFi.softAP(ssid, password);
//     Serial.println("Access Point Started");
//     Serial.print("IP Address: ");
//     Serial.println(WiFi.softAPIP());
    
//     // Initialize servos
//     for (int i = 0; i < MAX_SERVOS; i++) {
//         servos[i].attach(servoPins[i]);
//         servos[i].write(90);  // Set to center position
//     }
    
//     server.begin();
// }

// void loop() {
//   WiFiClient client = server.available();

//   if (client) {
//     Serial.println("New client connected");

//     while (client.connected()) {
//       if (client.available() >= 3) { // Changed to 3 bytes minimum
//         uint8_t buffer[3];
//         size_t bytesRead = client.read(buffer, 3);

//         if (bytesRead == 3) {      // Ensure we read all 3 bytes
//           if (buffer[0] == 0xFF) { // Servo control command
//             if (buffer[1] < MAX_SERVOS) {
//               int angle = constrain(buffer[2], 0, 180);
//               servos[buffer[1]].write(angle);
//               Serial.printf("Setting servo %d to angle %d\n", buffer[1], angle);
//               // Send acknowledgment
//               client.write("OK");
//             }
//           } else { // GPIO control command
//             pinMode(buffer[0], OUTPUT);
//             digitalWrite(buffer[0], buffer[1]);
//             Serial.printf("Setting GPIO %d to %d\n", buffer[0], buffer[1]);
//             // Send acknowledgment
//             client.write("OK");
//           }
//         }
//       }
//       delay(1); // Give other tasks a chance to run
//     }

//     client.stop();
//     Serial.println("Client disconnected");
//   }
// }