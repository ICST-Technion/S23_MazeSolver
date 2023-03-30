

#include <WiFi.h>

// Wifi info
const char* ssid = "GIVE_ME_PI";
const char* password = "";
const uint16_t port = 8888;
const char * host = "10.42.0.1"; // raspberry pi ip 
int connectionTimeOut = 10000; // 10 ms
WiFiClient client;
bool connectedToServer = false;

#define BUFFER_SIZE = 100;
#define WIFI_CONNECTION_ERROR -1


int connectToWiFi(const char* ssid, const char* password){
  int loopCounter = 0;
  int maxLoops = 10;
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(1000);
    loopCounter++;
    if (loopCounter > maxLoops){
      return WIFI_CONNECTION_ERROR;
    }
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
  return 0;
}

void setup() {


  Serial.begin(9600);
  Serial.println("hey...");
  // Connect to Wi-Fi network
  WiFi.mode(WIFI_STA);
  if (connectToWiFi(ssid,password) == WIFI_CONNECTION_ERROR){
      Serial.println("connection error occurred...");
      exit(0);
  };

}

void loop() {
  // check WiFi connection
  if (WiFi.status() != WL_CONNECTED){
    Serial.println("Lost connection to Wi-Fi network, reconnecting...");
    while (connectToWiFi(ssid,password) == WIFI_CONNECTION_ERROR) {};
    // if reconneting to Wifi, we need to connect the server again.
    connectedToServer = false;
  }

  if (connectedToServer == false){
    // create a connection with the server.
    if (!client.connect(host, port,connectionTimeOut)) {
        return;
    }
    connectedToServer = true;
  }

  client.print("HI!!! THIS IS THE ESP32\r");

  //wait for the server's reply to become available
  while (!client.available()){}

  uint8_t rxBuffer[100];
  if (client.available() > 0){
    Serial.println("server is available");
    //read back one line from the server
    int bytesReceived = client.read(rxBuffer,100);
    for (int i = 0; i < bytesReceived; i++){
      Serial.print(rxBuffer[i]);
      Serial.print(" ");

    }
  }

}
