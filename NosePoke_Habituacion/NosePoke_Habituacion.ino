//This library allows to control the stepper motor

//Pin conections
//Infrared sensors on the holes
const int IR_Right=4;
const int IR_Left=3;
const int MOTOR=8;
//Contecions for the LED lights
const int LED_Right=6;
const int LED_Left=5;
const int LED_center=7;

//Motor constants
//120 steps per turn dispense 0.017 ml aprox. Above 120 RPM the motor get clumsy
int nSpeed=120;
int nSteps=150;

//Number of blocks
const int nBlocks=1;
//Number of trials per block
const int nTrials=50;
//Inter trial interval, in miliseconds
const int ITI=5000;
int ITIsec=ITI/1000;
//Maximum duration of each trial, in milisencods
const int durTrial=10000;
//Reward period, in case the nose enters while the trial, in miliseconds
const int durReward=3000;

//Output constants
//Number of successful trials. Can be up to 50 por block.
int success;
//Time spend on impulsive responses. An impulsive response is when the animal inserts its nose during the ITI
unsigned long impulsive;
//Number of omissions. An omision response is when the animal doesn't inster its nose during a trial
int omission;
//Number of categories. A category is when a animal has 3 successes in a row.
int category;
//Number of right correct choices
int goodRight;
//Number of left correct choices
int goodLeft;
//mean of the latency of each block
unsigned long latency;
//temporal number for math
double temp;

//Object that represents the motor
//Stepper pump(nSteps, IN4,IN3,IN2,IN1);

int right;
int left;
int COM=-1;
//Integer that counts the number of consecutives succeses
int sucesiveSuccess;
bool metioNariz;
unsigned long inicio;
unsigned long fin;
unsigned long tIni;
unsigned long tInterm;
unsigned long tLog;
String msg="";


