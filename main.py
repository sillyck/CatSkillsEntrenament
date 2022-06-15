from serial import Serial

Robot = Serial("COM4", 115200, timeout=.1)
Robot.flushInput() # Eliminar buffer salida
Robot.flushOutput() # Eliminar buffer entrada

endavant = "cmd_vel[0.1,0,0]"
endarrere = "cmd_vel[0.1,0,0]"
dreta = "cmd_vel[0.1,0,0]"
esquerra = "cmd_vel[0.1,0,0]"

Robot.write(endavant.encode() + '\n'.encode())
getValue = Robot.readline()
print(getValue)
