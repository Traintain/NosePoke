//Pin conections

const int IRDer=3;
const int IN1 = 11;
const int IN2 = 10;
const int IN3 = 9;
const int IN4 = 8;

int nSpeed=1;
int currentStep = 0; //Indicates the next row in the step's matrix

int der;
int COM=-1;
bool metioNariz;
float tIni;
float tInterm;
int perseveraciones;

int eachStep[8][4]={
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1} };

void setup() {
  pinMode(IRDer, INPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
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

void avanzar(int turn){
  for(int i=0;i<turn;i++){
    digitalWrite(IN1, eachStep[currentStep][0]);
    digitalWrite(IN2, eachStep[currentStep][1]);
    digitalWrite(IN3, eachStep[currentStep][2]);
    digitalWrite(IN4, eachStep[currentStep][3]);
    currentStep=(currentStep+1)%8;
    delay(nSpeed);  
  }
}

void loop() {
   while(COM!=57){
     COM=Serial.read();
   }
   Serial.println("Van a empezar los 50 ensayos");
   //Haga 50 ensayos
   for(int i=0; i<50; i++){
     Serial.println(i);
     ensayo();
   }
}

void ensayo(){

  perseveraciones=0;
  metioNariz=false;
  
  Serial.println("Inicia ensayo");
  tIni=millis();  
  //Ver durante 15s si el animal metió la nariz
  while(((millis()-tIni) < 15000) && metioNariz==false){
    Serial.println(millis()-tIni);
    der=digitalRead(IRDer);
    if(der==LOW){
      metioNariz=true;
      Serial.println("Metió la nariz: " + millis()-tIni);
      avanzar(2400);
   }
  }
  
  Serial.println("Fin ensayo, inician 10 seg de espera");
  tInterm=millis();
  while((millis()-tInterm) < 10000){
    der=digitalRead(IRDer);
    if(der==LOW){
      perseveraciones++;
      Serial.println("Perseveracion "+ perseveraciones);
      while(der==LOW){
      }
      tInterm = millis();
    }
  }
}