void setup() {
  //Setup of the different pins
    pinMode(IR_Right, INPUT);
    pinMode(IR_Left, INPUT);
  pinMode(LED_Right, OUTPUT);
  pinMode(LED_Left, OUTPUT);
  pinMode(LED_center, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  digitalWrite(MOTOR,HIGH);
  
//  pump.setSpeed(nSpeed);
  Serial.begin(9600);
  //Comprobar comunicación con PC
  Serial.println("Transmitiendo");
  //while(COM==-1){
  //  COM=Serial.read();
  //}
  //To check the serial comunication the PC sends a number 6.
  //if(COM!=54){
    //Error en caso de que no haya comunicación
  //  Serial.println("Error");
  //}else{
    //Todo va bien
  //  Serial.println("Ok");
  //}
}

//Method to make the motor turn
void motor(){
  Serial.println("Iniciando un ciclo del motor");
  digitalWrite(LED_center,HIGH);
  digitalWrite(MOTOR,LOW);
  //Poner en 1000 al inicio para que llene la sonda rapidamente
  //Poner en 20 para dispensar una gota
  delay(20);
  digitalWrite(MOTOR,HIGH);
  delay(durReward);
  digitalWrite(LED_center,LOW);
}

//To initiate the protocol the PC must send a number 9
void loop() {
   //while(COM!=57){
   //  COM=Serial.read();
   //}
   
   //Run two blocks
   for(int j=0; j<nBlocks;j++){
    //Reset the output counters
    success=0;
    impulsive=0;
    omission=0;
    category=0;
    sucesiveSuccess=0;
    temp=0;
    goodLeft=0;
    goodRight=0;
    latency=0;
    
    Serial.println("Van a empezar los 50 ensayos");
    //Wait 5 seconds for habituation
    delay(ITI);
    //Begin 50 trials
    inicio=millis();
    for(int i=0; i<nTrials; i++){
      Serial.print("Ensayo numero: ");
      temp=i+1;
      Serial.println(temp);
      trial();
      Serial.println("Termina ensayo.");
      if(i==49){
        Serial.println("***********************************");
        }
      Serial.println("--------------------------------------------------");
      Serial.print("Aciertos: ");
      Serial.println(success);
      Serial.print("Porcentaje aciertos: ");
      temp=(success*100/nTrials);
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Tiempo total en Respuestas impulsivas: ");
      temp=impulsive/1000;
      Serial.println(temp);
      //Serial.print("Porcentaje respuestas impulsivas: ");
      //temp=(impulsive*100/nTrials);
      //Serial.print(temp);
      //Serial.println("%");
      Serial.print("Omisiones: ");
      Serial.println(omission);
      Serial.print("Porcentaje omisiones: ");
      temp=(omission*100/nTrials);
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Categorias: ");
      Serial.println(category);
      Serial.print("Total correctas a la derecha: ");
      Serial.println(goodRight);
      Serial.print("Total correctas a la izquierda: ");
      Serial.println(goodLeft);
      Serial.print("La latencia promedio es de: ");
      if(success!=0){
        temp=latency/success;
      }else{
        temp=0;
      }
      Serial.print(temp);
      Serial.println(" ms");
      Serial.println("--------------------------------------------------");
      if(i==49){
        Serial.println("***********************************");
        }
      
   }
   Serial.println("Terminan bloque de 50 ensayos");
   Serial.println();
   Serial.println();
  }
  while(true);
}

//The instructions for each trial
void trial(){
  metioNariz=false;
  
  Serial.println("Inicia ensayo");
  tIni=millis();
  
  //Check fot 10 seconds if the animal inserts its nose
  while(( (millis()-tIni) < durTrial) && metioNariz==false){
    digitalWrite(LED_Right,HIGH);
    digitalWrite(LED_Left,HIGH);
    //Serial.println(millis()-tIni);
    right=digitalRead(IR_Right);
    left=digitalRead(IR_Left);
    if(right==LOW){
      tLog=millis()-tIni;
      Serial.print("Metio la nariz en la derecha a los: ");
      Serial.println(tLog);
      digitalWrite(LED_Right,LOW);
      digitalWrite(LED_Left,LOW);
      motor();
      while(right==LOW){
        right=digitalRead(IR_Right);
      }
      latency+=tLog;
      goodRight++;
      metioNariz=true;
   }
   if(left==LOW){
      tLog=millis()-tIni;
      Serial.print("Metio la nariz en la izquierda a los: ");
      Serial.println(tLog);
      digitalWrite(LED_Right,LOW);
      digitalWrite(LED_Left,LOW);
      motor();
      while(left==LOW){
        left=digitalRead(IR_Left);
      }
      latency+=tLog;
      goodLeft++;
      metioNariz=true;
   }
  }
  if(metioNariz==false){
    digitalWrite(LED_Right,LOW);
    digitalWrite(LED_Left,LOW);
    omission++;
    Serial.print("Omision numero:");
    Serial.println(omission);
    sucesiveSuccess=0;
  }else{
    success++;
    Serial.print("Exito numero:");
    Serial.println(success);
    if((sucesiveSuccess%3)==2)category++;
    sucesiveSuccess++;
  }
  
  //El animal debe esperar 10 segundos antes de volver a meter la nariz
  //Si la mete antes se reinicia la cuenta
  Serial.print("Fin ensayo, inician ");
  Serial.print(ITIsec);
  Serial.println(" s de intervalo entre estímulos");
  tInterm=millis();
  while((millis()-tInterm) < ITI){
    right=digitalRead(IR_Right);
    left=digitalRead(IR_Left);
    if(right==LOW || left==LOW){
      //impulsive++;
      tIni=millis();
      Serial.println("Inicio de respuesta impulsiva");
      while(right==LOW || left==LOW){
        right=digitalRead(IR_Right);
        left=digitalRead(IR_Left);
      }
      impulsive+=millis()-tIni;
      tInterm = millis();
      Serial.println("Inician de nuevo ");
      Serial.print(ITIsec);
      Serial.println(" s de espera");
    }
  }
}
