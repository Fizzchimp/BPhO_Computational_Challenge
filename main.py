from numpy import pi, sin, cos, tan, sqrt, arctan, arcsin, log
import pygame as pg
pg.init()
from display import Display, G_WIDTH, G_HEIGHT, G_POINT, SUB_WIDTH, SUB_HEIGHT, SUB_POINT


class Point():
    def __init__(self, pos, colour, label):
        self.pos = pos
        self.colour = colour
        
        self.label = label

class Line():
    def __init__(self, points, label, initPos = None, endPos = None, apogee = None):
        self.points = points
        
        self.startPoint = initPos
        self.endPoint = endPos
        
        self.apogee = apogee



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
    

        # Finding the apogee
        maxTime = -yVel / yAcc
        apogee = Point((xVel * maxTime + 0.5 * xAcc * maxTime ** 2, yVel * maxTime + 0.5 * yAcc * maxTime ** 2 + initPos[1]), (100, 70, 70), "Apogee")
        
        startPoint = Point(initPos, (70, 70, 100), "Start")
        
        b = initVelocity * sin(angle)
        endTime = (b + sqrt((b ** 2) - (2 * -gravity * initPos[1]))) / gravity

        endPos = (initPos[0] + initVelocity * cos(angle) * endTime, 0)
        endPoint = Point(endPos, (70, 70, 100), "end")
        points.append(endPos)
        
        return Line(points, "Line", startPoint, endPoint, apogee)

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
    def bounceProj(self, initPos, initVelocity, angle):
        pass

    
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
                        
                    elif subMousePos != False:
                        self.subMouseTracking = True
                        pg.mouse.get_rel()

                    else:
                        # Slider Tracking
                        for slider in self.display.sliders:
                            if slider.active:
                                slider.getTracking(mousePos)

                        # CheckBox Detection
                        for checkBox in self.display.checkBoxes:
                            checkBox.inHitbox(mousePos)

                if event.type == pg.MOUSEBUTTONUP:
                    self.mouseTracking = False
                    self.subMouseTracking = False
                    for slider in self.display.sliders:
                        slider.tracking = False

                # Keyboard Inputs
                if event.type == pg.KEYDOWN:
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
            point1 = (0, 10)

            if self.display.checkBoxes[0].state:
                boundParabola = world.boundParabola(point1, velocity)
                world.lines.append(boundParabola)
            

            line = self.basicProj(point1, velocity, angle)
            # approxDist = world.approxDist(point1, velocity, angle)
            calcDist = world.findDistance(point1, velocity, angle)

            self.subLines.append(self.timeRangeGraph(point1, velocity, angle))
            self.lines.append(line)
            
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