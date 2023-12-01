#include <SD.h>
#include <SPI.h>
#include "Adafruit_MAX31855.h"

// CS pins for all thermocouples (MAXDO and MAXCLK are shared by all)
int MAXDO = 2;  // digital output pin (shared by all)
int MAXCS1 = 3;
int MAXCS2 = 4;
int MAXCS3 = 5;
int MAXCS4 = 6;
int MAXCS5 = 7;
int MAXCS6 = 8;
int MAXCS7 = 9;
int MAXCS8 = 11;
int MAXCLK = 12;  // clock pin (shared by all)
int CS = 10;      // SD card's digital pin (MUST BE 10)

// output File
File file;
// set logging frequency in minutes
double minutes = 1/60; // this value is multiplied by 60000 milliseconds (1/60 minutes = 1 second)
// state of the onboard LED (solid on = SD Card full, slow blink = wait (SD card not inserted), fast blink = logging in progress)

// initializing all 8 thermocouples
Adafruit_MAX31855 thermocouple1(MAXCLK, MAXCS1, MAXDO);
Adafruit_MAX31855 thermocouple2(MAXCLK, MAXCS2, MAXDO);
Adafruit_MAX31855 thermocouple3(MAXCLK, MAXCS3, MAXDO);
Adafruit_MAX31855 thermocouple4(MAXCLK, MAXCS4, MAXDO);
Adafruit_MAX31855 thermocouple5(MAXCLK, MAXCS5, MAXDO);
Adafruit_MAX31855 thermocouple6(MAXCLK, MAXCS6, MAXDO);
Adafruit_MAX31855 thermocouple7(MAXCLK, MAXCS7, MAXDO);
Adafruit_MAX31855 thermocouple8(MAXCLK, MAXCS8, MAXDO);


void setup() {

  // overwrite existing file
  if (SD.exists("output.csv")) {  // overwrite output file
    Serial.println("File exists");
    if (SD.remove("output.csv") == true) {
      Serial.println("File removed");
    } else {
      Serial.println("Could not remove file");
    }
  }
  Serial.begin(9600);
  // give the MAX time to settle
  delay(500);
}

void loop() {

  // initialize SD card - logging occurs only if card is present
  pinMode(CS, OUTPUT);  // set SD pin to output
  if (!SD.begin(CS)) {
    Serial.println("Could not initialize SD card - make sure SD card is inserted");
    return;
  }

  // basic readout test
  Serial.print("TC 1 = ");
  Serial.print(thermocouple1.readCelsius());
  Serial.print("   ");
  Serial.print("TC 2 = ");
  Serial.print(thermocouple2.readCelsius());
  Serial.print("   ");
  Serial.print("TC 3 = ");
  Serial.print(thermocouple3.readCelsius());
  Serial.print("   ");
  Serial.print("TC 4 = ");
  Serial.print(thermocouple4.readCelsius());
  Serial.print("   ");
  Serial.print("TC 5 = ");
  Serial.print(thermocouple5.readCelsius());
  Serial.print("   ");
  Serial.print("TC 6 = ");
  Serial.print(thermocouple6.readCelsius());
  Serial.print("   ");
  Serial.print("TC 7 = ");
  Serial.print(thermocouple7.readCelsius());
  Serial.print("   ");
  Serial.print("TC 8 = ");
  Serial.print(thermocouple8.readCelsius());
  Serial.println();

  writeFile();  // write data to file

  delay(60000 * minutes);  // delay between readings (adjust as needed)
}

void writeFile() {  // write data to SD card
  using namespace std;
  file = SD.open("output.csv", FILE_WRITE);
  if (file) {
    file.println(String(thermocouple1.readCelsius()) + ";" + String(thermocouple2.readCelsius()) + ";" + String(thermocouple3.readCelsius()) + ";" + String(thermocouple4.readCelsius()) + ";" + String(thermocouple5.readCelsius()) + ";" + String(thermocouple6.readCelsius()) + ";" + String(thermocouple7.readCelsius()) + ";" + String(thermocouple8.readCelsius()));
    file.close();
    Serial.println(String(thermocouple1.readCelsius()) + ";" + String(thermocouple2.readCelsius()) + ";" + String(thermocouple3.readCelsius()) + ";" + String(thermocouple4.readCelsius()) + ";" + String(thermocouple5.readCelsius()) + ";" + String(thermocouple6.readCelsius()) + ";" + String(thermocouple7.readCelsius()) + ";" + String(thermocouple8.readCelsius()));
  } else {
    Serial.println("Could not write to file");
  }
}