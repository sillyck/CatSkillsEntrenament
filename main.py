from socket import timeout
from time import sleep
from serial import Serial

Robot = Serial("COM4", 9600, timeout=.1)
Robot.flushOutput() # Eliminar buffer salida
Robot.flushOutput() # Eliminar buffer entrada
com = "cmd_vel[0.1,0,0]"
Robot.write(com.encode() + '\n'.encode())
getValue = Robot.readline()
print(getValue)
