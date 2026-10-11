import pytest
from unittest.mock import MagicMock, patch, PropertyMock

# In circuitpython, board.I2C() can fail if not on a raspberry pi, 
# but testing shouldn't depend on actual hardware. We need to patch 
# board *before* it tries to do platform-specific things if possible, 
# or just patch it in the station file.
import sys
for mod in ['board', 'serial', 'adafruit_bmp280', 'adafruit_lsm303_accel', 'adafruit_lis2mdl', 'busio']:
    sys.modules[mod] = MagicMock()

import Raspberry_bmp_lsm as station

@patch('Raspberry_bmp_lsm.serial.Serial')
@patch('Raspberry_bmp_lsm.board')
@patch('Raspberry_bmp_lsm.adafruit_lsm303_accel.LSM303_Accel')
@patch('Raspberry_bmp_lsm.adafruit_lis2mdl.LIS2MDL')
@patch('Raspberry_bmp_lsm.adafruit_bmp280.Adafruit_BMP280_I2C')
def test_initialize_sensors_success(mock_bmp, mock_mag, mock_accel, mock_board, mock_serial):
    arduinoData, i2c, accel, mag, sensor = station.initialize_sensors()
    assert arduinoData is not None
    assert i2c is not None
    assert accel is not None
    assert mag is not None
    assert sensor is not None

@patch('Raspberry_bmp_lsm.serial.Serial', side_effect=Exception("Serial Error"))
@patch('Raspberry_bmp_lsm.board.I2C', side_effect=Exception("I2C Error"))
def test_initialize_sensors_failure(mock_i2c, mock_serial):
    arduinoData, i2c, accel, mag, sensor = station.initialize_sensors()
    assert arduinoData is None
    assert i2c is None
    assert accel is None
    assert mag is None
    assert sensor is None

def test_read_sensor_data_success():
    mock_sensor = MagicMock()
    mock_sensor.temperature = 25.0
    mock_sensor.pressure = 1013.25
    
    mock_accel = MagicMock()
    mock_accel.acceleration = (0.0, 0.0, 9.8)
    
    mock_mag = MagicMock()
    mock_mag.magnetic = (1.0, 2.0, 3.0)
    
    temp, press, acc, mag = station.read_sensor_data(mock_sensor, mock_accel, mock_mag)
    
    assert temp == 25.0
    assert press == 1013.25
    assert acc == (0.0, 0.0, 9.8)
    assert mag == (1.0, 2.0, 3.0)

def test_read_sensor_data_failure():
    mock_sensor = MagicMock()
    type(mock_sensor).temperature = PropertyMock(side_effect=Exception("I2C Read Error"))
    
    temp, press, acc, mag = station.read_sensor_data(mock_sensor, MagicMock(), MagicMock())
    
    assert temp is None
    assert press is None
    assert acc is None
    assert mag is None

def test_format_sensor_data():
    temp = 25.0
    press = 1013.25
    acc = (0.0, 0.0, 9.8)
    mag = (1.0, 2.0, 3.0)
    
    formatted = station.format_sensor_data(temp, press, acc, mag)
    assert formatted == ",25.0,1013.25,0.000,0.000,9.800,1.000,2.000,3.000"

def test_format_sensor_data_with_none():
    formatted = station.format_sensor_data(None, 1013.25, (0,0,0), (0,0,0))
    assert formatted is None

def test_read_telemetry_success():
    mock_serial = MagicMock()
    mock_serial.in_waiting = 10
    mock_serial.readline.return_value = b'GPS Data\n'
    
    telemetry = station.read_telemetry(mock_serial)
    assert telemetry == "b'GPS Data\\n'"

def test_read_telemetry_none():
    telemetry = station.read_telemetry(None)
    assert telemetry is None

def test_read_telemetry_error():
    mock_serial = MagicMock()
    mock_serial.readline.side_effect = Exception("Read Error")
    
    telemetry = station.read_telemetry(mock_serial)
    assert telemetry is None

@patch('Raspberry_bmp_lsm.read_sensor_data')
@patch('Raspberry_bmp_lsm.read_telemetry')
@patch('Raspberry_bmp_lsm.sleep')
@patch('Raspberry_bmp_lsm.os.fsync')
def test_main_loop(mock_fsync, mock_sleep, mock_telemetry, mock_sensor_data):
    mock_sensor_data.return_value = (25.0, 1013.25, (0, 0, 9.8), (1, 2, 3))
    mock_telemetry.return_value = "Mock GPS Data"
    
    mock_serial = MagicMock()
    
    # We only run 2 iterations
    station.main_loop(mock_serial, MagicMock(), MagicMock(), MagicMock(), max_samples=2)
    
    assert mock_sleep.call_count == 2
    assert mock_sensor_data.call_count == 2
    assert mock_telemetry.call_count == 2
    mock_serial.close.assert_called_once()
