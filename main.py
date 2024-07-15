from numpy import pi, sin, cos, sqrt, arctan, arcsin, log
import pygame as pg
from display import Display, G_WIDTH, G_HEIGHT, G_POINT

gravity = 9.81
class World():
    def __init__(self):
        pg.init()
        self.display = Display()
        self.lines = []
        self.points = []
    # Task 1/2
    def basicProj(self, initPos, initVelocity, angle):

        xVel = initVelocity * cos(angle)
        yVel = initVelocity * sin(angle)

        xAcc = 0
        yAcc = -gravity

        xDif = 0.1
        
        x = initPos[0]
        y = 0
        i = 0
        points = []
        while y >= 0:
            x += xDif
            t = (x - initPos[0]) / xVel
            y = (yVel * t)  + (0.5 * yAcc * (t ** 2)) + initPos[1]

            points.append((x, y))

            i += 1
    

        # Finding the apogee
        maxTime = -yVel / yAcc
        apogee = (xVel * maxTime + 0.5 * xAcc * maxTime ** 2, yVel * maxTime + 0.5 * yAcc * maxTime ** 2 + initPos[1])

        return points, apogee


    # Task 3
    def twoPoints(self, point1, point2, initVelocity):
        xDisp = point2[0] - point1[0]
        yDisp = point2[1] - point1[1]

        a = (gravity * (xDisp ** 2)) / (2 * (initVelocity ** 2))
        b = -xDisp
        c = (gravity * (xDisp ** 2)) / (2 * initVelocity ** 2) + yDisp
        
        z1 = (-b + sqrt((b ** 2) - (4 * a * c))) / (2 * a)
        z2 = (-b - sqrt((b ** 2) - (4 * a * c))) / (2 * a)

        angle1 = arctan(z1)
        angle2 = arctan(z2)

        self.points.append(point1)
        self.points.append(point2)

        line1, apogee1 = self.basicProj(point1, initVelocity, angle1)
        line2, apogee2 = self.basicProj(point1, initVelocity, angle2)

        return line1, line2

    def minVelocity(self, point1, point2):
        xDisp = point2[0] - point1[0]
        yDisp = point2[1] - point1[1]

        tangle = (yDisp + sqrt((xDisp ** 2) + (yDisp ** 2))) / xDisp
        angle = arctan(tangle)

        velocity = sqrt(gravity * xDisp * tangle)

        return self.basicProj(point1, velocity, angle)


    # Task 4
    def maxRange(self, initPos, initVelocity):
        yDisp = -initPos[1]
        angle = arcsin(1 / (sqrt(2 + ((2 * gravity * -yDisp) / (initVelocity ** 2)))))
        return self.basicProj(initPos, initVelocity, angle)
    

    # Task 5
    def boundParabola(self, initPos, initVelocity):
        x = 0
        points = []
        while True:
            y = ((initVelocity ** 2) / (2 * gravity)) - ((gravity * (x ** 2)) / (2 * (initVelocity) ** 2))
            points.append((x + initPos[0], y + initPos[1]))
            if y < 0:
                break
            x += 0.1

        return points


    # Task 6
    def findDistance(self, initPos, initVelocity, angle):
        pass


    # Game Handling
    def mousePos(self):
        pos = pg.mouse.get_pos()
        relPos = (pos[0] - G_POINT[0], pos[1] - G_POINT[1])
        if 0 <= relPos[0] <= G_WIDTH and 0 <= relPos[1] <= G_HEIGHT:
            return  relPos
        else: return False
        
    def doEvents(self):
        mousePos = self.mousePos()
        for event in pg.event.get():
                if event.type == pg.QUIT: self.running = False
                 
                # Scroll Wheel Input
                if event.type == pg.MOUSEWHEEL and mousePos != False:
                    if event.y == 1:
                        difference = (mousePos[0] - self.display.graphCentre[0], mousePos[1] - self.display.graphCentre[1])
                        self.display.graphZoom /= 1.125
                        self.display.graphCentre = [mousePos[0] - difference[0] * 1.125, mousePos[1] - difference[1] * 1.125]
                        
                    if event.y == -1:
                        difference = (G_WIDTH // 2 - self.display.graphCentre[0], G_HEIGHT // 2 - self.display.graphCentre[1])
                        self.display.graphZoom *= 1.125
                        self.display.graphCentre = [G_WIDTH // 2 - difference[0] / 1.125, G_HEIGHT // 2 - difference[1] / 1.125]

                # Mouse Button Inputs
                if event.type == pg.MOUSEBUTTONDOWN and mousePos != False:
                    self.mouseTracking = True
                    pg.mouse.get_rel()
                if event.type == pg.MOUSEBUTTONUP: self.mouseTracking = False

                # Keyboard Inputs
                if event.type == pg.KEYDOWN:
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
            self.display.drawScreen(self.lines, self.points)

world = World()

point1 = (0, 0)
point2 = (10, 10)

line = world.basicProj(point1, 10, 45 / 180 * pi)[0]
world.lines.append(line)

boundParabola = world.boundParabola(point1, 10)
world.lines.append(boundParabola)
world.points.append(point1)
world.points.append(point2)

line1, line2 = world.twoPoints(point1, point2, 20)
world.lines.append(line1)
world.lines.append(line2)

minVel = world.minVelocity(point1, point2)[0]
world.lines.append(minVel)

world.run()