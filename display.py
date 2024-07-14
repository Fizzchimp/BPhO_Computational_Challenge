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
           

        if axisWidth >= 1:
            axisWidth = int(axisWidth)
            
        # # Drawing the axes
        pg.draw.line(self.graphSurf, (150, 150, 150), (centre[0], 0), (centre[0], G_HEIGHT), 3)
        pg.draw.line(self.graphSurf, (150, 150, 150), (0, centre[1]), (G_WIDTH, centre[1]), 3)

        
        i = 1
        while True:
            x = centre[0] + i * axisWidth * scale

            textSurf = self.graphFont.render(str(i * axisWidth), True, (100, 100, 100))
            self.graphSurf.blit(textSurf, (x - textSurf.get_size()[0] - 2, centre[1]))

            if x > G_WIDTH:
                break
            pg.draw.line(self.graphSurf, (150, 150, 150), (x, 0), (x, G_HEIGHT))
            i += 1
        
        i = 1
        while True:
            x = centre[0] - i * axisWidth * scale
            
            textSurf = self.graphFont.render(str(-i * axisWidth), True, (100, 100, 100))
            self.graphSurf.blit(textSurf, (x - textSurf.get_size()[0] - 2, centre[1]))
            
            if x < 0:
                break
            pg.draw.line(self.graphSurf, (150, 150, 150), (x, 0), (x, G_HEIGHT))
            i += 1

        i = 1
        while True:
            y = centre[1] + i * axisWidth * scale
            
            textSurf = self.graphFont.render(str(-i * axisWidth), True, (100, 100, 100))
            self.graphSurf.blit(textSurf, (centre[0] - textSurf.get_size()[0] - 3, y))
            if y > G_HEIGHT:
                break
            pg.draw.line(self.graphSurf, (150, 150, 150), (0, y), (G_WIDTH, y))
            i += 1

        i = 1
        while True:
            y = centre[1] - i * axisWidth * scale
           
            textSurf = self.graphFont.render(str(i * axisWidth), True, (100, 100, 100))
            self.graphSurf.blit(textSurf, (centre[0] - textSurf.get_size()[0] - 3, y))
            
            if y < 0:
                break
            text = str(-i * axisWidth)
            pg.draw.line(self.graphSurf, (150, 150, 150), (0, y), (G_WIDTH, y))
            i += 1
            
        self.graphSurf.blit(self.graphFont.render("0", True, (100, 100, 100)), (centre[0] - 12, centre[1]))

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