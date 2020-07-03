"""
==============================================================================================================
Controleverything.com- H3LIS331DL 3-Axis Linear Accelerometer I2C Mini Module
A versatile motion-sensing system-in-a-chip
 
3-Axis Accelerometer
10,000 g High-Shock Survivability
+/-100g/+/-200g/+/-400g Dynamically Selectable Scales
5V I2C Mini Module Form-Factor
2 Devices per I2C Port
0x18 I2C Start Address

Hardware Version - Rev 0.1 (Beta)
Platform - Beaglebone
Based code in https://github.com/ControlEverythingCommunity/H3LIS331DL/blob/master/Python/H3LIS331DL.py

Initial Contributor:
Pablo Garcia Covelo - Initial contributor
pablogcovelo@gmail.com

New Contributors:
==============================================================================================================
"""
from __future__ import print_function
import smbus
import math
import collections
import sys


if sys.version_info[0] < 3:
    raise Exception("O programa foi actualizado,debe usar python3")
import configparser
import logging
import sys
import json
import time

import Adafruit_BBIO.GPIO as GPIO

sys.path.insert(0, "./handler")
from H3LIS331DL import H3LIS331DL

#print(__name__)

class Controller:
    def __init__(self):
        self.JSON = dict()
        self.ring_buffer_x = dict()
        self.ring_buffer_y = dict()
        self.ring_buffer_z = dict()

        self.magnitude = 0
        self.vibration=0
        self.gpioPorts = []
        self.conf = self.readConf()
        self.bus = smbus.SMBus(int(self.conf["smbus"]))
        self.sensitivity = int(self.conf["sensitivity"])  # This is a estimated sensitivity for the accelerometer
        self.devibrate = int(self.conf["devibrate"])  # Count to guarantee new impact detection with no interferences
        self.bufferMaxLength = int(self.conf["buffer_max_length"])
        self.acclNumber = int(self.conf["accl_number"])

        with open("spec/spec.json") as f:
            spec = json.load(f)
        self.gpioPorts.extend(spec["gpioPorts"])

        self.H3LIS331DL_obj = H3LIS331DL(self.conf, self.bus, self.gpioPorts, self.JSON,self.bufferMaxLength,
                                    self.ring_buffer_x, self.ring_buffer_y, self.ring_buffer_z)


    def readConf(self):
        # Read and load de configuration data in a dictionary
        config = configparser.ConfigParser()
        config.read("./conf/config.ini")
        H3LIS331DL_options = config.options("H3LIS331DL")
        conf = dict()
        for op in H3LIS331DL_options:
            conf[op] = config.get("H3LIS331DL", op)
        logging.debug("[CONFIGURATION]: %s", conf)
        return conf

    def generateDicts(self):
        for s in self.gpioPorts:
            self.JSON[s] = dict(axis_x=dict(values=[], times=[]),
                                axis_y=dict(values=[], times=[]),
                                axis_z=dict(values=[], times=[]))

            self.ring_buffer_x[s] = dict(values=collections.deque(maxlen=self.bufferMaxLength),
                                         times=collections.deque(maxlen=self.bufferMaxLength))
            self.ring_buffer_y[s] = dict(values=collections.deque(maxlen=self.bufferMaxLength),
                                         times=collections.deque(maxlen=self.bufferMaxLength))
            self.ring_buffer_z[s] = dict(values=collections.deque(maxlen=self.bufferMaxLength),
                                         times=collections.deque(maxlen=self.bufferMaxLength))

            for i in range(0, self.bufferMaxLength):
                self.ring_buffer_x[s]["values"].append(0)
                self.ring_buffer_x[s]["times"].append(0)
                self.ring_buffer_y[s]["values"].append(0)
                self.ring_buffer_y[s]["times"].append(0)
                self.ring_buffer_z[s]["values"].append(0)
                self.ring_buffer_z[s]["times"].append(0)

            with open("./out/" + s + ".json", "w") as jsonFile:
                json.dump(self.JSON[s], jsonFile, indent=4, sort_keys=True)
                jsonFile.close()

        logging.debug("[JSON]: %s", self.JSON)
        logging.debug("[RING_BUFFER_X]: %s", self.ring_buffer_x)
        logging.debug("[RING_BUFFER_Y]: %s", self.ring_buffer_y)
        logging.debug("[RING_BUFFER_Z]: %s", self.ring_buffer_z)

    def detectAccelerometers(self):
        # Set the GPIOs that will be used in output mode and with LOW signal (0) to initialize the accelerometer
        # and detect if is connected or not, then set HIGH signal (1) to they listen in channel 19
        for i in self.gpioPorts:
            GPIO.setup(i, GPIO.OUT)
            GPIO.setup(i, GPIO.HIGH)

        while len(self.gpioPorts) > self.acclNumber:
            for x in reversed(self.gpioPorts):
                try:
                    GPIO.setup(x, GPIO.OUT)
                    GPIO.output(x, GPIO.LOW)
                    self.H3LIS331DL_obj.initialiseAccelerometer()
                    GPIO.output(x, GPIO.HIGH)

                except Exception:
                    try:
                        GPIO.output(x, GPIO.HIGH)
                        self.gpioPorts.remove(x)
                        logging.debug("The channel 18 no have any accelerometer connected in GPIO %s", x)
                        logging.debug("The GPIO %s do not will be use again", x)
                        logging.debug("To use again this GPIO restart the program")
                    except Exception:
                        self.gpioPorts.remove(x)
                        logging.error("The %s not exist", x)
                        logging.error("The GPIO %s do not will be use again", x)
                        logging.error("To use again this GPIO restart the program")

        logging.info("Total accelerometers connected: %i", len(self.gpioPorts))
        logging.info(self.gpioPorts)

    def detectImpact(self, gpio):
        Acclx, Accly, Acclz = self.H3LIS331DL_obj.readAcclValues(gpio)

        self.magnitude = 0
        try:
            self.magnitude = math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)
        except Exception:
            logging.error("An error are ocurred during the magnitude operations")

        if self.magnitude >= self.sensitivity and self.vibration == 0:
            return True
        else:
            return False


    def probar(self):
        print("Probar existe e imprime esto")

    def main(self):
        print("Okey lets go")
        logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S")
        logging.getLogger().setLevel(logging.INFO)

        #Spec has all GPIO ports
        # Read the specification file which contain all board GPIO ports available
	#ATA AQUI CREO QUE SE PODE POnhER O INICIALIZAR,TEnhO QUE VER QUE FAI H3L1SS331DL PERO PARECE SIMPLEMENTE
	#UN CONSTRUCTOR,ASIQUE PODERIASE INICIALZIAR TAMEN SOLO

        self.detectAccelerometers()
        if not self.gpioPorts:
            logging.error("The board not have any accelerometer connected.")
            logging.error("The program will be close immediately.")
            sys.exit(0)

        self.generateDicts()  # Generate de dictionaries only for the GPIOs conected
        while True:
            error = False
        # Loop all the GPIOs ports used
            for x in self.gpioPorts:
                # Set in the selected GPIO a LOW signal (0) to set the reading accelerometer channel in the channel 18
                GPIO.output(x, GPIO.LOW)

                try:
                    self.H3LIS331DL_obj.initialiseAccelerometer()  # Set up the I2C channel 18 to start reading
                except Exception:
                    error = True
                    GPIO.output(x, GPIO.HIGH)
                    self.gpioPorts.remove(x)
                    logging.warning("The channel 18 no have any accelerometer connected in GPIO %s", x)
                    logging.warning("The GPIO %s do not will be use again", x)
                    logging.warning("To use again this GPIO restart the program")
                    logging.info("Total accelerometers connected: %i", len(self.gpioPorts))

                if not error:
                    try:
                        # Suppose when vibration is 0 we can detect new impact
                        self.vibration = self.vibration - 1
                        if self.vibration < 0:
                            self.vibration = 0

                            if self.detectImpact(x):
                                print("IMPACT DETECTED!!!!!")
                                GPIO.output(x, GPIO.HIGH)
                                final = False  # Determine when the impact data capture ends
                                while not final:
                                    for i in self.gpioPorts:
                                        final = self.H3LIS331DL_obj.captureImpact(i)
                                        if final:
                                            break
                                print("IMPACT END")
                                try:
                                    if int(input("Foi un golpe valido?\n\t1)Si\n\t2)No")) is 1:
                                        return
                                except:
                                    raise Exception("Error:Caracter invalido introducido")
                                # Set vibration equals devibrate to estimate a time to we can detect new impact
                                self.vibration = self.devibrate

                        # Set in the selected GPIO a HIGH signal (1) to reset the
                        # reading accelerometer channel to default (channel 19)
                        GPIO.output(x, GPIO.HIGH)
                    except Exception as e:
                        logging.error(e)


