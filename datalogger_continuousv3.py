import serial
import time
import random
import numpy
import busio

import board
import adafruit_gps as gpsd

#from gps import *
uart=serial.Serial ("/dev/ttyACM1", 9600)
gps=gpsd.GPS(uart)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")


if not gps.has_fix:
    print("No fix")
    

i=0

ser=serial.Serial('/dev/ttyACM0', 9600, timeout=6)
ser.flushInput()
mat=numpy.zeros((1,8))
print(mat)

last_print = int(time.monotonic())
location=input("Enter location ")
filename = '/home/pi/datadump/data'+location+'.csv'

f = open(filename, "w+")

while True:
        try:
            # Make sure to call gps.update() every loop iteration and at least twice
            # as fast as data comes from the GPS unit (usually every second).
            # This returns a bool that's true if it parsed new data (you can ignore it
            # though if you don't care and instead look at the has_fix property).
            time.sleep(.1)
            gps.update()
            # Every second print out current location details if there's a fix.
            current = int(time.monotonic())
            if current - last_print >= 1.0:
                #Get GPS data
                last_print = current
                if not gps.has_fix:
                    # Try again if we don't have a fix yet.
                    print("Waiting for fix...")
                    continue
                # We have a fix! (gps.has_fix is true)
                # Print out details about the fix like location, date, etc.
                
                month=float(format(gps.timestamp_utc.tm_mon))
                day=float(format(gps.timestamp_utc.tm_mday))
                year=float(format(gps.timestamp_utc.tm_year))
                hour=float(format(gps.timestamp_utc.tm_hour))
                minute=float(format(gps.timestamp_utc.tm_min))
                second=float(format(gps.timestamp_utc.tm_sec))
                
                latitude=float(format(gps.latitude))
                longitude=float(format(gps.longitude))
                fix_quality=float(format(gps.fix_quality))
                # Some attributes beyond latitude, longitude and timestamp are optional
                # and might not be present.  Check if they're None before trying to use!
                if gps.satellites is not None:
                    gps_satellites=float(format(gps.satellites))
                if gps.altitude_m is not None:
                    altitude=float(format(gps.altitude_m))
                if gps.speed_knots is not None:
                    speed=float(format(gps.speed_knots))
                if gps.track_angle_deg is not None:
                    track_angle=float(format(gps.track_angle_deg))
                if gps.horizontal_dilution is not None:
                    horizontal_dilution=float(format(gps.horizontal_dilution))
                if gps.height_geoid is not None:
                    height_geoid=float(format(gps.height_geoid))
                    
                
                #Get temperature (deg_F) data   
                ser_bytes=ser.readline()
                decoded_bytes_temp=float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                
                #Get pH data            
                
                
                data=str(latitude) + "," + str(longitude) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(minute) + "," + str(second) + "," + str(decoded_bytes_temp) + ',' + str(time.monotonic())
                
                #mat=numpy.vstack((mat,numpy.atleast_2d(data).T))
                
                print(decoded_bytes_temp)
                #print(second)
                
                
                #time.sleep(1)
                
                i=i+1
                
                f.write(data + "\r\n")

                last_print = current
        except KeyboardInterrupt:
            #numpy.savetxt(filename,mat,delimiter=',')
            f.close()
            print('Done')
            quit()
            