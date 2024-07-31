from numpy import pi, sin, cos, tan, sqrt, arctan, arcsin, log
import pygame as pg
pg.init()
from display import Display, G_WIDTH, G_HEIGHT, G_POINT, SUB_WIDTH, SUB_HEIGHT, SUB_POINT


class Point():
    def __init__(self, pos, label = None, colour = (70, 70, 70)):
        self.pos = pos
        self.colour = colour
        
        self.label = label

class Line():
    def __init__(self, points, label = None, colour = (100, 100, 100)):
        self.points = points
        
        self.colour = colour
        self.label = label

        self.properties = []

    def addProperties(self, *items):
        for item in items:
                self.properties.append(item)



class World():
    def __init__(self):
        self.display = Display()
        self.lines = []
        self.points = []
        self.subLines = []
    
    # Task 1/2
    def basicProj(self, initPos, initVelocity, angle):
        xVel = initVelocity * cos(angle)
        yVel = initVelocity * sin(angle)

        xAcc = 0
        yAcc = -gravity

        xDif = 0.1
        
        x = initPos[0]
        y = initPos[1]
        i = 0
        points = []
        while y >= 0:
            points.append((x, y))
            
            x += xDif
            t = (x - initPos[0]) / xVel
            y = (yVel * t)  + (0.5 * yAcc * (t ** 2)) + initPos[1]

            i += 1
    
        
        b = initVelocity * sin(angle)
        endTime = (b + sqrt((b ** 2) - (2 * -gravity * initPos[1]))) / gravity

        endPos = (initPos[0] + initVelocity * cos(angle) * endTime, 0)
        endPoint = Point(endPos, (70, 70, 100), "End")
        points.append(endPos)

        line = Line(points, "Line", (100, 70, 70))

        line.addProperties(endPoint)

        return line

    def apogee(self, initPos, initVelocity, angle):
        # Finding the apogee
        xVel = initVelocity * cos(angle)
        yVel = initVelocity * sin(angle)


        maxTime = yVel / gravity
        apogee = Point((xVel * maxTime, yVel * maxTime + 0.5 * -gravity * maxTime ** 2 + initPos[1]), (100, 70, 70), "Apogee")
        return apogee
    



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


        line1 = self.basicProj(point1, initVelocity, angle1)
        line2 = self.basicProj(point1, initVelocity, angle2)

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
        y = 0
        points = []
        while y >= -initPos[1]:
            y = ((initVelocity ** 2) / (2 * gravity)) - ((gravity * (x ** 2)) / (2 * (initVelocity) ** 2))
            points.append((x + initPos[0], y + initPos[1]))
            x += 0.1

        line = Line(points, "Bounding Parabola")
        return line


    # Task 6
    def approxDist(self, initPos, initVelocity, angle):
        y = initPos[1]
        x = initPos[0]
        dt = 0.001
        time = 0
        dist = 0
        while y >= 0:
            newX = initPos[0] + initVelocity * cos(angle) * time
            newY = initPos[1] + initVelocity * sin(angle) * time + 0.5 * -gravity * (time ** 2)
            
            dist += sqrt((newX - x) ** 2 + (newY - y) ** 2)
            time += dt
            x = newX
            y = newY

        return dist
    
    def findDistance(self, initPos, initVelocity, angle):
        b = initVelocity * sin(angle)
        endTime = (b + sqrt((b ** 2) - (2 * -gravity * initPos[1]))) / gravity
        xDisp = initPos[0] + initVelocity * cos(angle) * endTime

        sub1 = tan(angle)
        sub2 = tan(angle) - (gravity * xDisp) / (initVelocity ** 2) * (1 + tan(angle) ** 2)

        integral = lambda sub: 0.5 * log(abs(sqrt(1 + (sub) ** 2) + sub)) + 0.5 * sub * sqrt(1 + (sub ** 2))
        distance = ((initVelocity ** 2) / (gravity * (1 + tan(angle) ** 2))) * (integral(sub1) - integral(sub2))
        return distance

    # Task 7
    def timeRangeGraph(self, initPos, initVelocity, angle):
        b = initVelocity * sin(angle)
        endTime = (b + sqrt((b ** 2) - (2 * -gravity * initPos[1]))) / gravity

        points = []
        iters = 30
        for i in range(iters):
            time = i / iters * endTime
            displacement = sqrt((initVelocity ** 2) * (time ** 2) - gravity * (time ** 3) * initVelocity * sin(angle) + 0.25 * (gravity ** 2) * (time ** 4))
            points.append((time, displacement))

        return Line(points, "Range/Time", (0, 0))


    # Task 8
    def bounceProj(self, initPos, initVelocity, angle, coeffRest, iterationsLeft):
        self.lines.append(self.basicProj(initPos, initVelocity, angle))
        
        if iterationsLeft > 1:
            b = initVelocity * sin(angle)
            endTime = (b + sqrt((b ** 2) - (2 * -gravity * initPos[1]))) / gravity
            
            endPos = (initPos[0] + initVelocity * cos(angle) * endTime, 0)
            endVelY = initVelocity * sin(angle) - gravity * endTime

            newVelY = -endVelY * coeffRest
            velX = initVelocity * cos(angle)

            newVel = sqrt(newVelY ** 2 + velX ** 2)
            newAngle = arctan(newVelY / velX)

            self.bounceProj(endPos, newVel, newAngle, coeffRest, iterationsLeft - 1)


    # Task 9
    def airResistance(self, initPos, initVelocity, angle, k):
        x = initPos[0]
        y = initPos[1]
        xVel = initVelocity * cos(angle)
        yVel = initVelocity * sin(angle)
        speed = initVelocity
        xAcc = 0
        yAcc = -gravity

        time = 0
        dt = 0.1
        points = []
        while y >= 0:
            points.append((x, y))
            time += dt
            xAcc = -xVel / speed * k * (speed ** 2)
            yAcc = -gravity - yVel / speed * k * (speed ** 2)
            x += xVel * dt + 0.5 * xAcc * (dt ** 2)
            y += yVel * dt + 0.5 * yAcc * (dt **2)
            xVel += xAcc * dt
            yVel += yAcc * dt
            speed = sqrt(xVel ** 2 + yVel ** 2)

        return Line(points, "Air resistance")

    def testAirResistance(self, initPos, initVelocity, angle, k):
        points = []
        x, xVel, xAcc = initPos[0], initVelocity * cos(angle), 0
        y, yVel, yAcc = initPos[1], initVelocity * sin(angle), -gravity
        dt = 0.01
        while y >= 0:
            points.append((x, y))
            # xVel += 0.5 * xAcc * dt
            xVel += xAcc * dt
            x += xVel * dt
            # xVel += 0.5 * xAcc * dt

            # yVel += 0.5 * yAcc * dt#
            yVel += yAcc * dt
            y += yVel * dt
            # yVel += 0.5 * yAcc * dt

            speed = sqrt(xVel ** 2 + yVel ** 2)
            xAcc = -xVel * k * speed
            yAcc = -gravity - xVel * k * speed

        return Line(points, "Air resistance")



    # Program Handling
    def graphMousePos(self):
        pos = pg.mouse.get_pos()
        relPos = (pos[0] - G_POINT[0], pos[1] - G_POINT[1])
        if 0 <= relPos[0] <= G_WIDTH and 0 <= relPos[1] <= G_HEIGHT:
            return relPos
        return False

    def subMousePos(self):
        pos = pg.mouse.get_pos()
        relPos = (pos[0] - SUB_POINT[0], pos[1] - SUB_POINT[1])
        if 0 <= relPos[0] <= SUB_WIDTH and 0 <= relPos[1] <= SUB_HEIGHT:
            return relPos
        return False


    def doEvents(self):
        graphMousePos = self.graphMousePos()
        subMousePos = self.subMousePos()
        mousePos = pg.mouse.get_pos()
        gCentre = self.display.graphCentre
        subCentre = self.display.subCentre

        # PyGame input events
        for event in pg.event.get():
                if event.type == pg.QUIT: self.running = False
                
                # Scroll Wheel Input
                if event.type == pg.MOUSEWHEEL:
                    # Graph Zoom
                    if graphMousePos != False:
                        if event.y == 1:
                            difference = (graphMousePos[0] - gCentre[0], graphMousePos[1] - gCentre[1])
                            self.display.graphZoom /= 1.125
                            
                            if not (gCentre[0] - 25 < graphMousePos[0] < gCentre[0] + 25 and gCentre[1] - 25 < graphMousePos[1] < gCentre[1] + 25):
                                self.display.graphCentre = [graphMousePos[0] - difference[0] * 1.125, graphMousePos[1] - difference[1] * 1.125]
                            
                        if event.y == -1:
                            difference = (G_WIDTH // 2 - gCentre[0], G_HEIGHT // 2 - gCentre[1])
                            self.display.graphZoom *= 1.125
                            self.display.graphCentre = [G_WIDTH // 2 - difference[0] / 1.125, G_HEIGHT // 2 - difference[1] / 1.125]
                    
                    # Sub Graph Zoom
                    elif subMousePos != False:
                        if event.y == 1:
                            difference = (subMousePos[0] - subCentre[0], subMousePos[1] - subCentre[1])
                            self.display.subZoom /= 1.125
                            
                            if not (subCentre[0] - 25 < subMousePos[0] < subCentre[0] + 25 and subCentre[1] - 25 < subMousePos[1] < subCentre[1] + 25):
                                self.display.subCentre = [subMousePos[0] - difference[0] * 1.125, subMousePos[1] - difference[1] * 1.125]
                            
                        if event.y == -1:
                            difference = (SUB_WIDTH // 2 - subCentre[0], SUB_HEIGHT // 2 - subCentre[1])
                            self.display.subZoom *= 1.125
                            self.display.subCentre = [SUB_WIDTH // 2 - difference[0] / 1.125, SUB_HEIGHT // 2 - difference[1] / 1.125]

                # Mouse Button Inputs
                if event.type == pg.MOUSEBUTTONDOWN:
                    if graphMousePos != False:
                        self.mouseTracking = True
                        pg.mouse.get_rel()
                        
                    if subMousePos != False:
                        self.subMouseTracking = True
                        pg.mouse.get_rel()

                    
                    # Slider Tracking
                    for slider in self.display.sliders:
                        if slider.active:
                            slider.getTracking(mousePos)

                    # CheckBox Detection
                    for checkBox in self.display.checkBoxes:
                        checkBox.inHitbox(mousePos)

                    # TextBox Tracking
                    for textBox in self.display.textBoxes:
                        textBox.mouseClicked(event)
                    
                    # Tab Detection
                    if self.display.tabMenu.mouseClicked(event):
                        self.display.sliders[3].hidden = True
                        self.display.sliders[4].hidden = True
                        self.display.sliders[5].hidden = True
                        self.display.sliders[6].hidden = True

                        self.display.textBoxes[2].hidden = True
                        self.display.textBoxes[3].hidden = True
                        self.display.textBoxes[4].hidden = True
                        self.display.textBoxes[5].hidden = True

                        self.display.checkBoxes[3].hidden = True
                        self.display.checkBoxes[4].hidden = True
                        self.display.checkBoxes[5].hidden = True

                        if self.display.tabMenu.currentTab == 1:
                            self.display.textBoxes[2].hidden = False
                            self.display.textBoxes[3].hidden = False
                            self.display.checkBoxes[3].hidden = False
                            self.display.checkBoxes[4].hidden = False
                            self.display.checkBoxes[5].hidden = False

                        if self.display.tabMenu.currentTab == 2:
                            self.display.sliders[3].hidden = False
                            self.display.sliders[4].hidden = False
                            self.display.textBoxes[4].hidden = False
                            self.display.textBoxes[5].hidden = False

                        if self.display.tabMenu.currentTab == 3:
                            self.display.sliders[5].hidden = False
                            self.display.sliders[6].hidden = False

                if event.type == pg.MOUSEBUTTONUP:
                    self.mouseTracking = False
                    self.subMouseTracking = False
                    for slider in self.display.sliders:
                        slider.tracking = False

                # Keyboard Inputs
                if event.type == pg.KEYDOWN:
                    # Checking TextBox Inputs
                    for textBox in self.display.textBoxes:
                        if textBox.tracking:
                            textBox.keyPressed(event)
                    if event.key == pg.K_ESCAPE: self.running = False



        # Tracking the movement of the mouse
        if self.mouseTracking:
            displacement = pg.mouse.get_rel()
            self.display.graphCentre[0] += displacement[0]
            self.display.graphCentre[1] += displacement[1]
        
        elif self.subMouseTracking:
            displacement = pg.mouse.get_rel()
            self.display.subCentre[0] += displacement[0]
            self.display.subCentre[1] += displacement[1]

        # Tracking the slider movement
        for slider in self.display.sliders:
            if slider.tracking:
                slider.moveSlider(pg.mouse.get_pos()[0])


    def run(self):
        global gravity
        self.running = True
        self.mouseTracking = False
        self.subMouseTracking = False
        while self.running:

            self.lines = []
            self.points = []
            self.subLines = []
            self.subPoints = []

            if self.display.checkBoxes[1].state:
                self.display.sliders[2].value = 9.81
                self.display.sliders[2].active = False
            else:
                self.display.sliders[2].active = True
            gravity = self.display.sliders[2].value

            self.doEvents()
            angle =  self.display.sliders[0].value / 180 * pi
            velocity = self.display.sliders[1].value

            xPoint = self.display.textBoxes[0].value
            yPoint = self.display.textBoxes[1].value
            if xPoint == "" or xPoint == ".": xPoint = 0
            if yPoint == "" or xPoint == ".": yPoint = 0
            point1 = (float(xPoint), float(yPoint))

            # Bounding Parabola
            if self.display.checkBoxes[0].state: self.lines.append(self.boundParabola(point1, velocity))

            # Maximum Range
            if self.display.checkBoxes[2].state: self.lines.append(self.maxRange(point1, velocity))


            # Two Points Tab
            if self.display.tabMenu.currentTab == 1:
                xPoint = self.display.textBoxes[2].value
                yPoint = self.display.textBoxes[3].value
                if xPoint == "" or xPoint == ".": xPoint = 0
                if yPoint == "" or xPoint == ".": yPoint = 0
                point2 = (float(xPoint), float(yPoint))
                
                self.points.append(Point(point1))
                self.points.append(Point(point2))
                highBall, lowBall = self.twoPoints(point1, point2, velocity)
                if self.display.checkBoxes[4].state: self.lines.append(highBall)
                if self.display.checkBoxes[5].state: self.lines.append(lowBall)

                if self.display.checkBoxes[3].state: self.lines.append(self.minVelocity(point1, point2))
            
            # Air resistance Tab
            if self.display.tabMenu.currentTab == 2:
                dragCoeff = self.display.sliders[3].value
                airDensity = self.display.sliders[4].value

                crossArea = self.display.textBoxes[4].value
                if crossArea == "" or crossArea == ".": crossArea = 0.01
                crossArea = float(crossArea) / 10000

                mass = self.display.textBoxes[5].value
                if mass == "" or mass == ".": mass = 0
                mass = float(mass) / 1000
                if mass == 0: mass = 0.01

                k = (0.5 * dragCoeff * airDensity * crossArea) / mass
                self.lines.append(self.testAirResistance(point1, velocity, angle, k))

        
            # Bounces Tab
            if self.display.tabMenu.currentTab == 3:
                coeffRest = self.display.sliders[5].value
                bounces = self.display.sliders[6].value
                self.bounceProj(point1, velocity, angle, coeffRest, bounces)


            else:
                self.lines.append(self.basicProj(point1, velocity, angle))
                self.points.append(self.apogee(point1, velocity, angle))

            # approxDist = world.approxDist(point1, velocity, angle)
            # calcDist = world.findDistance(point1, velocity, angle)

            # self.bounceProj(point1, velocity, angle, 0.8, 4)

            self.subLines.append(self.timeRangeGraph(point1, velocity, angle))
            
            self.display.drawScreen(self.lines, self.points, self.graphMousePos(), self.subLines)

world = World()

# world.points.append(point1)
# world.points.append(point2)

# line1, line2 = world.twoPoints(point1, point2, 20)
# world.lines.append(line1)
# world.lines.append(line2)

# minVel = world.minVelocity(point1, point2)[0]
# world.lines.append(minVel)

world.run()