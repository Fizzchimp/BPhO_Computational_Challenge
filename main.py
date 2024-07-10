from numpy import pi, sin, cos
import pygame as pg
from display import Display

class World():
    def __init__(self):
        pg.init()
        self.display = Display()

    def basicProj(self):

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

        self.points = []

        xDif = 0.01
        i = 0
        while y >= 0:
            x = i * xDif
            t = x / xVel
            
            y = yVel * t + 0.5 * yAcc * t * t + height

            self.points.append((x, y))

            i += 1
    

        # Finding the apogee
        maxTime = -yVel / yAcc
        self.apogee = (xVel * maxTime + 0.5 * xAcc * maxTime ** 2, yVel * maxTime + 0.5 * yAcc * maxTime ** 2 + height)


    def doEvents(self):
        for event in pg.event.get():
                if event.type == pg.QUIT: self.running = False
                 
                # Scroll Wheel Input
                if event.type == pg.MOUSEWHEEL:
                    if event.y == 1:
                        self.display.graphZoom /= 1.5
                    if event.y == -1:
                        self.display.graphZoom *= 1.5

                # Mouse Button Inputs
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouseTracking = True
                    pg.mouse.get_rel()
                if event.type == pg.MOUSEBUTTONUP: self.mouseTracking = False

                # Keyboard Inputs
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE: self.running = False


        if self.mouseTracking:
            displacement = pg.mouse.get_rel()
            self.display.graphCentre[0] += displacement[0]
            self.display.graphCentre[1] += displacement[1]

    def run(self):
        self.running = True
        self.mouseTracking = False
        while self.running:
            
            self.doEvents()
            self.display.drawScreen(self.points)

world = World()
# world.basicProj()

world.points = []
for i in range(720):
    world.points.append((i / 180 * pi, sin(i / 180 * pi)))

world.run()