if __name__ == "__main__":
    #DESCOMENTlogging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)
    #DESCOMENTlogging.getLogger().setLevel(logging.INFO)
    # logging.getLogger().setrLevel(logging.WARN)
    Controller().main()

"""
########################################################################
#     Examples to convert accelerometer read values in other units     #
########################################################################
"""

"""
    # Initialising the Device.
    initialiseAccelerometer()

    while True:
    # Read our Accelerometer values
    Acclx = readAcclx()
    Accly = readAccly()
    Acclz = readAcclz()
    Atotal = AcclDataTotal()

    # Convert Accelerometer raw to g values
    Atotal = Atotal * aRes  # 49/1000
    Ax = Acclx * aRes
    Ay = Accly * aRes
    Az = Acclz * aRes

    # Convert Accelerometer values to degrees
    # AcclXangle = (math.atan2(Accly, Acclz) + 3.14) * 57.3
    # AcclYangle = (math.atan2(Acclz, Acclx) + 3.14) * 57.3
    # AcclZangle = (math.atan2(Acclx, Accly) + 3.14) * 57.3

    # If IMU is up the correct way, use these lines
    # AcclXangle = AcclXangle - 180.0
    # if AcclYangle > 90:
    #     AcclYangle = AcclYangle - 270.0
    # else:
    #     AcclYangle = AcclYangle + 90.0
    #
    # if AcclZangle > 90:
    #     AcclZangle = AcclZangle - 270.0
    # else:
    #     AcclZangle = AcclZangle + 90

    # Normalise Accelerometer raw values.
    AcclXnorm = Acclx/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)
    AcclYnorm = Accly/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)
    AcclZnorm = Acclz/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)

    # print "Accelerometer Readings:"
    # print "Accl X-Axis: ", Acclx, " Accl Y-Axis: ", Accly, " Accl Z-Axis: ", Acclz
    # print "****************************"
    # print "Atotal: ", Atotal, "g"
    # print "****************************"
    # print "AcclX Angle: ",AcclXangle," degrees"
    # print "AcclY Angle: ",AcclYangle," degrees"
    # print "AcclZ Angle: ",AcclZangle," degrees"
    # print "****************************"
    # print "AcclXnorm: ", AcclXnorm
    # print "AcclYnorm: ", AcclYnorm
    # print "AcclZnorm: ", AcclZnorm
    # print "****************************"
    # print "Ax: ", Ax ," g"
    # print "Ay: ", Ay ," g"
    # print "Az: ", Az ," g"
    # print "\n\n"
"""
