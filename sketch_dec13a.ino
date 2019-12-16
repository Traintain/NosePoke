int eachStep [8][4] ={
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1} };

const int IN1 = 11;
const int IN2 = 10;
const int IN3 = 9;
const int IN4 = 8;

int steps_left=4095;
int currentStep = 0; //Indicates the next row in the step's matrix
int nSpeed=1;

void setup() {
  Serial.begin(9600);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  avanzar(2400);
  delay(1000);
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
