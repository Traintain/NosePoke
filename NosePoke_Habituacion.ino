#include <Stepper.h>

//Pines a los que se conectan los sensores
int led1=1;
int led2=2;
int IRDer=3;
int IRIzq=4;
const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper motorAgua(stepsPerRevolution, 8, 9, 10, 11);

int stepCount = 0;  // number of steps the motor has taken
int der;
int izq;
String COM;
bool metioNariz;
float tIni;
float tInterm;

void setup() {
  // put your setup code here, to run once:
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(IRDer, INPUT);
  pinMode(IRIzq, INPUT);
  motorAgua.setSpeed(60);
  Serial.begin(9600);
  //Comprobar comunicación con PC
  Serial.println("Transmitiendo");
  COM=Serial.read();
  if(COM!="Recibiendo"){
    //Error en caso de que no haya comunicación
    Serial.println("Error");
  }else{
    //Todo va bien
    Serial.println("Ok");
  }
}

void loop() {
   while(COM!="Inicio"){
     COM=Serial.read();
   }
   //Haga 50 ensayos
   for(int i=0; i<50; i++){
     ensayo();
   }
   
}

void ensayo(){
  //En este momento se prenden ambos leds
  digitalWrite(led1,HIGH);
  digitalWrite(led2,HIGH);

  metioNariz=false;
  
  tIni=millis();
  
  //Ver durante 15s si el animal meitió la nariz
  while((millis()-tIni < 15000) || metioNariz==false){
    der=digitalRead(IRDer);
    izq=digitalRead(IRDer);
    if(der!=0 || izq!=0){
      metioNariz=true;
      motorAgua.step(stepsPerRevolution); //Indicar al motor que gire y cuanto
    }
  }
  digitalWrite(led1,LOW);
  digitalWrite(led2,LOW);

  tInterm=millis();
  while((millis()-tInterm < 10000)){
    der=digitalRead(IRDer);
    izq=digitalRead(IRDer);
    if(der!=0 || izq!=0){
      Serial.println(millis()+", perseveracion");
      tInterm = millis();
    }
  }
}

