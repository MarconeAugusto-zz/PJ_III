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
String IdVaga = "VG01";   //exemplo 
int ledVerde = 12, buzzer = 9, tempoEspera = 10000; // 5 segundos.
float distancia = 20.0, dist; // distancia utilizada 20 cm

//estados
boolean estado_vaga = false, estado_aut = false;

//Acho melhor colocar os estados como int
//estado 1 = vaga livre
//estado 2 = vaga ocupada e autenticada
//estado 3 = vaga ocupada e nao autenticada


// ThreadController que controlará todos os threads
ThreadController controll = ThreadController();
ThreadController controll2 = ThreadController();

//My Thread  (como um ponteiro)
Thread* myThread = new Thread();
//His Thread (not pointer)
Thread hisThread = Thread();

void iniciaSerial() {
  Serial.begin(9600);   // Inicia a serial
  Serial.println();
  Serial.println("Iniciando Serial...");
  Serial.println();
}

void initPIN() {
  pinMode(ledVerde , OUTPUT);
  pinMode(buzzer , OUTPUT);
}

void setup() {
  iniciaSerial();       //Inicia Serial
  getDistancia();       //Obtem a distancia inicial
  initPIN();            //Configura os pinos
  Serial.println("Iniciando Sensor Ultrassonico...");
  Serial.println();
  SPI.begin();          // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
  // Configure myThread
  myThread->onRun(getDistancia);
  myThread->setInterval(1000);  //verifica o sensor ultrassonico de 1 em 1 segundo
  hisThread.onRun(getAutenticacao);
  hisThread.setInterval(1000);  //verifica o RFID de 2 em 2 segundos
  // add as Threads ao controle
  controll.add(myThread);
  controll2.add(&hisThread);
  
  digitalWrite(ledVerde , LOW); // identificaçao visual para sensor ultrassonico
}

void loop() {
  controll.run(); //metodo verifica distancia
  Serial.print("Distancia = ");
  Serial.print(dist);
  Serial.println(" cm");
  
  //////////////////////// mudança no estado da vaga, solicitar autenticação da vaga
  //////////////////////////////////////////////////////////////////////////////////
  if (dist < distancia and estado_aut == false) {
    digitalWrite(ledVerde , HIGH);  // identificaçao visual para sensor ultrassonico
    elapsedMillis waiting;
    while (waiting < tempoEspera) {
      getAutenticacao(); // tempo para autenticar a vaga
    }
    if (estado_aut == true) {
      Serial.println();
      Serial.print("Vaga: ");
      Serial.print(IdVaga);
      Serial.println(", Autenticada");
      Serial.println();
      estado_vaga = true;
      // Chamar metodo para enviar mensagem via Sigfox
    } else {
      Serial.println();
      Serial.print("Vaga: ");
      Serial.print(IdVaga);
      Serial.println(", nao Autenticada");
      Serial.println();
      // Chamar metodo para enviar mensagem via Sigfox
    }
  }
  Serial.println("Passou o primeiro IF");
  if (dist > distancia and estado_vaga == true){
    estado_vaga == false;
    digitalWrite(ledVerde , LOW); // identificaçao visual para sensor ultrassonico    
  }
  
  //////////////////////////////// sem mudança no estado da vaga, houve autenticação
  //////////////////////////////////////////////////////////////////////////////////
  if(estado_vaga == true){  // sem mudança no estado da vaga, autenticação da vaga
    // usuario vai autenticar a retirada do veiculo
    //digitalWrite(ledVerde , HIGH);  // identificaçao visual para sensor ultrassonico
    controll2.run(); //leitor RFID
  }
  
  //////////////////////////////////////////////////// sem veiculo, sem autenticação
  //////////////////////////////////////////////////////////////////////////////////
  if(estado_vaga == false and estado_aut == false){

    Serial.println("Nenhum veiculo detectado...");
  }
  delay(1000);  
}

void getDistancia() { // myThread
  //Serial.println("Verifica distancia"); // debug
  //Le as informacoes do sensor e converte para centímetros
  float cmMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  dist = cmMsec;
}

void getAutenticacao() { // hisThread
  //Serial.println("Verifica RFID"); // debug
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  // Selecione um dos cartões
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  //Mostra o UID na serial
  Serial.println();
  Serial.println();
  Serial.print("UID da tag :");
  String conteudo = "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.println();
  //Serial.print("Mensagem : ");
  conteudo.toUpperCase();
  if (conteudo.substring(1) == "40 1F 63 46") { //UID 1 - Chaveiro
    if(estado_aut == false){
      estado_aut = true;  //altera a variavel
    }else{
      estado_aut = false;  //altera a variavel
    }
    //Serial.println("Vaga autenticada");
    buzzer_aprovado();
    delay(2500);
  } else {
    Serial.println("Vaga nao autenticada");
    buzzer_rejeitado();
    delay(2500);
  }
}

void buzzer_aprovado() {
  int frequencia = 3500;
  tone(buzzer, frequencia, 500);
}

void buzzer_rejeitado() {
  int frequencia = 300;
  tone(buzzer, frequencia, 500);
}
