from time import sleep
from datetime import datetime
import board
import adafruit_bmp280
import busio
import adafruit_lsm303_accel
import adafruit_lis2mdl
#from picamera import PiCamera
import serial,os

arduinoData = serial.Serial('/dev/ttyACM0',115200)
i2c = board.I2C()
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lis2mdl.LIS2MDL(i2c)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
#camera = PiCamera()

condition=True
i=0


#camera.resolution = (1024, 768)
#camera.start_preview()
sleep(2)

#for filename in camera.capture_continuous('img{counter:03d}.jpg'):
#    print('Captured %s' % filename)
#    sleep(10) # wait 10 seconds
#camera.stop_preview()    
#while condition:
#    print('Temperature: {} degrees C'.format(sensor.temperature)) 
#    print('Pressure: {}hPa'.format(sensor.pressure))
#    print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
#    print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
#    sleep(0.5)
#    i=i+1
#    if i==10:
#        condition=False

first=0
n=0
m=45
with open("DadosGeofisicos.txt",'w') as f, open("Satelites.txt","w") as fs:
    while n<m: # while loop that loops forever
        # while (arduinoData.inWaiting()==0): #Wait here until there is data
        #     pass do nothing
        #cc=str(arduinoData.readline())
        #c=cc[2:][:-5]
        c=",{},{},".format(sensor.temperature,sensor.pressure)+"%0.3f,%0.3f,%0.3f,"%accel.acceleration+"%0.3f,%0.3f,%0.3f"%mag.magnetic
        if first==0:
            first=1
            f.write("Data,Temp_Celcius,Pressure_hPa,accelaration X (m/s^2),accelaration Y (m/s^2),accelaration Z (m/s^2),Magnetometer X (micro-Teslas),Magnetometer Y (micro-Teslas),Magnetometer Z (micro-Teslas)"+"\n")
        else:
            f.write(datetime.now().isoformat() + '\t' + c + '\n')
            #f.write(c+'\n')
        cc=str(arduinoData.readline())
        fs.write(cc+"\n")
        f.flush()
        os.fsync(f.fileno())
        
        fs.flush()
        os.fsync(fs.fileno())

        n=n+1
        print("Amostra %i de %i"%(n,m))
        #print(f"im sleeping: n={n}")
        #print(datetime.now().isoformat() + '\t' + c + '\n')
        sleep(1)#30m
arduinoData.close()