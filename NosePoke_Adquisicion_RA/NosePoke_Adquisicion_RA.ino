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
//Number of impulsive responses. An impulsive response is when the animal inserts its nose during the ITI
int impulsive;
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
int temp;
//Error de seleccion: numero de errores antes del primer acierto
int errSelec;
//Perseveracion primaria
int EPP;
//Perseveracion secundaria
int EPS;
//Aciertos por segmento
int aciertoTemprano;
int aciertoIntermedio;
int aciertoFinal;


int right;
int left;
int COM=-1;
//Integer that counts the number of consecutives succeses
int sucesiveSuccess;
bool metioNariz;
unsigned long tIni;
unsigned long tInterm;
unsigned long persev;
unsigned long tLog;
String msg="";

//Number between 0 and 2, that indicates the side where the animal should drink
long randomSide;
bool isRight;
int firstCorrect;


void setup() {
  //Setup of the different pins
  pinMode(IR_Right, INPUT);
  pinMode(IR_Left, INPUT);
  pinMode(LED_Right, OUTPUT);
  pinMode(LED_Left, OUTPUT);
  pinMode(LED_center, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  digitalWrite(MOTOR,HIGH);
  randomSeed(analogRead(0));
  
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
    firstCorrect=0;
    errSelec=0;
    EPP=0;
    EPS=0;
    aciertoTemprano=0;
    aciertoIntermedio=0;
    aciertoFinal=0;
    
    Serial.print("Van a empezar los ");
    Serial.print(nTrials);
    Serial.println(" ensayos");
    //Wait 5 seconds for habituation
    delay(ITI);
    //Begin 50 trials
    for(int i=0; i<nTrials; i++){
      Serial.print("Ensayo numero: ");
      temp=i+1;
      Serial.println(temp);
      trial(i);
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
      Serial.print("Respuestas impulsivas: ");
      Serial.println(impulsive);
      Serial.print("Porcentaje respuestas impulsivas: ");
      temp=(impulsive*100/nTrials);
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Omisiones: ");
      Serial.println(omission);
      Serial.print("Porcentaje omisiones: ");
      temp=(omission*100/nTrials);
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Categorias: ");
      Serial.println(category);
      Serial.print("La latencia promedio es de: ");
      if(success!=0){
        temp=latency/success;
      }else{
        temp=0;
      }
      Serial.print(temp);
      Serial.println(" ms");
      Serial.print("Errores de perseveración primarios: ");
      Serial.println(EPP);
      Serial.print("Porcentaje errores de perseveración primarios: ");
      if(success!=0){
        temp=(EPP*100/success);
      }else{
        temp=0;
      }
      Serial.print(temp);
      Serial.println("%");
            Serial.print("Errores de perseveración secundarios: ");
      Serial.println(EPS);
      Serial.print("Porcentaje errores de perseveración secundarios: ");
      if(EPP!=0){
        temp=(EPP*100/EPS);
      }else{
        temp=0;
      }
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Errores de seleccion: ");
      Serial.println(errSelec);
      Serial.print("Porcentaje errores de selección: ");
      if(firstCorrect!=0){
        temp=(errSelec*100/firstCorrect);
      }else{
        temp=0;
      }
      Serial.print(temp);
      Serial.println("%");
      Serial.print("Adquisicion de reglas: ");
      temp=aciertoTemprano/17;
      Serial.println(temp);
      Serial.print("Establecimiento de reglas: ");
      temp=aciertoIntermedio/16;
      Serial.println(temp);
      Serial.print("Mantenimiento de reglas: ");
      temp=aciertoFinal/17;
      Serial.println(temp);
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
void trial(int i){
  metioNariz=false;

  randomSide=random(0,2);
  isRight=randomSide<1;
  
  Serial.println("Inicia ensayo");
  tIni=millis();
  
  //Check fot 10 seconds if the animal inserts its nose
  while(( (millis()-tIni) < durTrial) && metioNariz==false){
    if(isRight){
      digitalWrite(LED_Right,HIGH);
      Serial.println("Se enciende la luz derecha");
    }else{
      digitalWrite(LED_Left,HIGH);
      Serial.println("Se enciende la luz izquierda");
    }
    
    right=digitalRead(IR_Right);
    left=digitalRead(IR_Left);
    if(right==LOW){
      tLog=millis()-tIni;
      Serial.print("Metio la nariz en la derecha a los: ");
      Serial.println(tLog);
      if(isRight){
        digitalWrite(LED_Right,LOW);
        motor();
        //Exito
        if(firstCorrect==0){
          firstCorrect=i+1;
          Serial.print("Primer acierto en el intento: ");
          Serial.println(firstCorrect);
        }
        success++;
        if(i<=16){
          aciertoTemprano++;
        }else if(i<=32){
          aciertoIntermedio++;
        }else{
          aciertoFinal++;
        }
        if((sucesiveSuccess%3)==2)category++;
        sucesiveSuccess++;
      }else{
        //Fallo
        digitalWrite(LED_Left,LOW);
        if(firstCorrect==0){
          errSelec++;
          Serial.println("Error de selección");
        }else{
          if(sucesiveSuccess!=0){
            EPP++;
            Serial.println("Error de perseveración primaria");
            sucesiveSuccess=0;
          }else{
            EPS++;
            Serial.println("Error de perseveración secundaria");
          }
        }
      }
      while(right==LOW){
        right=digitalRead(IR_Right);
      }
      latency+=tLog;
      metioNariz=true;
   }

   if(left==LOW){
      tLog=millis()-tIni;
      Serial.print("Metio la nariz en la izquierda a los: ");
      Serial.println(tLog);
      if(isRight){
        //Fallo
        digitalWrite(LED_Right,LOW);
        if(firstCorrect==0){
          errSelec++;
          Serial.println("Error de selección");
        }else{
          if(sucesiveSuccess!=0){
            EPP++;
            Serial.println("Error de perseveración primaria");
            sucesiveSuccess=0;
          }else{
            EPS++;
            Serial.println("Error de perseveración secundaria");
          }
        }
      }else{
        //Exito
        digitalWrite(LED_Left,LOW);
        motor();
        //Exito
        if(firstCorrect==0){
          firstCorrect=i+1;
          Serial.print("Primer acierto en el intento: ");
          Serial.println(firstCorrect);
        }
        success++;
        if((sucesiveSuccess%3)==2)category++;
        sucesiveSuccess++;
      }
      while(left==LOW){
        left=digitalRead(IR_Left);
      }
      latency+=tLog;
      metioNariz=true;
   }
  }

  //------------------------
  if(metioNariz==false){
    digitalWrite(LED_Right,LOW);
    digitalWrite(LED_Left,LOW);
    omission++;
    Serial.print("Omision numero:");
    Serial.println(omission);
    sucesiveSuccess=0;
  }
  //------------------------

  
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
      impulsive++;
      Serial.print("Perseveracion numero: ");
      Serial.println(impulsive);
      while(right==LOW || left==LOW){
        right=digitalRead(IR_Right);
        left=digitalRead(IR_Left);
      }
      tInterm = millis();
      Serial.println("Inician de nuevo ");
      Serial.print(ITIsec);
      Serial.println(" s de espera");
    }
  }
}
