# 🌦️ IoT Weather Station

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)

Project using an Arduino and Sensors connected to a Raspberry Pi to build a functional, telemetry-logging meteorological station. 

## 🗺️ Hardware & Data Flow Diagram

```mermaid
graph TD
    A[BMP280 Sensor<br>Temp/Pressure] -->|I2C| R(Raspberry Pi)
    B[LSM303 Sensor<br>Accel] -->|I2C| R
    C[LIS2MDL Sensor<br>Magnetometer] -->|I2C| R
    D[GPS/Telemetry] -->|Serial| E(Arduino)
    E -->|Serial| R
    R -->|Log to File| F(DadosGeofisicos.txt)
    R -->|Log to File| G(Satelites.txt)
```

## 🛠️ Bill of Materials (BOM)

- **Microcontrollers:** Raspberry Pi 3/4, Arduino Uno/Mega
- **Sensors:**
  - BMP280 (Temperature & Pressure)
  - LSM303 (Accelerometer)
  - LIS2MDL (Magnetometer)
  - GPS Module (for Telemetry)
- **Cables:** Jumper wires (I2C, Serial, Power), USB Cable for Arduino -> Pi connection.

## 🔌 Wiring Overview

| Sensor / Module | Connection to Pi/Arduino | Protocol / Pins |
|-----------------|--------------------------|-----------------|
| BMP280          | Raspberry Pi             | I2C (SDA, SCL)  |
| LSM303          | Raspberry Pi             | I2C (SDA, SCL)  |
| LIS2MDL         | Raspberry Pi             | I2C (SDA, SCL)  |
| GPS             | Arduino                  | UART (RX, TX)   |
| Arduino         | Raspberry Pi             | USB Serial      |

## 🚀 Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/meteostation.git
   cd meteostation
   ```

2. **Install dependencies:**
   ```bash
   pip install adafruit-blinka adafruit-circuitpython-bmp280 adafruit-circuitpython-lsm303-accel adafruit-circuitpython-lis2mdl pyserial pandas numpy matplotlib
   ```

3. **Run the weather station script:**
   ```bash
   python3 Raspberry_bmp_lsm.py
   ```

4. **Visualize data:**
   Lively recommend using [TelemetryViewer](http://www.farrellf.com/TelemetryViewer/) to visualize the data from afar!
