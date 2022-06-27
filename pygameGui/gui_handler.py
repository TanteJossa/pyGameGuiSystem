import pygame
import os
from time import time, sleep
import time
import pygame
from math import *
from pygameGui.screen.create import *
from pygameGui.screen.calc import *
from pygameGui.settings.settings import *

#mouse States
mousePressed = False 
leftMousePressed = False 
middleMousePressed = False 
rightMousePressed = False 
clock = pygame.time.Clock()
#mouse an mouse arrow setup
click_arrow_start = (0, 0)
click_arrow_end = (0, 0)

last_click_selected_obj = False
mouseHoldLength = 0

TotalSteps = 0
TotalIRLTime = 0
menus = {'solid' : {}, 'layout' : {}, 'all' : []}    
menuNames = {}
screenMenuId = 1


class screenMenu():
    def __init__(self, name = 'None', hasLayout = False, isSimField = False, isVertical = False, leftup = None, rightdown = None, divisions = None, settings = None, priority = 1):
        global menus, menuNames, screenMenuId
        

        self.hasLayout = hasLayout
        
        if leftup != None and rightdown != None:
            self.leftup = leftup
            self.rightdown = rightdown
            self.hasLayout = False
        else:
            print('please provide position data for this menu')  
        self.priority = priority
        self.id = screenMenuId
        self.name = name
        if self.hasLayout:
            type = 'layout'
        else:
            type = 'solid'
            
        self.isVertical = isVertical
        self.divisions = []

        self.divisionNames = []
        for divisionValue in list(divisions.values()):
            self.divisions.append(divisionValue)
        for divisionName in list(divisions.keys()):
            self.divisionNames.append(divisionName)
        
        self.settings = settings

        menus[type][str(screenMenuId)] = self

        menuNames[str(screenMenuId)] = name
        screenMenuId += 1


                    
        i = 0
        placedMenu = False

        while i < len(menus['all']) and placedMenu == False:
            if menus['all'][i].priority >= priority:
                menus['all'].insert(i, self) 
                placedMenu = True
            i = i + 1
        if placedMenu == False:
            menus['all'].append(self) 
        
    def name_to_id(name):
        return list(menuNames.keys())[list(menuNames.values()).index(name)]

    def id_to_name(id):
        return list(menuNames.values())[list(menuNames.keys()).index(id)]
     
    def calc_dimensions(self, screenX, screenY, divisions):
        self.width = (screenX - 20) / divisions[0] * self.divisions[0] 
        self.length = (screenY - 20) / divisions[1] * self.divisions[1]
            

            
#pygameGui object
class pyGameGui():
    def __init__(self, ScreenSizeX = 600, ScreenSizeY = 300, resizeable = True, backGroundColor = black, useSimField = True):
        self.screenX = ScreenSizeX
        self.screenY = ScreenSizeY
        self.sizeable = resizeable
        self.background = backGroundColor
        self.menus = {'layout' : [],'solid' : []}

        #initialize button gui 
        #manager = pygame_gui.UIManager((screenX, screenY))
        self.clock = pygame.time.Clock()
        self.TotalSteps = 0
        self.TotalIRLTime = 0
    
    def update(self, menuSort):
        global TotalSteps, TotalIRLTime, menus, menuNames, screenMenuId

        self.menuSort = menuSort
        #setup for frame time calculation
        StartTime = time.time()
        time_delta = clock.tick(60)/1000.0

        #set the screen size if it has changed
        self.screenX = screen.get_size()[0]
        self.screenY = screen.get_size()[1]
        
        # simFieldX1 = 10
        # simFieldY1 = 10
        # simFieldX2 = screen.get_width() / (screenlayout[0][0] + screenlayout[2][0]) * screenlayout[0][0]
        # simFieldY2 = (screen.get_height())  / (screenlayout[0][1] + screenlayout[1][1]) * screenlayout[0][1] - 10
        # screenXYratio = (simFieldY2 - simFieldY1) /  (simFieldX2 - simFieldX1)
        # simFieldOrigin = ((simFieldX2 - simFieldX1) / 2, (simFieldY2 - simFieldY1) / 2)
        # pixelPerUnity =  (simFieldY2 - simFieldY1) / (simfieldsizey)
        # pixelPerUnitx =  (simFieldX2 - simFieldX1) / (simfieldsizex)

        #event loop
        for event in pygame.event.get():
            #stop the program if someone exits
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(str(pygame.mouse.get_pos()) + str((calc_pixel_to_game_coords(pygame.mouse.get_pos()[0]), calc_pixel_to_game_coords(y=pygame.mouse.get_pos()[1]))))
                self.mousePressed = True
            
                state = pygame.mouse.get_pressed()
                #state = (leftclick, middleclick, rightclick) = (0, 0, 0)
                if state[0] == True:
                    self.leftMousePressed = True
                elif state[1] == True:
                    self.middleMousePressed = True
                elif state[2] == True:
                    self.rightMousePressed = True

                    

                #setup for draw arrow creation
                last_mous_clickpos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                selected_an_obj = False
                last_click_selected_obj = False
                mouseHoldLength = 0

                #set the start of the arrow if a player drags in an open space (or on an object)
                click_arrow_start = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.leftMousePressed = False 
                self.middleMousePressed = False
                self.rightMousePressed = False
                self.mousePressed = False

        #mouse pressed loop actions        
        if leftMousePressed == True:
            pass
        if rightMousePressed == True:
            pass
   
        screen.fill(self.background)
        
        self.menuSortNames = []

        for column in self.menuSort:
            for menu in column['data']:                
                if not isinstance(column['data'][menu], dict):
                    heightData = column['data'][menu]
                    column['data'][menu] = {'height' : heightData, 'isEmpty': False} 
                    
                                
        self.draw_menus()
        #menu blocks
        #draw the menu's
