import pygame as pg
from numpy import round, log10

WIDTH = 1100
HEIGHT = 700

G_WIDTH = 650
G_HEIGHT = 620

SUB_WIDTH = 375
SUB_HEIGHT = 230

G_POINT = (15, 15)
SUB_POINT = (WIDTH - SUB_WIDTH - 30, HEIGHT - SUB_HEIGHT - 30)

AXES_SCALES = (1, 2, 5)

GRAPH_FONT = pg.font.SysFont("arial", 17)

TAB_FONT = pg.font.SysFont("arial", 17)
UI_FONT = pg.font.SysFont("arial", 20)

TITLE_FONT = pg.font.SysFont("arial", 20)
TITLE_FONT.underline = True

class Display():
    def __init__(self):
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption("Projectile Simulation")

        # Main Graph Properties
        self.graphSurf = pg.Surface((G_WIDTH, G_HEIGHT))
        self.graphZoom = 30
        self.graphCentre = [G_WIDTH / 6, 5 * G_HEIGHT / 6]
        
        # Sub Graph Properties
        self.subGraphSurf = pg.Surface((SUB_WIDTH, SUB_HEIGHT))
        self.subZoom = 30
        self.subCentre = [25, SUB_HEIGHT - 25]

    
        self.sliders = [Slider(690, 1075, 50, 45, 90, 0.5, "Angle: ___°"),
                        Slider(690, 1075, 100, 10, 50, 0.0625, "Velocity:  ___m/s"),
                        Slider(690, 1075, 310, 9.81, 20, 0.0625, "Gravity:  ___N/Kg"),
                        Slider(710, 1055, 440, 0.5, 2, 0.00390625, "Drag Coefficient: ___", hidden = True),
                        Slider(710, 1055, 500, 1.2, 5, 0.015625, "Air Density: ___Kg/m³", hidden = True),
                        Slider(710, 1055, 480, 0.5, 1, 0.00390625, "Coefficient of Restitution: ___", hidden = True),
                        Slider(710, 1055, 570, 4, 10, 1, "Number of bounces: ___", hidden = True)]
        
        self.checkBoxes = [CheckBox((900, 160), "Bounding Parabola"),
                           CheckBox((697, 255), "Earth Gravity", True),
                           CheckBox((900, 200), "Maximum Range"),
                           CheckBox((710, 510), "Minimum Velocity", True, hidden = True),
                           CheckBox((710, 545), "High Ball", hidden = True),
                           CheckBox((710, 580), "Low Ball", hidden = True)]

        self.textBoxes = [TextBox((716, 170), 40, "X : ", 0),
                          TextBox((794, 170), 40, "Y : ", 0),
                          TextBox((732, 440), 40, "X : ", 3, True),
                          TextBox((812, 440), 40, "Y : ", 3, True),
                          TextBox((915, 540), 40, "Cross Sectional Area (cm²): ", 10, True),
                          TextBox((784, 590), 40, "Mass (g): ", 5, True)]
        
        self.tabMenu = TabMenu((680, 375), (1085, 685), ("Sub Graph", "Two Points", "Air Resistance", "Bounce"))

        self.textSurfs = [TITLE_FONT.render("Launch Point:", True, (50, 50, 70)),
                          TITLE_FONT.render("Second Point:", True, (50, 50, 70))]

    def drawScreen(self, lines, points, relMousePos, subLines):
        self.screen.fill((150, 150, 175))
        self.drawGraph(lines, points)

        # Draw the Tab Menu
        self.tabMenu.draw(self.screen)

        self.screen.blit(self.textSurfs[0], (690, 130))
        if self.tabMenu.currentTab == 0: self.drawSubGraph(subLines, None)
        if self.tabMenu.currentTab == 1: self.screen.blit(self.textSurfs[1], (707, 400), )
        
        # Draw all sliders
        for slider in self.sliders:
            slider.draw(self.screen)

        # Draw all checkboxes
        for checkBox in self.checkBoxes:
            checkBox.draw(self.screen)

        # Draw all textboxes
        for textBox in self.textBoxes:
            textBox.draw(self.screen)


        # Displaying the coordinates of the mouse on screen
        if relMousePos != False:
            pixScale = self.graphZoom / G_WIDTH
            roundVal = int(log10(1 / self.graphZoom)) + 2

            gMousePos = (round((relMousePos[0] - self.graphCentre[0]) * pixScale, roundVal),
                         round((self.graphCentre[1] - relMousePos[1]) * pixScale, roundVal))
            
            if roundVal <= 0:
                gMousePos = (int(gMousePos[0]), int(gMousePos[1]))

            self.screen.blit(UI_FONT.render(f"{str(gMousePos[0])}, {str(gMousePos[1])}", True, (50, 50, 60)), (G_POINT[0] + 5, G_POINT[1] + G_HEIGHT + 5))
        
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

            textSurf = GRAPH_FONT.render(str(text), True, (100, 100, 100))
            dims = textSurf.get_size()

            if centre[1] < 4: surface.blit(textSurf, (x - dims[0] - 2, 4))
            if 4 < centre[1] < height - dims[1] - 4: surface.blit(textSurf, (x - dims[0] - 2, centre[1]))
            if height - dims[1] - 4 < centre[1]: surface.blit(textSurf, (x - dims[0] - 2, height - dims[1] - 4))

            pg.draw.line(surface, (150, 150, 150), (x, 0), (x, height))
        
        
        for i in range(int(height // axScale) + 2):
            y = centreOffset[1] + axScale * (i - 1)

            text = axisWidth * (axisBefore[1] - i)
            if textType: text = int(text)

            textSurf = GRAPH_FONT.render(str(text), True, (100, 100, 100))
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
                pg.draw.aaline(self.graphSurf, line.colour, point1, point2)

        # Drawing any points
        for point in points:
            pg.draw.circle(self.graphSurf, (200, 75, 75), (centre[0] + point.pos[0] * scale, centre[1] - point.pos[1] * scale), 5)
            
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
    def __init__(self, xPos1, xPos2, yPos, initVal, valRange, step, label, active = True, hidden = False):
        
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
        self.hidden = hidden

    def draw(self, surface):
        if not self.hidden:
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
            surface.blit(labelSurf, (self.xPos1, self.yPos - 30))
    
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
    def __init__(self, pos, label, startState = False, active = True, hidden = False):
        self.label = label
        self.pos = pos

        self.state = startState
        self.active = active
        self.hidden = hidden

    def draw(self, surface):
        if not self.hidden:
            pg.draw.rect(surface, (100, 100, 100), pg.Rect(self.pos[0] - 7, self.pos[1] - 7, 18, 18))
            pg.draw.rect(surface, (200, 200, 200), pg.Rect(self.pos[0] - 5, self.pos[1] - 5, 14, 14))
            if self.state:
                pg.draw.rect(surface, (70, 70, 70), pg.Rect(self.pos[0] - 4, self.pos[1] - 4, 12, 12))
                
            
            labelSurf = UI_FONT.render(self.label, True, (50, 50, 60))
            surface.blit(labelSurf, (self.pos[0] + 15, self.pos[1] - 10))
            

    def inHitbox(self, mousePos):
        if self.pos[0] - 7 <= mousePos[0] <= self.pos[0] + 11 and self.pos[1] - 7 <= mousePos[1] <= self.pos[1] + 11:
                if self.state: self.state = False
                else: self.state = True


class TextBox():
    def __init__(self, pos, width, label, defaultVal, hidden = False):
        self.pos = pos
        self.width = width
        self.hitBox = pg.Rect(self.pos, (self.width, 25))

        self.label = label
        self.labelSurf = UI_FONT.render(self.label, True, (50, 50, 70))
        self.labelDims = self.labelSurf.get_size()
        self.value = str(defaultVal)

        self.tracking = False
        self.cursorClock = pg.time.Clock()
        self.cursorTime = 0
        self.hidden = hidden

    def draw(self, surface):
        if not self.hidden:
            height = 25
            pg.draw.rect(surface, (180, 180, 220), self.hitBox)
            pg.draw.lines(surface, (50, 50, 70), True, (self.pos, (self.pos[0] + self.width, self.pos[1]), (self.pos[0] + self.width, self.pos[1] + height), (self.pos[0],self.pos[1] + height)), 2)
            
            surface.blit(self.labelSurf, (self.pos[0] - self.labelDims[0], self.pos[1] + (height - self.labelDims[1]) / 2))

            valSurf = UI_FONT.render(str(self.value), True, (50, 50, 70))
            valDims = valSurf.get_size()
            surface.blit(valSurf, (self.pos[0] + 5, self.pos[1] + 1))

            if self.tracking:
                if (self.cursorTime // 500) %  2 == 0:
                    surface.blit(UI_FONT.render("|", True, (70, 70, 100)), (self.pos[0] + 5 + valDims[0], self.pos[1] - 1))
                self.cursorTime += self.cursorClock.tick()

    def mouseClicked(self, event):
        if self.hitBox.collidepoint(event.pos):
            self.tracking = True
            self.cursorClock.tick()
            self.cursorTime = 0
        else:
            self.tracking = False

    def keyPressed(self, event):
        if event.key == pg.K_BACKSPACE:
            self.value = self.value[:-1]

        if 48 <= event.key <= 57:
            self.value += event.unicode
        
        if event.key == pg.K_PERIOD and "." not in self.value:
            self.value += event.unicode


class TabMenu():
    def __init__(self, pos1, pos2, tabs, currentTab = 0):
        self.pos1 = pos1
        self.pos2 = pos2
        self.dims = (pos2[0] - pos1[0], pos2[1] - pos1[1])

        self.rect = pg.Rect(self.pos1, self.dims)

        self.currentTab = currentTab

        self.tabs = [None for i in range(len(tabs))]
        self.tabWidth = self.dims[0] / len(tabs)
        

        for i, label in enumerate(tabs):
            tabRect = pg.Rect((self.pos1[0] + i * self.tabWidth, self.pos1[1] - 35), (self.tabWidth, 40))
            labelSurf = TAB_FONT.render(label, True, (50, 50, 70))

            self.tabs[i] = (labelSurf, tabRect)

    def draw(self, surface):
        r = 3
        bCol = (50, 50, 80)
        darkCol = (120, 120, 150)

        for i, (labelSurf, rect) in enumerate(self.tabs):
            pg.draw.rect(surface, (130, 130, 160), rect, 0, -1, r, r)
            pg.draw.rect(surface, (80, 80, 100), rect, r - 1, r)
            labelDims = labelSurf.get_size()
            surface.blit(labelSurf, (self.pos1[0] + self.tabWidth * (i + 0.5) - labelDims[0] / 2, self.pos1[1] - 28))
        
    
        pg.draw.rect(surface, darkCol, self.rect, 0, r)
        pg.draw.rect(surface, bCol, self.rect, r, r)
        

        labelSurf, tabRect = self.tabs[self.currentTab]
        pg.draw.rect(surface, darkCol, tabRect, 0, -1, r, r)
        pg.draw.rect(surface, bCol, tabRect, r, r)
        labelDims = labelSurf.get_size()
        surface.blit(labelSurf, (self.pos1[0] + self.tabWidth * (self.currentTab + 0.5) - labelDims[0] / 2, self.pos1[1] - 28))

        pg.draw.line(surface, darkCol, (self.pos1[0] + self.tabWidth * self.currentTab + 1, self.pos1[1] + r), (self.pos1[0] + self.tabWidth * (self.currentTab + 1) - 1, self.pos1[1] + r), r)
        pg.draw.line(surface, bCol, (self.pos1[0] + r / 2, self.pos1[1]), (self.pos1[0] + r / 2, self.pos1[1] + 10), r)
        pg.draw.line(surface, bCol, (self.pos2[0] - r / 2, self.pos1[1]), (self.pos2[0] - r / 2, self.pos1[1] + 10), r)

    def mouseClicked(self, event):
        for i, tab in enumerate(self.tabs):
            if tab[1].collidepoint(event.pos):
                self.currentTab = i
                return True