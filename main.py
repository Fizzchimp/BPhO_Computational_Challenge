import matplotlib.pyplot as plt
from numpy import pi, sin, cos

dt = 0.001

# velocity = int(input("Enter start velocity\n: "))
# angle = int(input("\n\nEnter angle\n: ")) / 180 * pi
# height = int(input("\n\nEnter starting height\n: "))
# gravity = int(input("\n\nEnter gravity\n: "))

velocity = 10
angle = 1 / 180 * pi
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

while y >= 0:
    x += xVel * dt
    y += yVel * dt

    xVel += xAcc * dt
    yVel += yAcc * dt

    xPoints.append(x)
    yPoints.append(y)
    print(y)

    
plt.plot(xPoints, yPoints)
plt.show()