#        create_rectangle((simFieldX1, simFieldY1),(simFieldX2, simFieldY2), color=(30, 30, 70))
        
        #grafiek
        # create_line(calc_game_to_pixel_coords((simfieldsizex / 2, 0)), calc_game_to_pixel_coords((simfieldsizex / 2, simfieldsizey)), width=3)
        # create_line(calc_game_to_pixel_coords((0, simfieldsizey / 2)) , calc_game_to_pixel_coords((simfieldsizex, simfieldsizey / 2)), width=3)
        
        #update menus
        pygame.display.flip()
        #manager.draw_ui(screen)

        #counts total simulation steps
        TotalSteps = TotalSteps + 1

        #draw the entire picture to the screen
        pygame.display.update()

        #calculate simulation time
        EndTime = time.time()

        TotalIRLTime = TotalIRLTime + (time.time() - StartTime)

    def draw_menus(self):
        #voor
        totalColumnSegments = 0
        
        #menu sort  = [{'width': 1, 'data': {'test': {'height': 1, 'isEmpty': False}, 'hi2': 3}}, {'width': 1, 'data': {'hi3': 3}}]
        ##get the total amount of horizontal segments
        for column in self.menuSort:
            totalColumnSegments += column['width']
        
        columnWidthPixels = []
        currentColumnWidth = 0
        
        for column in self.menuSort:
            columnWidth = (self.screenX - 10) / totalColumnSegments * column['width']
            #get the pixel width of this column
            columnWidthPixels.append(columnWidth)

            #calculate the heigth segments of the column
            totalHeightSegments = 0
            heightSegmentAmount = 0
            for menu in column['data']:
                print(column)
                totalHeightSegments += column['data'][menu]['height']
                heightSegmentAmount += 1
                        
            currentHeightPixels = 0
            
            #calculate the height for every segment in a column
            for menu in column['data']:
                heigth = (self.screenY - 10) / totalHeightSegments * column['data'][menu]['height'] + 0 * heightSegmentAmount  
                

                X1 = currentColumnWidth + 5
                Y1 = currentHeightPixels + 5
                
                X2 = X1 + columnWidth - 5
                Y2 = Y1 + heigth - 5

                if not column['data'][menu]['isEmpty'] == True:
                #set the height and width of the segments
                    self.menuSortNames.append(menu)

                    currentMenu = menus['layout'][screenMenu.name_to_id(menu)]

                    currentMenu.height = heigth
                    currentMenu.width = columnWidth

                    currentMenu.leftup = (X1, Y1)
                    currentMenu.rightdown = (X2, Y2)

                
                currentHeightPixels += heigth
            
            currentColumnWidth += columnWidth

        for menu in menus['all']:
            if menu.name in self.menuSortNames or menu in menus['solid']:
                create_menu(menu.leftup, menu.rightdown, divisions=menu.divisions, names=menu.divisionNames, isVertical=menu.isVertical, settings=menu.settings)
