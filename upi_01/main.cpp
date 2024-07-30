#include <WiFi.h>
#include <PubSubClient.h>
#include <SimpleDHT.h>
#include <ArduinoJson.h>
#include <time.h>

// Configurações da rede Wi-Fi
const char* ssid = "";
const char* password = "";

// Configurações do broker MQTT
const char* mqtt_server = "www.maqiatto.com";
const int mqtt_port = 1883;
const char* temp_topic = "UPI1/temperature";
const char* humidity_topic = "UPI1/moisture";

// Credenciais MQTT
const char* mqtt_user = "lucasl050503@gmail.com";  
const char* mqtt_password = "123456"; 

// Configuração do sensor
#define DHT_PIN 21
SimpleDHT11 dht11(DHT_PIN);

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi();
void reconnect();
void readAndPublishSensorData();
String getFormattedTime();

void setup() {
  Serial.begin(115200);
  Serial.println(F("Initializing..."));

  // Conectar ao Wi-Fi
  setup_wifi();

  // Configurar cliente MQTT
  client.setServer(mqtt_server, mqtt_port);

  // Configurar o servidor de tempo NTP
  configTime(0, 0, "pool.ntp.org");
}

void loop() {
  // Conectar ao broker MQTT se não estiver conectado
  if (!client.connected()) {
    reconnect();
  }
  
  // Manter o cliente MQTT ativo
  client.loop();
  
  // Leitura e publicação de dados
  readAndPublishSensorData();
  
  // Lê de 1 em 1 segundo
  delay(1000);
}

void setup_wifi() {
  Serial.print("Connecting to ");
  Serial.print(ssid);

  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi.");
  }
}

void reconnect() {
  // Loop até que esteja conectado
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Tenta conectar
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      
      delay(5000);
    }
  }
}

void readAndPublishSensorData() {
  byte temperature = 0;
  byte humidity = 0;
  int err = dht11.read(&temperature, &humidity, NULL);
  
  if (err != SimpleDHTErrSuccess) {
    Serial.print(F("Read DHT11 failed, err="));
    Serial.println(err);
    return;
  }

  // Obter o timestamp formatado
  String timestamp = getFormattedTime();

  // Publicar temperatura em formato JSON
  StaticJsonDocument<200> tempJson;
  tempJson["timestamp"] = timestamp;
  tempJson["value"] = (int)temperature;
  char tempBuffer[256];
  serializeJson(tempJson, tempBuffer);

  String temperature_topic = String(mqtt_user) + "/UPI1/temperature";
  client.publish(temperature_topic.c_str(), tempBuffer);
  Serial.println(tempBuffer);


  // Publicar umidade em formato JSON
  StaticJsonDocument<200> humidJson;
  humidJson["timestamp"] = timestamp;
  humidJson["value"] = (int)humidity;
  char humidBuffer[256];
  serializeJson(humidJson, humidBuffer);

  String humidity_topic = String(mqtt_user) + "/UPI1/moisture";
  client.publish(humidity_topic.c_str(), humidBuffer);
  Serial.println(humidBuffer);

}

String getFormattedTime() {
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);

  char buffer[30];
  sprintf(buffer, "%04d-%02d-%02dT%02d:%02d:%02d",
          p_tm->tm_year + 1900,
          p_tm->tm_mon + 1,
          p_tm->tm_mday,
          p_tm->tm_hour - 3,
          p_tm->tm_min,
          p_tm->tm_sec);
  return String(buffer);
}