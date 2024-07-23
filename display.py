import pygame as pg
from numpy import sin, cos, pi, log10

WIDTH = 1100
HEIGHT = 700

G_WIDTH = 650
G_HEIGHT = 650

G_POINT = (25, 25)

AXES_SCALES = (1, 2, 5)

SLIDER_FONT = pg.font.SysFont("arial", 17)

class Display():
    def __init__(self):
        self.graphFont = pg.font.SysFont("arial", 17)
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])

        self.graphSurf = pg.Surface((G_WIDTH, G_HEIGHT))
        self.graphPoint = G_POINT
        self.graphZoom = 30
        self.graphCentre = [G_WIDTH / 6, 5 * G_HEIGHT / 6]
        
        self.sliders = [Slider(700, 1075, 100, 45, 90, 0.5, "Angle: ___°"),
                        Slider(700, 1075, 150, 10, 200, 1, "Velocity:  ___m/s")]
        
        self.checkBoxes = [CheckBox((700, 200), "CheckBox")]


    def drawScreen(self, lines, points):
        self.screen.fill((150, 150, 175))
        self.drawGraph(lines, points)
        
        for slider in self.sliders:
            slider.draw(self.screen)

        for checkBox in self.checkBoxes:
            checkBox.draw(self.screen)


        pg.display.flip()

    def drawGraph(self, lines, points):
        # How many pixels in 1 unit measurement
        scale = G_WIDTH / self.graphZoom

        # Graphical centre
        centre = self.graphCentre
        
        self.graphSurf.fill((200, 200, 200))
        self.drawAxes(scale)

        # Drawing any lines
        for l_points in lines:
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
        self.screen.blit(self.graphSurf, self.graphPoint)

    def drawAxes(self, scale):
        centre = self.graphCentre
        
        exponent = log10(self.graphZoom) // 1
        mantissa = self.graphZoom / (10 ** exponent)
        

        if 2.5 < mantissa < 5:
            axisWidth = 5 * (10 ** (exponent - 1))
        
        elif 1 < mantissa <= 2.5:
            axisWidth = 2 * (10 ** (exponent - 1))
            
        elif 5 < mantissa:
            axisWidth = 1 * (10 ** exponent)
        
            
        # Drawing the axes
        if centre[0] < G_WIDTH: pg.draw.line(self.graphSurf, (150, 150, 150), (centre[0], 0), (centre[0], G_HEIGHT), 3)
        if centre[1] < G_HEIGHT: pg.draw.line(self.graphSurf, (150, 150, 150), (0, centre[1]), (G_WIDTH, centre[1]), 3)

        axScale = axisWidth * scale
        
        axisBefore = (-centre[0] // axScale + 1, centre[1] // axScale + 1)
        centreOffset = (centre[0] % axScale, centre[1] % axScale)

        if axisWidth >= 1: textType = True
        else: textType = False

        # Draw grid
        for i in range(int(G_WIDTH // axScale) + 2):
            x = centreOffset[0] + axScale * i

            text = axisWidth * (axisBefore[0] + i)
            if textType: text = int(text)

            textSurf = self.graphFont.render(str(text), True, (100, 100, 100))
            dims = textSurf.get_size()

            if centre[1] < 4: self.graphSurf.blit(textSurf, (x - dims[0] - 2, 4))
            if 4 < centre[1] < G_HEIGHT - dims[1] - 4: self.graphSurf.blit(textSurf, (x - dims[0] - 2, centre[1]))
            if G_HEIGHT - dims[1] - 4 < centre[1]: self.graphSurf.blit(textSurf, (x - dims[0] - 2, G_HEIGHT - dims[1] - 4))

            pg.draw.line(self.graphSurf, (150, 150, 150), (x, 0), (x, G_HEIGHT))
        
        
        for i in range(int(G_HEIGHT // axScale) + 2):
            y = centreOffset[1] + axScale * (i - 1)

            text = axisWidth * (axisBefore[1] - i)
            if textType: text = int(text)

            textSurf = self.graphFont.render(str(text), True, (100, 100, 100))
            dims = textSurf.get_size()

            if centre[0] < dims[0] + 8: self.graphSurf.blit(textSurf, (6, y))
            if dims[0] + 8 < centre[0] < G_WIDTH - 4: self.graphSurf.blit(textSurf, (centre[0] - dims[0] - 2, y))
            if G_WIDTH - 4 < centre[0]: self.graphSurf.blit(textSurf, (G_WIDTH - dims[0] - 6, y))

            pg.draw.line(self.graphSurf, (150, 150, 150), (0, y), (G_WIDTH, y))
            

class Slider():
    def __init__(self, xPos1, xPos2, yPos, initVal, valRange, step, label):
        
        self.xPos1 = xPos1
        self.xPos2 = xPos2
        self.yPos = yPos
        self.length = xPos2 - xPos1
        
        self.range = valRange
        self.step = step
        self.value = initVal
        
        self.tracking = False
        
        self.label = label

    def draw(self, surface):
        pg.draw.line(surface, (100, 100, 120), (self.xPos1, self.yPos), (self.xPos2, self.yPos), 5)
        pg.draw.circle(surface, (90, 70, 90), (self.xPos1 + self.value / self.range * self.length, self.yPos), 7)
        
        labelSurf = SLIDER_FONT.render(self.label.replace("___", str(self.value)), True, (50, 50, 60))
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
    def __init__(self, pos, label, startState = False):
        self.label = label
        self.pos = pos
        self.state = startState

    def draw(self, surface):
        pg.draw.rect(surface, (100, 100, 100), pg.Rect(self.pos[0] - 7, self.pos[1] - 7, 14, 14))
        if not self.state:
            pg.draw.rect(surface, (200, 200, 200), pg.Rect(self.pos[0] - 6, self.pos[1] - 6, 12, 12))
            

    def inHitbox(self, mousePos):
        if self.pos[0] - 7 <= mousePos[0] <= self.pos[0] + 7 and self.pos[1] - 7 <= mousePos[1] <= self.pos[1] + 7:
                if self.state: self.state = False
                else: self.state = True