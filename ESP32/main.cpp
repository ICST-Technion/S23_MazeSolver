

#include <WiFi.h>
#include <Arduino.h>


const char* ssid = "sagiv";
const char* password = "";

WiFiServer server(8080);

void setup() {
  Serial.begin(9600);
  
  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  // Start the server
  server.begin();

  Serial.println("Server started");

}

void loop() {

  // Wait for a client to connect
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected");

    // Read the data into a byte array
    const int bufferSize = 256;  // Maximum buffer size
    uint8_t buffer[bufferSize];
    int bytesRead = client.readBytes(buffer, bufferSize);

    // Do something with the byte array
    // ...

    // Send the response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("");
    client.println("<html><body><h1>Hello, World!</h1></body></html>");

    // Close the connection
    client.stop();
    Serial.println("Client disconnected");
  }
}
