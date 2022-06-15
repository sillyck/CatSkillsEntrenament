from socket import timeout
from serial import Serial
from threading import Thread, Timer
from math import pow
import time

class Minairo():
    """Minairo 1.0 - Requereix numero de port"""
    def __init__(self, n):
        self.pullingTime = 0.1  #Tiempo de ciclo para adquisición de datos con el Robot
        self.thread_runs = True
        
        self.X = 0.0    # Velocidad en m/s
        self.Y = 0.0    # Velocidad en m/s
        self.W = 0.0    # Velocidad en rad/s
        self.SensorLine_Analog = [0,0,0,0,0,0,0,0]
        self.SensorLine_Digital = [False,False,False,False,False,False,False,False]
        self.SensorLine_Threshold = 1000
        self.SensorSharp = [0,0,0,0]
        self.port = "COM" + str(n)
        ## Configuració de la instància de Port Sèrie
        self.Robot = Serial(self.port,115200,timeout=.1)
        self.Robot.flushOutput() ## Buidar el buffer de sortida del port
        self.Robot.flushInput() ## Buidar el buffer d'entrda del port
        print (f"Minairo 1.0 en puerto:{self.port} conectado")
        

    def start(self):
        self.transmit()

    def close(self):
        self.thread_runs = False
        print (f"Minairo 1.0 en puerto:{self.port} desconectado")
        pass

    def run(self):
        while self.thread_runs:
            self.transmit()
            time.sleep(self.pullingTime)

    def transmit(self):
        #self.Robot.flushOutput() ## Buidar el buffer de sortida del port
        #self.Robot.flushInput() ## Buidar el buffer d'entrda del port
        #self.transmit = TRUE
        self.Robot.flushInput() ## Buidar el buffer d'entrda del port
        comanda = f"cmd_vel[{self.X},{self.Y},{self.W}]"
        self.Robot.write(bytes(comanda, 'utf-8') + b'\n')
        getValue = self.Robot.readline()
        data = getValue.decode('utf-8', errors='replace')
        comanda = f"getSensors"
        self.Robot.write(bytes(comanda, 'utf-8') + b'\n')
        getValue = self.Robot.readline()
        data = getValue.decode('utf-8', errors='replace')
        characters = "\r\n"
        for x in range(len(characters)):
            data = data.replace(characters[x],"")

        
        output=data.split(',')
        for x in range(0,8):
            self.SensorLine_Analog[x] = int(output[x])
            if self.SensorLine_Analog[x]>=self.SensorLine_Threshold:
                self.SensorLine_Digital[x] = True
            else:
                self.SensorLine_Digital[x] = False
        
        for x in range(0,4):
            self.SensorSharp[x] = int(32120*((1+int(output[x+8]))**(-1.238)))
            if self.SensorSharp[x] > 400:
                self.SensorSharp[x] = 400
        
        print(self.SensorSharp)
        if self.thread_runs:
            Timer(self.pullingTime, self.transmit).start()
        


    def setX(self,x):
        self.X = x

    def setY(self,y):
        self.Y = y

    def setW(self,w):
        self.W = w

    def setSensorLine_Threshold(self,x):
        self.SensorLine_Threshold = x

    def getSensorLine_Threshold(self):
        return self.SensorLine_Threshold

    def getSensorLine_Analog(self):
        return self.SensorLine_Analog

    def getSensorLine_Digital(self):
        return self.SensorLine_Digital

    def getSensorSharp(self):
        return self.SensorSharp
    
    def setPullingTime(self,x):
        self.pullingTime = x

    def getPullingTime(self):
        return self.pullingTime
