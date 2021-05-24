//1. Conectar fuente a corriente
//2.

void setup() {
  //Pines del relé
  //VCC - 5V
  //GND - GND
  //IN - Pin 3
  pinMode(3,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(3, LOW);
  //Poner en 1000 al inicio para que llene la sonda rapidamente
  //Poner en 20 para dispensar una gota
  delay(20);
  digitalWrite(3,HIGH);
  while(true){}
}
