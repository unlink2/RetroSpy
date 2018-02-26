#define MD_PIN_1 2 // start of pins, this requries the 6 next pins as well
#define MD_SELECT_PIN 8

#define ZERO  '\0'  // Use a byte value of 0x00 to represent a bit with value 0.
#define ONE    '\1'  // Use an ASCII one to represent a bit with value 1.  This makes Arduino debugging easier.
#define SPLIT '\n'  // Use a new-line character to split up the controller state packets.


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// General initialization, just sets all pins to input and starts serial communication.
void setup() {
  PORTD = 0x00;
  DDRD  = 0x00;
  PORTC = 0xFF; // Set the pull-ups on the port we use to check operation mode.
  DDRC  = 0x00;
  Serial.begin(115200);
}

/*
 * The Megadrive input spy returns 4 bytes
 * byte 1 = pin 1-9 with 7 high
 * byte 2 = pin 1-9 with 7 low
 * Connect MD pins as such (Starting at Arduino PIN 2)
 * DBUS1 = A2
 * DBUS2 = A3
 * DBUS3 = A4
 * DBUS4 = A5
 * Do not connect DBUS5
 * DBUS6 - A6
 * DBUS7 = A8
 * DBUS8 = Ground
 * DBUS9 = A7
 */
inline void loop_MD() {
  // read the state of all lines
  // this is faster and therefore better for md purposes
  // to increase our chance of getting all inputs
  Serial.write(PIND);
  
  // now we wait for pin 7 to be 0
  while(digitalRead(MD_SELECT_PIN) != 0) {}

  Serial.write(PIND);
  Serial.write(SPLIT);
}

void loop() {
  loop_MD();
}

