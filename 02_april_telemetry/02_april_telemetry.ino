

#include <Wire.h>
#include <Adafruit_LSM303_Accel.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LIS2MDL.h>
#include <HIH4000.h>


/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(54321);
void displaySensorDetails(void) {
  sensor_t sensor;
  accel.getSensor(&sensor);
}
/* -------------------------------------------------- */
Adafruit_LIS2MDL lis2mdl = Adafruit_LIS2MDL(12345);
#define LIS2MDL_CLK 13
#define LIS2MDL_MISO 12
#define LIS2MDL_MOSI 11
#define LIS2MDL_CS 10
/* -------------------------------------------------- */

//calibration sensors
float sea_pressure = 1020.25;
char report[80];
float Pi = 3.14159;

int readPin = A3;
HIH4000 hih(readPin);  //the analog pin where the sensor is connected
float tempC = 44.23;
//------------------------BMP280

#include <SPI.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

Adafruit_BMP280 bmp; // I2C
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

//--------------------


void setup(void) {
#ifndef ESP8266
  while (!Serial);
  //Serial.begin(9600);
#endif
  Serial.begin(115200);
  Wire.begin();
  //--------------------BMP
  while ( !Serial ) delay(100);   // wait for native usb

  unsigned status;
  //status = bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
  status = bmp.begin();
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                     "try a different address!"));
    Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(), 16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }
  /* Initialise the acell sensor */
  if (!accel.begin()) {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while (1)
      ;
  }


  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

  lis2mdl.enableAutoRange(true);
  /* Initialise the sensor */
  if (!lis2mdl.begin()) {  // I2C mode
    //if (! lis2mdl.begin_SPI(LIS2MDL_CS)) {  // hardware SPI mode
    //if (! lis2mdl.begin_SPI(LIS2MDL_CS, LIS2MDL_CLK, LIS2MDL_MISO, LIS2MDL_MOSI)) { // soft SPI
    /* There was a problem detecting the LIS2MDL ... check your connections */
    Serial.println("Ooops, no LIS2MDL detected ... Check your wiring!");
    while (1) delay(10);
  }

  accel.setRange(LSM303_RANGE_4G);
  accel.setMode(LSM303_MODE_NORMAL);//Normal|Low Power|High Resolution

}

void loop(void) {

  //-------BMP

  Serial.print(bmp.readTemperature(), DEC);
  Serial.print(",");
  Serial.print(bmp.readPressure(), DEC);
  Serial.print(",");
  Serial.print(bmp.readAltitude(sea_pressure), 2);
  Serial.print(",");
  //-----------------
  sensors_event_t event;
  accel.getEvent(&event);

  Serial.print(event.acceleration.x);// m/s^2
  Serial.print(",");
  Serial.print(event.acceleration.y);
  Serial.print(",");
  Serial.print(event.acceleration.z);
  Serial.print(",");

  //-----------------

  lis2mdl.getEvent(&event);
  // Calculate the angle of the vector y,x
  float heading = (atan2(event.magnetic.y, event.magnetic.x) * 180) / Pi;
  // Normalize to 0-360
  if (heading < 0)
  {
    heading = 360 + heading;
  }
  /* Display the results (magnetic vector values are in micro-Tesla (uT)) */
  Serial.print(event.magnetic.x);
  Serial.print(",");
  Serial.print(event.magnetic.y);
  Serial.print(",");
  Serial.print(event.magnetic.z);

  //delay(100);
  Serial.print(",");
  float rh = hih.getHumidity(); //humidity with compensation for 25C(typical use)
  Serial.print(rh);
  Serial.print(",");
  tempC = bmp.readTemperature();
  delay(100);//make sure to read temepratue first, dann call .getTrueHumidity
  float truerh = hih.getTrueHumidity(bmp.readTemperature()); //function for temperatue compensated Humidity, tempC can be read from sensor
  Serial.print(truerh);
  Serial.println("");
}
