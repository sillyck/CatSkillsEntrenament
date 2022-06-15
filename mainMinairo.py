### CatSkills Jordi Ribellas i Eloy Altozano ###

# Imports
from Minairo2 import *

# Variables
port = 4

Robot = Minairo(port)
Robot.start()
Robot.setX(0.1)

time.sleep(1)

Robot.setX(0)

print(Robot.getSensorLine_Analog())
print(Robot.getSensorSharp())

Robot.close()
