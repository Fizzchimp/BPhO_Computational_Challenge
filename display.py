import pygame as pg
from numpy import sin, cos, pi, log10

WIDTH = 1100
HEIGHT = 700

G_WIDTH = 650
G_HEIGHT = 650

G_POINT = (25, 25)

AXES_SCALES = (1, 2, 5)

class Display():
    def __init__(self):
        self.graphFont = pg.font.SysFont("arial", 17)
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])

        self.graphSurf = pg.Surface((G_WIDTH, G_HEIGHT))
        self.graphPoint = G_POINT
        self.graphZoom = 30
        self.graphCentre = [G_WIDTH / 6, 5 * G_HEIGHT / 6]


    def drawScreen(self, lines, points):
        self.screen.fill((150, 150, 175))
        self.drawGraph(lines, points)


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
    def __init__(self, point1, point2, initVal, range):
        
        self.point1
        self.point2
        
        self.lineVect = (point1[0] - point2[0], point1[1] - point2[1])
        
        self.val = initVal
        self.range = range
        
    #def getPos(self, mousePos):
        
        
    def draw(self, surface):
        percentageAlong = self.val / self.range
        pg.draw.line(surface, (150, 150, 150), self.point1, self.point2, 5)
        pg.draw.circle(surface, (50, 50, 50), (self.point1[0] + self.lineVect[0] * percentageAlong, self.point1[1] + self.lineVect[1] * percentageAlong))