/*
midi_reader_advanced.ino

Cory Hungate

A simple program that reads in midi data and publishes it to serial.
*/

#include <MIDI.h>
#include "Timer.h" 
#include "math.h"

MIDI_CREATE_INSTANCE(HardwareSerial, Serial1, MIDI);

//declaring my global variables, pins, etc
Timer timer; 

long number = 0; 
int num1 = 0;
int num2 = 0;
int num3 = 0;
int num4 = 0;
int timer_event = 0;

int D1 = 2;
int D2 = 3;
int D3 = 4;
int D4 = 5;

int latchPin = 9;
int clockPin = 10;
int dataPin = 8;

int count = 0;
int numbers[4] ;
int cathodePins[] = {2, 3, 4, 5};

unsigned long int last_update = 0;
int DELAY_TIME = 2000;

byte table[10] {B11111100, B01100000, B11011010, B11110010, B01100110, B10110110, B10111110, B11100000, B11111110, B11110110};

// Handle "note on" events
void handleNoteOn(byte channel, byte pitch, byte velocity) {
  Serial.print("Note On - Channel: ");
  Serial.print(channel);
  Serial.print(" Pitch: ");
  Serial.println(pitch);

  //not using the velocity data at the moment. might turn it back on later
  // Serial.print(" Velocity: ");
  // Serial.println(velocity);
}


//handler for reading knob movements on the midi controller 
void handleKnobChange(byte channel, byte control, byte value){

  //values come in btwn 0-127, so remapping them to a 0-100 value
  int mappedValue = map(value, 0, 127, 0, 100);

  //modifying the control value to reflect the label on the physical controller
  int modifiedControl = control - 9;

  Serial.print ("Knob: ");
  Serial.print (modifiedControl);
  Serial.print (" value: ");
  Serial.println (mappedValue);
}

//get the digits from incoming serial data
void separate(long num) { 
  for (int i = 3; i>=0; i--) {
    int divisor = (int)pow(10, i);
    numbers[3 - i] = num / divisor;
    num = num % divisor;
  }
}


//function for firing the appropriate LEDs on the correct digit pin
//if I wanted to have a leading zero be white space, this is probably where to do it...
void Display() {
  screenOff(); 
  digitalWrite(latchPin, LOW); 
  shiftOut(dataPin, clockPin,LSBFIRST, table[numbers[count]]); 
  digitalWrite(cathodePins[count], LOW); 
  digitalWrite(latchPin, HIGH); 
  count++; 
  if (count == 4) { 
    count = 0;
  }
}


//quick function to turn the screen off
void screenOff() { 
  digitalWrite(D4, HIGH);
  digitalWrite(D3, HIGH);
  digitalWrite(D2, HIGH);
  digitalWrite(D1, HIGH);
}


void setup() {
  //initializing serial ports
  Serial.begin(115200);   //serial read/write
  Serial1.begin(9600);    //read data from MIDI

  //other setup for the MIDI controller data
  MIDI.begin(MIDI_CHANNEL_OMNI);  // Listen to all channels
  MIDI.setHandleNoteOn(handleNoteOn);
  MIDI.setHandleControlChange(handleKnobChange);
  Serial.println("MIDI Library Active");

  //other setup for the LED display functionality
  pinMode(D4, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D1, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  digitalWrite(D4, HIGH);
  digitalWrite(D3, HIGH);
  digitalWrite(D2, HIGH);
  digitalWrite(D1, HIGH);

  screenOff();
  timer.every(1,Display);
}



void loop() {
  MIDI.read();  // Continuously read incoming messages

  //after delay, display a random number
  timer.update();
  
  if (Serial.available()){
    String s = Serial.readStringUntil('\n');
    int num = s.toInt();
    separate(num);
  }
}


