import pygame as pg
from numpy import round, log10

WIDTH = 1100
HEIGHT = 700

G_WIDTH = 620
G_HEIGHT = 620

SUB_WIDTH = 250
SUB_HEIGHT = 150

G_POINT = (25, 25)
SUB_POINT = (WIDTH - SUB_WIDTH - 25, HEIGHT - SUB_HEIGHT - 50)

AXES_SCALES = (1, 2, 5)

SCREEN_FONT = pg.font.SysFont("arial", 17)

UI_FONT = pg.font.SysFont("arial", 17)

class Display():
    def __init__(self):
        self.graphFont = pg.font.SysFont("arial", 17)
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption("Projectile Motion")

        # Main Graph Properties
        self.graphSurf = pg.Surface((G_WIDTH, G_HEIGHT))
        self.graphZoom = 30
        self.graphCentre = [G_WIDTH / 6, 5 * G_HEIGHT / 6]
        
        # Sub Graph Properties
        self.subGraphSurf = pg.Surface((SUB_WIDTH, SUB_HEIGHT))
        self.subZoom = 30
        self.subCentre = [25, SUB_HEIGHT - 25]

    
        self.sliders = [Slider(700, 1075, 100, 45, 90, 0.5, "Angle: ___°"),
                        Slider(700, 1075, 150, 10, 50, 0.0625, "Velocity:  ___m/s"),
                        Slider(700, 1075, 200, 9.81, 20, 0.0625, "Gravity:  ___N/Kg")]
        
        self.checkBoxes = [CheckBox((710, 300), "Bounding Parabola"),
                           CheckBox((900, 300), "Earth Gravity", True)]


    def drawScreen(self, lines, points, relMousePos, subLines):
        self.screen.fill((150, 150, 175))
        self.drawGraph(lines, points)
        self.drawSubGraph(subLines, None)
        
        # Draw all sliders
        for slider in self.sliders:
            slider.draw(self.screen)

        # Draw all checkboxes
        for checkBox in self.checkBoxes:
            checkBox.draw(self.screen)

        # Displaying the coordinates of the mouse on screen
        if relMousePos != False:
            pixScale = self.graphZoom / G_WIDTH
            roundVal = int(log10(1 / self.graphZoom)) + 2

            gMousePos = (round((relMousePos[0] - self.graphCentre[0]) * pixScale, roundVal),
                         round((self.graphCentre[1] - relMousePos[1]) * pixScale, roundVal))
            
            if roundVal <= 0:
                gMousePos = (int(gMousePos[0]), int(gMousePos[1]))

            self.screen.blit(SCREEN_FONT.render(f"{str(gMousePos[0])}, {str(gMousePos[1])}", True, (50, 50, 60)), (G_POINT[0] + 5, G_POINT[1] + G_HEIGHT + 5))
        
        pg.display.flip()

    def drawAxes(self, scale, width, height, centre, surface):

        zoom = width / scale
        exponent = log10(zoom) // 1
        mantissa = zoom / (10 ** exponent)
        

        if 2.5 < mantissa < 5:
            axisWidth = 5 * (10 ** (exponent - 1))
        
        elif 1 < mantissa <= 2.5:
            axisWidth = 2 * (10 ** (exponent - 1))
            
        elif 5 < mantissa:
            axisWidth = 1 * (10 ** exponent)
        
            
        # Drawing the axes
        if centre[0] < width: pg.draw.line(surface, (150, 150, 150), (centre[0], 0), (centre[0], height), 3)
        if centre[1] < height: pg.draw.line(surface, (150, 150, 150), (0, centre[1]), (width, centre[1]), 3)

        axScale = axisWidth * scale
        
        axisBefore = (-centre[0] // axScale + 1, centre[1] // axScale + 1)
        centreOffset = (centre[0] % axScale, centre[1] % axScale)

        if axisWidth >= 1: textType = True
        else: textType = False

        # Draw grid
        for i in range(int(width // axScale) + 2):
            x = centreOffset[0] + axScale * i

            text = axisWidth * (axisBefore[0] + i)
            if textType: text = int(text)

            textSurf = self.graphFont.render(str(text), True, (100, 100, 100))
            dims = textSurf.get_size()

            if centre[1] < 4: surface.blit(textSurf, (x - dims[0] - 2, 4))
            if 4 < centre[1] < height - dims[1] - 4: surface.blit(textSurf, (x - dims[0] - 2, centre[1]))
            if height - dims[1] - 4 < centre[1]: surface.blit(textSurf, (x - dims[0] - 2, height - dims[1] - 4))

            pg.draw.line(surface, (150, 150, 150), (x, 0), (x, height))
        
        
        for i in range(int(height // axScale) + 2):
            y = centreOffset[1] + axScale * (i - 1)

            text = axisWidth * (axisBefore[1] - i)
            if textType: text = int(text)

            textSurf = self.graphFont.render(str(text), True, (100, 100, 100))
            dims = textSurf.get_size()

            if centre[0] < dims[0] + 8: surface.blit(textSurf, (6, y))
            if dims[0] + 8 < centre[0] < width - 4: surface.blit(textSurf, (centre[0] - dims[0] - 2, y))
            if width - 4 < centre[0]: surface.blit(textSurf, (width - dims[0] - 6, y))

            pg.draw.line(surface, (150, 150, 150), (0, y), (width, y))

    def drawGraph(self, lines, points):
        # How many pixels in 1 unit measurement
        scale = G_WIDTH / self.graphZoom

        # Graphical centre
        centre = self.graphCentre
        
        self.graphSurf.fill((200, 200, 200))
        self.drawAxes(scale, G_WIDTH, G_HEIGHT, centre, self.graphSurf)

        # Drawing any lines
        for line in lines:
            l_points = line.points
            for i in range(len(l_points) - 1):
                point1 = (centre[0] + l_points[i][0] * scale,
                        centre[1] - l_points[i][1] * scale)

                point2 = (centre[0] + l_points[i + 1][0] * scale,
                          centre[1] - l_points[i + 1][1] * scale)
                pg.draw.aaline(self.graphSurf, (0, 0, 0), point1, point2)

        # Drawing any points
        for point in points:
            pg.draw.circle(self.graphSurf, (200, 75, 75), (centre[0] + point[0] * scale, centre[1] - point[1] * scale), 5)
            
        # Drawing the border
        pg.draw.lines(self.graphSurf, (0, 0, 0), True, ((0, 0), (G_WIDTH - 1, 0), (G_WIDTH - 1, G_HEIGHT - 1), (0, G_HEIGHT - 1)), 5)
        self.screen.blit(self.graphSurf, G_POINT)


    def drawSubGraph(self, lines, points):
        scale = SUB_WIDTH / self.subZoom
        centre = self.subCentre
        self.subGraphSurf.fill((200, 200, 200))
        self.drawAxes(scale, SUB_WIDTH, SUB_HEIGHT, centre, self.subGraphSurf)


        for line in lines:
            l_points = line.points
            for i in range(len(l_points) - 1):
                point1 = (centre[0] + l_points[i][0] * scale,
                        centre[1] - l_points[i][1] * scale)

                point2 = (centre[0] + l_points[i + 1][0] * scale,
                          centre[1] - l_points[i + 1][1] * scale)
                pg.draw.aaline(self.subGraphSurf, (0, 0, 0), point1, point2)


        # Drawing the border
        pg.draw.lines(self.subGraphSurf, (0, 0, 0), True, ((0, 0), (SUB_WIDTH - 1, 0), (SUB_WIDTH - 1, SUB_HEIGHT - 1), (0, SUB_HEIGHT - 1)), 5)
        self.screen.blit(self.subGraphSurf, SUB_POINT)



class Slider():
    def __init__(self, xPos1, xPos2, yPos, initVal, valRange, step, label, active = True):
        
        self.xPos1 = xPos1
        self.xPos2 = xPos2
        self.yPos = yPos
        self.length = xPos2 - xPos1
        
        self.range = valRange
        self.step = step
        self.value = initVal
        
        self.tracking = False
        
        self.label = label

        self.active = active

    def draw(self, surface):
        if self.active:
            lineColour = (100, 100, 120)
            circColour = (90, 70, 90)
            fontColour = (50, 50, 60)
        else:
            lineColour = (130, 130, 150)
            circColour = (110, 110, 130)
            fontColour = (100, 100, 120)
        pg.draw.line(surface, lineColour, (self.xPos1, self.yPos), (self.xPos2, self.yPos), 5)
        pg.draw.circle(surface, circColour, (self.xPos1 + self.value / self.range * self.length, self.yPos), 7)
        
        labelSurf = UI_FONT.render(self.label.replace("___", str(self.value)), True, fontColour)
        surface.blit(labelSurf, (self.xPos1, self.yPos - 25))
    
    def moveSlider(self, mousePos):
        if self.xPos1 <= mousePos <= self.xPos2:
            self.value = ((mousePos - self.xPos1) / self.length * self.range)
            self.value = self.value - (self.value % self.step)
            if self.value % 1 == 0:
                self.value = int(self.value)
            
        if mousePos < self.xPos1:
            self.value = 0
            
        if self.xPos2 < mousePos:
            self.value = self.range

    def getTracking(self, mousePos):
        if self.xPos1 - 7 <= mousePos[0] <= self.xPos2 + 7 and self.yPos - 7 <= mousePos[1] <= self.yPos + 7:
            self.tracking = True



class CheckBox():
    def __init__(self, pos, label, startState = False, active = True):
        self.label = label
        self.pos = pos

        self.state = startState
        self.active = active

    def draw(self, surface):
        pg.draw.rect(surface, (100, 100, 100), pg.Rect(self.pos[0] - 7, self.pos[1] - 7, 14, 14))
        pg.draw.rect(surface, (200, 200, 200), pg.Rect(self.pos[0] - 5, self.pos[1] - 5, 10, 10))
        if self.state:
            pg.draw.rect(surface, (70, 70, 70), pg.Rect(self.pos[0] - 4, self.pos[1] - 4, 8, 8))
            
        
        labelSurf = UI_FONT.render(self.label, True, (50, 50, 60))
        surface.blit(labelSurf, (self.pos[0] + 12, self.pos[1] - 10))
            

    def inHitbox(self, mousePos):
        if self.pos[0] - 7 <= mousePos[0] <= self.pos[0] + 7 and self.pos[1] - 7 <= mousePos[1] <= self.pos[1] + 7:
                if self.state: self.state = False
                else: self.state = True