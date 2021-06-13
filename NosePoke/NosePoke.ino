//1. Conectar fuente a corriente
//2.
const int LED_Right=6;
const int LED_Left=5;
const int LED_center=7;
const int MOTOR=8;
const int IR_Right=4;
const int IR_Left=3;

int right;
int left;

void setup() {
  //Pines del relé
  //VCC - 5V
  //GND - GND
  //IN - Pin 3
    pinMode(IR_Right, INPUT);
  pinMode(IR_Left, INPUT);
    pinMode(LED_Right, OUTPUT);
  pinMode(LED_Left, OUTPUT);
  pinMode(LED_center, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  //Poner en 1000 al inicio para que llene la sonda rapidamente
  //Poner en 20 para dispensar una gota
    digitalWrite(LED_Right,HIGH);
    digitalWrite(LED_center,HIGH);
    digitalWrite(LED_Left,HIGH);
    digitalWrite(MOTOR,HIGH);
    delay(1000);
  while(true){
    right=digitalRead(IR_Right);
    left=digitalRead(IR_Left);
    Serial.print("Derecha: ");
    Serial.println(right);
    Serial.print("Izquierda: ");
    Serial.println(left);
    }
}
