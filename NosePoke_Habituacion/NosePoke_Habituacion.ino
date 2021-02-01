//This library allows to control the stepper motor
#include <Stepper.h>

//Pin conections

const int IR_Right=3;
const int IN1 = 11;
const int IN2 = 10;
const int IN3 = 9;
const int IN4 = 8;

//Motor constants
//120 steps per turn dispense 0.017 ml aprox. Above 120 RPM the motor get clumsy
int nSpeed=120;
int nSteps=120;

//Object that represents the motor
Stepper pump(nSteps, IN4,IN3,IN2,IN1);


int der;
int COM=-1;
bool metioNariz;
unsigned long tIni;
unsigned long tInterm;
unsigned long persev;
unsigned long tLog;
String msg="";

//To check the serial comunication the PC sends a number 6.
void setup() {
  pinMode(IR_Right, INPUT);
  pump.setSpeed(nSpeed);
  Serial.begin(9600);
  //Comprobar comunicación con PC
  Serial.println("Transmitiendo");
  while(COM==-1){
    COM=Serial.read();
  }
  
  if(COM!=54){
    //Error en caso de que no haya comunicación
    Serial.println("Error");
  }else{
    //Todo va bien
    Serial.println("Ok");
  }
}

//To initiate the protocol the PC must send a number 9
void loop() {
   while(COM!=57){
     COM=Serial.read();
   }
   Serial.println("Van a empezar los 50 ensayos");
   //Begin 50 trials
   for(int i=0; i<50; i++){
     Serial.println("Ensayo numero: "+i);
     ensayo();
   }
}

void ensayo(){
  persev=0;
  metioNariz=false;
  
  Serial.println("Inicia ensayo");
  tIni=millis();
  
  //Ver durante 15s si el animal metió la nariz
  while(((millis()-tIni) < 15000) && metioNariz==false){
    
    Serial.println(millis()-tIni);
    der=digitalRead(IR_Right);
    if(der==LOW){
      tLog=millis()-tIni;
      msg="Metio la nariz a los: ";
      Serial.println(tLog);
      pump.step(nSteps);
      metioNariz=true;
   }
  }
  //El animal debe esperar 10 segundos antes de volver a meter la nariz
  //Si la mete antes se reinicia la cuenta
  Serial.println("Fin ensayo, inician 10 s de espera");
  tInterm=millis();
  while((millis()-tInterm) < 10000){
    der=digitalRead(IR_Right);
    //Si mete la nariz, se suma 1 a las perseveraciones, y apenas la saque inician los 10 s
    if(der==LOW){
      persev++;
      msg="Perseveracion numero:";
      Serial.println(persev);
      while(der==LOW){
        der=digitalRead(IR_Right);
      }
      tInterm = millis();
      Serial.println("Inician 10 s de espera");
    }
  }
}
