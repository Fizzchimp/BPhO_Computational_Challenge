import pygame as pg
from numpy import sin, pi, log2

WIDTH = 700
HEIGHT = 700

class Display():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])

        self.graphSurf = pg.Surface((600, 400))
        self.graphPoint = 50, 50
        self.graphZoom = 20
        self.graphCentre = [300, 200]


    def drawScreen(self, points):
        self.screen.fill((150, 150, 175))
        self.drawGraph(points)


        pg.display.flip()

    def drawGraph(self, points):
        # Set the scale of 1 pixel
        scale = 600 / self.graphZoom
        centre = self.graphCentre
        axisWidth = scale


        # Drawing the axes
        self.graphSurf.fill((200, 200, 200))
        pg.draw.line(self.graphSurf, (150, 150, 150), (centre[0], 0), (centre[0], 400), 3)
        pg.draw.line(self.graphSurf, (150, 150, 150), (0, centre[1]), (600, centre[1]), 3)

        offset = (centre[0] % axisWidth, centre[1] % axisWidth)
        i = 0
        while i * axisWidth <= 600:
            pg.draw.line(self.graphSurf, (150, 150, 150), (offset[0] + i * axisWidth, 0), (offset[0] + i * axisWidth, 400))
            i += 1

        i = 0
        while i * axisWidth <= 400:
            pg.draw.line(self.graphSurf, (150, 150, 150), (0, offset[1] + i * axisWidth), (600, offset[1] + i * axisWidth))
            i += 1


        # Drawing the curve
        for i in range(len(points) - 1):
            point1 = (points[i][0] * scale + centre[0],
                      points[i][1] * scale + centre[1],)

            point2 = (points[i + 1][0] * scale + centre[0],
                      points[i + 1][1] * scale + centre[1],)
            pg.draw.aaline(self.graphSurf, (0, 0, 0), point1, point2)


        # Drawing the border
        pg.draw.lines(self.graphSurf, (0, 0, 0), True, ((0, 0), (599, 0), (599, 399), (0, 399)), 5)
        self.screen.blit(self.graphSurf, self.graphPoint)


display = Display()


points = []
for i in range(720 * 2):
    i = i / 360 * pi - pi * 2
    points.append([i, sin(i)])


running = True
mouseTracking = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYUP and event.key == pg.K_ESCAPE: running = False
        if event.type == pg.MOUSEWHEEL:
            if event.y == 1: display.graphZoom /= 1.5
            if event.y == -1: display.graphZoom *= 1.5
        if event.type == pg.MOUSEBUTTONDOWN: 
            mouseTracking = True
            pg.mouse.get_rel()
        if event.type == pg.MOUSEBUTTONUP: mouseTracking = False

    if mouseTracking:
        displacement = pg.mouse.get_rel()
        display.graphCentre[0] += displacement[0]
        display.graphCentre[1] += displacement[1]

    display.drawScreen(points)
