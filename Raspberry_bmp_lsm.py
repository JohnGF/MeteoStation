from time import sleep
from datetime import datetime
import board
import adafruit_bmp280
import busio
import adafruit_lsm303_accel
import adafruit_lis2mdl
import serial
import os
import sys

def initialize_sensors():
    try:
        arduinoData = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    except Exception as e:
        print(f"Failed to initialize serial: {e}")
        arduinoData = None

    try:
        i2c = board.I2C()
        accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
        mag = adafruit_lis2mdl.LIS2MDL(i2c)
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    except Exception as e:
        print(f"Failed to initialize I2C sensors: {e}")
        return arduinoData, None, None, None, None

    return arduinoData, i2c, accel, mag, sensor

def read_sensor_data(sensor, accel, mag):
    try:
        temperature = sensor.temperature
        pressure = sensor.pressure
        acceleration = accel.acceleration
        magnetic = mag.magnetic
        return temperature, pressure, acceleration, magnetic
    except Exception as e:
        print(f"Error reading sensors: {e}")
        return None, None, None, None

def format_sensor_data(temperature, pressure, acceleration, magnetic):
    if None in (temperature, pressure, acceleration, magnetic):
        return None
    try:
        return ",{},{},".format(temperature, pressure) + "%0.3f,%0.3f,%0.3f," % acceleration + "%0.3f,%0.3f,%0.3f" % magnetic
    except Exception as e:
        print(f"Error formatting sensor data: {e}")
        return None

def read_telemetry(arduinoData):
    if arduinoData is None:
        return None
    try:
        if arduinoData.in_waiting > 0 or True: # Readline blocks anyway, timeout makes it safe
            cc = arduinoData.readline()
            if cc:
                return str(cc)
        return None
    except Exception as e:
        print(f"Error reading telemetry: {e}")
        return None

def main_loop(arduinoData, sensor, accel, mag, max_samples=45):
    first = 0
    n = 0
    
    try:
        with open("DadosGeofisicos.txt", 'w') as f, open("Satelites.txt", "w") as fs:
            while n < max_samples:
                temperature, pressure, acceleration, magnetic = read_sensor_data(sensor, accel, mag)
                c = format_sensor_data(temperature, pressure, acceleration, magnetic)
                
                if first == 0:
                    first = 1
                    f.write("Data,Temp_Celcius,Pressure_hPa,accelaration X (m/s^2),accelaration Y (m/s^2),accelaration Z (m/s^2),Magnetometer X (micro-Teslas),Magnetometer Y (micro-Teslas),Magnetometer Z (micro-Teslas)\n")
                else:
                    if c:
                        f.write(datetime.now().isoformat() + '\t' + c + '\n')
                
                cc = read_telemetry(arduinoData)
                if cc:
                    fs.write(cc + "\n")
                
                f.flush()
                os.fsync(f.fileno())
                
                fs.flush()
                os.fsync(fs.fileno())

                n = n + 1
                print("Amostra %i de %i" % (n, max_samples))
                sleep(1)
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        if arduinoData:
            arduinoData.close()

if __name__ == "__main__":
    arduinoData, i2c, accel, mag, sensor = initialize_sensors()
    if sensor and accel and mag:
        sleep(2)
        main_loop(arduinoData, sensor, accel, mag)
    else:
        print("Sensors failed to initialize. Exiting.")
        sys.exit(1)
