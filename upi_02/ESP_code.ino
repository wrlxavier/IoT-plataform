#include <SoftwareSerial.h>
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <TimeLib.h> // Biblioteca para manipular o tempo, instale em Library Manager
#include <ArduinoJson.h>

#include <WiFiUdp.h>
#include <NTPClient.h>

// Define o fuso horário (ex: -3 para horário de Brasília)
const long utcOffsetInSeconds = -3 * 3600;

// Cria uma instância de WiFiUDP para NTP
WiFiUDP ntpUDP;
// Cria uma instância de NTPClient para obter a hora
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);


// Variável para armazenar o tempo da última execução
unsigned long previousMillis = 0;

// Intervalo desejado (em milissegundos)
const long interval = 1000;

//WiFi
// const char* SSID = "Redmi Note 8 Pro";                // SSID / nome da rede WiFi que deseja se conectar
// const char* PASSWORD = "naotemsenha";   // Senha da rede WiFi que deseja se conectar
const char* SSID = "lp2g_wifi";                // SSID / nome da rede WiFi que deseja se conectar
const char* PASSWORD = "Lpp2g#23!lab";   // Senha da rede WiFi que deseja se conectar
// const char* SSID = "DELT_1101";                // SSID / nome da rede WiFi que deseja se conectar
// const char* PASSWORD = "Delt_1101";   // Senha da rede WiFi que deseja se conectar
WiFiClient wifiClient;                        
 
//MQTT Server
const char* mqtt_user = "lucasl050503@gmail.com";
const char* mqtt_password = "123456";
const char* BROKER_MQTT = "maqiatto.com";    //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 1883;                      // Porta do Broker MQTT

#define ID_MQTT  "UPI0ch4"            //Informe um ID unico e seu. Caso sejam usados IDs repetidos a ultima conexão irá sobrepor a anterior. 
#define TOPIC_PUBLISH_1 "lucasl050503@gmail.com/UPI2/moisture"    //Informe um Tópico único. Caso sejam usados tópicos em duplicidade, o último irá eliminar o anterior.
#define TOPIC_PUBLISH_2 "lucasl050503@gmail.com/UPI2/temperature"

PubSubClient MQTT(wifiClient);        // Instancia o Cliente MQTT passando o objeto espClient

//Declaração das Funções
void mantemConexoes();  //Garante que as conexoes com WiFi e MQTT Broker se mantenham ativas
void conectaWiFi();     //Faz conexão com WiFi
void conectaMQTT();     //Faz conexão com Broker MQTT
void enviaValores();
String createJsonString(float value);


// Pinos para a comunicação serial
const int rxPin = D1; // Pino RX da NodeMCU (GPIO5)
const int txPin = D0; // Pino TX da NodeMCU (GPIO4)

float umidade = 0;
float temperatura = 0;

// Inicializa a comunicação serial via SoftwareSerial
SoftwareSerial arduinoSerial(rxPin, txPin);

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);

  // Inicializa a comunicação serial com o Arduino
  arduinoSerial.begin(9600);

  // Inicializa a comunicação serial para debug
  Serial.begin(9600);

  Serial.println("Inicializando0...");

  setTime(1, 24, 34, 29, 7, 2024); // Hora, Minuto, Segundo, Dia, Mês, Ano

  conectaWiFi();

  // Inicializa o NTPClient
  timeClient.begin();

  // Atualiza a hora pela primeira vez
  timeClient.update();

  MQTT.setServer(BROKER_MQTT, BROKER_PORT);   
}

void loop() {

  if (arduinoSerial.available()) {
    String data = arduinoSerial.readStringUntil('\n');
    data.trim(); // Remove any extra newline or space characters
    int commaIndex = data.indexOf(',');

    if (commaIndex > 0) {
      String umidadeStr = data.substring(0, commaIndex);
      String temperaturaStr = data.substring(commaIndex + 1);

      umidade = umidadeStr.toFloat();
      temperatura = temperaturaStr.toFloat();

      Serial.print("Umidade: ");
      Serial.println(createJsonString(umidade));
      Serial.print("Temperatura: ");
      Serial.println(createJsonString(temperatura));
    }
  }

  unsigned long currentMillis = millis();
  // Verifica se passou o intervalo desejado desde a última execução
  if (currentMillis - previousMillis >= interval) {
    // Atualiza o tempo da última execução
    previousMillis = currentMillis;

    // Chama a função desejada
    Serial.print("Publicando dados :");
    Serial.println(timeClient.getFormattedTime());
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    enviaValores();
  }
  mantemConexoes();
  MQTT.loop();
}

void mantemConexoes() {
    if (!MQTT.connected()) {
       conectaMQTT(); 
    }
    
    conectaWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}

void conectaWiFi() {

  if (WiFi.status() == WL_CONNECTED) {
     return;
  }
        
  Serial.print("Conectando-se na rede: ");
  Serial.print(SSID);
  Serial.println("  Aguarde!");

  WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI  
  while (WiFi.status() != WL_CONNECTED) {
      delay(100);
      Serial.print(".");
  }
  
  Serial.println();
  Serial.print("Conectado com sucesso, na rede: ");
  Serial.print(SSID);  
  Serial.print("  IP obtido: ");
  Serial.println(WiFi.localIP()); 
}

void conectaMQTT() { 
    while (!MQTT.connected()) {
        Serial.print("Conectando ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT, mqtt_user, mqtt_password)) {
            Serial.println("Conectado ao Broker com sucesso!");
        } 
        else {
            Serial.println("Noo foi possivel se conectar ao broker.");
            Serial.println("Nova tentatica de conexao em 10s");
            delay(10000);
        }
    }
}

void enviaValores() {
  MQTT.publish(TOPIC_PUBLISH_1, createJsonString(umidade).c_str());
  MQTT.publish(TOPIC_PUBLISH_2, createJsonString(temperatura).c_str());
}

String createJsonString(float value) {
  DynamicJsonDocument doc(1024);

  unsigned long epochTime = timeClient.getEpochTime();
  // Converte epoch time para struct tm
  struct tm *ptm = gmtime((time_t *)&epochTime);

  char timestamp[25];
  snprintf(timestamp, sizeof(timestamp), "%04d-%02d-%02dT%02d:%02d:%02d",
           ptm->tm_year + 1900, ptm->tm_mon + 1, ptm->tm_mday,
           ptm->tm_hour, ptm->tm_min, ptm->tm_sec);

  doc["timestamp"] = timestamp;

  // Adiciona o valor
  doc["value"] = value;

  // Converte o JSON document em string
  String jsonString;
  serializeJson(doc, jsonString);

  return jsonString;
}

