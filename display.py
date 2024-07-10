import pygame as pg
from numpy import sin, cos, pi

WIDTH = 700
HEIGHT = 700

AXES_SCALES = (1, 2, 5)

class Display():
    def __init__(self):
        self.graphFont = pg.font.SysFont("arial", 20)
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])

        self.graphSurf = pg.Surface((600, 400))
        self.graphPoint = 50, 50
        self.graphZoom = 30
        self.graphCentre = [300, 200]


    def drawScreen(self, points):
        self.screen.fill((150, 150, 175))
        self.drawGraph(points)


        pg.display.flip()

    def drawGraph(self, points):
        # How many pixels in 1 unit measurement
        scale = 600 / self.graphZoom

        # Graphical centre
        centre = self.graphCentre
        
        self.graphSurf.fill((200, 200, 200))
        self.drawAxes(scale)

        # Drawing the curve
        for i in range(len(points) - 1):
            point1 = (centre[0] + points[i][0] * scale,
                      centre[1] - points[i][1] * scale)

            point2 = (centre[0] + points[i + 1][0] * scale,
                      centre[1] - points[i + 1][1] * scale)
            pg.draw.aaline(self.graphSurf, (0, 0, 0), point1, point2)


        # Drawing the border
        pg.draw.lines(self.graphSurf, (0, 0, 0), True, ((0, 0), (599, 0), (599, 399), (0, 399)), 5)
        self.screen.blit(self.graphSurf, self.graphPoint)

    def drawAxes(self, scale):
        centre = self.graphCentre
        axisWidth = 10

        # axisWidth = scale

        # # Drawing the axes
        pg.draw.line(self.graphSurf, (150, 150, 150), (centre[0], 0), (centre[0], 400), 3)
        pg.draw.line(self.graphSurf, (150, 150, 150), (0, centre[1]), (600, centre[1]), 3)


        i = 1
        while True:
            x = centre[0] + i * axisWidth * scale

            text = str(i * axisWidth)
            self.graphSurf.blit(self.graphFont.render(text, True, (100, 100, 100)), (x - 10 * len(text), centre[1]))

            if x > 600:
                break
            pg.draw.line(self.graphSurf, (150, 150, 150), (x, 0), (x, 400))
            i += 1
        
        i = 1
        while True:
            x = centre[0] - i * axisWidth * scale
            if x < 0:
                break
            text = str(-i * axisWidth)
            pg.draw.line(self.graphSurf, (150, 150, 150), (x, 0), (x, 400))
            i += 1

        i = 1
        while True:
            y = centre[1] + i * axisWidth * scale
            if y > 400:
                break
            text = str(i * axisWidth)
            pg.draw.line(self.graphSurf, (150, 150, 150), (0, y), (600, y))
            i += 1

        i = 1
        while True:
            y = centre[1] - i * axisWidth * scale
            if y < 0:
                break
            text = str(-i * axisWidth)
            pg.draw.line(self.graphSurf, (150, 150, 150), (0, y), (600, y))
            i += 1

