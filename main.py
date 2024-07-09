import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from numpy import pi, sin, cos

dt = 0.001

# velocity = int(input("Enter start velocity\n: "))
# angle = int(input("\n\nEnter angle\n: ")) / 180 * pi
# height = int(input("\n\nEnter starting height\n: "))
# gravity = int(input("\n\nEnter gravity\n: "))

velocity = 10
angle = 45 / 180 * pi
height = 10
gravity = 10

x = 0
y = height

xVel = velocity * cos(angle)
yVel = velocity * sin(angle)

xAcc = 0
yAcc = -gravity

yPoints = []
xPoints = []

xDif = 0.0001
i = 0
while y >= 0:
    x = i * xDif
    t = x / xVel
    
    y = yVel * t + 0.5 * yAcc * t * t + height

    xPoints.append(x)
    yPoints.append(y)

    i += 1
    

# Finding the apogee
maxTime = -yVel / yAcc
apogee = (xVel * maxTime + 0.5 * xAcc * maxTime ** 2, yVel * maxTime + 0.5 * yAcc * maxTime ** 2 + height)


plt.plot(xPoints, yPoints)
plt.plot(apogee[0], apogee[1], "ro")
plt.show()