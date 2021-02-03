
#include <Stepper.h>

// change this to the number of steps on your motor
#define STEPS 150
  
// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 8, 9, 10, 11);
int a;


void setup() {
  // set the speed of the motor to 30 RPMs
  stepper.setSpeed(120);
  pinMode(3,INPUT);
  Serial.begin(9600);
}

void loop() {
  for(int i=0;i<4;i++){
    stepper.step(STEPS);
    delay(20);
  }
  delay(4000);
  a=digitalRead(3);
  Serial.println(a);
}
