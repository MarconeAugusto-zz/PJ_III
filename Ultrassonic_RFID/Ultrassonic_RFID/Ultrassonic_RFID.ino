//Integração sesnsor ultrassom e RFID

//Bibliotecas
#include <SPI.h>
#include <MFRC522Extended.h>
#include <MFRC522.h>
#include <Ultrasonic.h>
#include <elapsedMillis.h>
#include <Thread.h>
#include <ThreadController.h>

//Constantes
#define SS_PIN 10
#define RST_PIN 11
#define pino_trigger 49
#define pino_echo 48
MFRC522 mfrc522(SS_PIN, RST_PIN); //Instância MFRC522.
Ultrasonic ultrasonic(pino_trigger, pino_echo);//Instancia Sensor

//Declarando os pinos dos LEDs
int ledVerde = 12, buzzer = 37, tempoEspera = 5000; // 5 segundos.
float distancia = 20.0, dist; // distancia utilizada 20 cm
boolean estado_vaga = false, estado_aut = false;

// ThreadController que controlará todos os threads
ThreadController controll = ThreadController();

//My Thread  (como um ponteiro)
Thread* myThread = new Thread();
//His Thread (not pointer)
//Thread hisThread = Thread();

void iniciaSerial() {
  Serial.begin(57600);   // Inicia a serial
  Serial.println("Iniciando Serial...");
  Serial.println();
  Serial.println("Iniciando Sensor Ultrassonico...");
  Serial.println();
}

void initPIN(){
  pinMode(ledVerde , OUTPUT);
  pinMode(buzzer , OUTPUT);
}

void setup() {
  iniciaSerial();       //Inicia Serial
  mfrc522.PCD_Init();   // Inicia MFRC522
  getDistancia();       //Obtem a distancia inicial
  initPIN();            //Configura os pinos
  SPI.begin();          // Inicia o barramento SPI

  // Configure myThread
  myThread->onRun(getDistancia);
  myThread->setInterval(1000);  //verifica o sensor ultrassonico de 1 em 1 segundo
  //hisThread.onRun(getAutenticacao);
  //hisThread.setInterval(2000);  //verifica o RFID de 2 em 2 segundos

  controll.add(myThread);
  //controle.add(&hisThread);
}

void loop() {
  controll.run();
  digitalWrite(ledVerde , LOW);
  Serial.print("Distancia = ");
  Serial.println(dist);
  while(dist < distancia){
    digitalWrite(ledVerde , HIGH);
    elapsedMillis waiting;
    while(waiting < tempoEspera){
      getAutenticacao();
    }
    if(estado_aut == true){
      Serial.println("Vaga autenticada");
    }else{
      Serial.println("Vaga nao autenticada");
    }
  }
  delay(1000);
  Serial.println("Nenhum veiculo detectado...");
}

void getAutenticacao(){
  estado_vaga = true;
  if ( ! mfrc522.PICC_IsNewCardPresent()){
    return;
  }
  // Selecione um dos cartões
  if ( ! mfrc522.PICC_ReadCardSerial()){
    return;
  }
  //Mostra o UID na serial
  Serial.print("UID da tag :");
  String conteudo= "";
  byte letra;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Mensagem : ");
  conteudo.toUpperCase();
  if (conteudo.substring(1) == "40 1F 63 46"){ //UID 1 - Chaveiro
    Serial.println("Ola Marcone Augusto !");
    Serial.println("Vaga autenticada");
    Serial.println();
    digitalWrite(ledVerde , LOW);
    buzina_aprovado();
    delay(2500);
    digitalWrite(ledVerde , HIGH);
    estado_aut = true;
  }
} 

void buzina_aprovado(){
    int frequencia = 3500;
    tone(buzzer,frequencia,500);
}
void buzina_rejeitado(){
    int frequencia = 300;
    tone(buzzer,frequencia,500);
}

void getDistancia(){
  //Le as informacoes do sensor e converte para centímetros
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  dist = cmMsec;
}
