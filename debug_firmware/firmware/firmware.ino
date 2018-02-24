/*
 * This firmware allows to read out any digital pin
 * Syntax: RD13 -> reads digital pin 13
 * Future modes might be implemented if the need arises
 */

char operation; // Holds operation (R, W, ...)
char mode; // Holds the mode (D, A)
int pin_number; // Holds the pin number
int digital_value;
const int wait_for_transmission = 5; // Delay in ms in order to receive the serial data
int value_to_write; // Holds the value that we want to write

void set_pin_mode(int pin_number, char mode) {
    /*
     * Performs a pinMode() operation depending on the value of the parameter
     * mode :
     * - I: Sets the mode to INPUT
     * - O: Sets the mode to OUTPUT
     * - P: Sets the mode to INPUT_PULLUP
     */
  switch (mode) {
    case 'I':
      pinMode(pin_number, INPUT);
      break;
     case 'O':
      pinMode(pin_number, OUTPUT);
      break;
     case 'P':
      pinMode(pin_number, INPUT_PULLUP);
      break;
   }
}

void digital_read(int pin_number) {
/*
* Performs a digital read on pin_number and returns the value read to serial
* in this format: D{pin_number}:{value}\n where value can be 0 or 1
*/
  if(pin_number == 0xFF) {
    // 0xFF outputs all pins in a binary string
    Serial.print('D');
    Serial.print(pin_number);
    Serial.print(':');
    for(int i = 2; i <= 13; i++) {
      digital_value = digitalRead(i);
      Serial.print(digital_value);
    }
    Serial.print('\n');
    return;
  }
  
  digital_value = digitalRead(pin_number);
  Serial.print('D');
  Serial.print(pin_number);
  Serial.print(':');
  Serial.println(digital_value); // Adds a trailing \n
}

void digital_write(int pin_number, int digital_value){
    /*
     * Performs a digital write on pin_number with the digital_value
     * The value must be 1 or 0
     */
  digitalWrite(pin_number, digital_value);
}

void setup() {
  Serial.begin(115200); // Serial Port at 115200 baud
  Serial.setTimeout(30); // Instead of the default 1000ms 
}

void loop() {
  if(Serial.available() > 0) {
    operation = Serial.read();
    delay(wait_for_transmission); // If not delayed, second character is not correctly read
    mode = Serial.read();
    pin_number = Serial.parseInt(); // Waits for an int to be transmitted
    if (Serial.read() == ':'){
      value_to_write = Serial.parseInt(); // Collects the value to be written
    }
    switch(operation) {
      case 'R': // Read operation
        if(mode == 'D') {
          digital_read(pin_number);
        }
        break;
      case 'W':
        if(mode == 'D') {
          digital_write(pin_number, value_to_write);
        }
      case 'M': // pin mode
        set_pin_mode(pin_number, mode);
        break;
    }
  }
}

