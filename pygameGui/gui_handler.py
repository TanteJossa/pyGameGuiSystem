import copy
from pandas import array
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
    def __init__(self, name = 'None', hasLayout = False, isSimField = False, simFieldDimensions = (10, 10), isVertical = False, coord1 = None, coord2 = None, divisions = {}, settings = None, priority = 1, hasAxis = False):
        global menus, menuNames, screenMenuId
        
        self.isSimfield = isSimField

        if isSimField:
            self.simFieldDimensions = simFieldDimensions
            self.objects = []
            self.objectId = 1
            self.hasAxis = hasAxis
            
        self.hasLayout = hasLayout
        
        
        self.isVertical = isVertical
        self.divisions = []
        self.divisionNames = []
        for divisionValue in list(divisions.values()):
            self.divisions.append(divisionValue)
        for divisionName in list(divisions.keys()):
            self.divisionNames.append(divisionName)
        
        self.settings = settings    
            
        if coord1 != None and coord2 != None:
            self.coord1 = coord1
            self.coord2 = coord2
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
        
    def draw_menu(self):
        if self.isSimfield == False:
            create_menu(self.coord1, self.coord2, divisions=self.divisions, names=self.divisionNames, isVertical=self.isVertical, settings=self.settings)
        else:
            create_rectangle(self.coord1, self.coord2)
            create_rectangle((self.coord1[0] + 5, self.coord1[1] + 5), (self.coord2[0] - 5, self.coord2[1] - 5), color=simFieldColor)
            if self.hasAxis == True:
                coord1Line1 = self.calc_simField_to_pixel((self.simFieldDimensions[0] / 2, 0))
                coord2Line1 = self.calc_simField_to_pixel((self.simFieldDimensions[0] / 2 , self.simFieldDimensions[1])) 
                coord1Line2 = self.calc_simField_to_pixel((0, self.simFieldDimensions[1] / 2))
                coord2Line2 = self.calc_simField_to_pixel((self.simFieldDimensions[0], self.simFieldDimensions[1] / 2))
                #vertical
                create_line((coord1Line1[0], coord1Line1[1] + 15), (coord2Line1[0], coord2Line1[1] + 3), width=3)
                #horizontal
                create_line((coord1Line2[0] + 5, coord1Line2[1]), (coord2Line2[0] - 5, coord2Line2[1]), width=3)
                            
            
            coordTypes = ['coord1', 'coord2', 'center', 'radius', 'radiusDimensions']
            objects = copy.deepcopy(self.objects)
            
            self.pixelPerX = self.width / self.simFieldDimensions[0]
            self.pixelPerY = self.height / self.simFieldDimensions[1]

            
            for currentObject in objects:
                for item in coordTypes:
                    if item in list(currentObject['data'].keys()):
                        currentObject['data'][item] = self.calc_simField_to_pixel(currentObject['data'][item])
                        
                if currentObject['type'] == 'rect':
                    create_rectangle(**currentObject['data'])
                elif currentObject['type'] == 'line':
                    create_line(**currentObject['data'])
                elif currentObject['type'] == 'point':
                    create_point(**currentObject['data'])
                elif currentObject['type'] == 'circle':
                    currentObject['data']['radiusDimensions'] = (currentObject['data']['radius'] * self.pixelPerX, currentObject['data']['radius'] * self.pixelPerY)
                    create_ellipse(**currentObject['data'])
                elif currentObject['type'] == 'ellipse':
                    create_ellipse(**currentObject['data'])
                elif currentObject['type'] == 'arrow':
                    create_arrow(**currentObject['data'])
                elif currentObject['type'] == 'text':
                    create_text(**currentObject['data'])            
            
            create_rectangle((self.coord1[0] + 8, self.coord1[1] + 8),(self.coord2[0] - 8, self.coord1[1] + 30) ,color=litergray)
            create_text(self.name, coord1=(self.coord1[0] + 13, self.coord1[1] + 8), coord2 =(self.coord1[0] + (self.coord1[0] + self.coord2[0]) / 2, self.coord1[1] + 30),color = liteblue, font=fontfreesan)
    
    def add_simObject(self, name = None, type= 'rect', coord1=None, coord2=None, centre=None, color = None, text = None, width = None, radius = None, radiusWidth= None, radiusHeight=None, textColor = None):
        if name == None:
            return print('please return a name')
        
        inputs = {'name': name,
                  'type' :type, 
                  'coord1': coord1,
                  'coord2': coord2,
                  'centre': centre,
                  'color': color, 
                  'text': text,
                  'width': width,
                  'radius': radius,
                  'radiusWidth': radiusWidth,
                  'radiusHeight': radiusHeight,
                  'textColor' : textColor
                  }

        if isinstance(type, int):
            if type == 1:
                type = 'rect'
                items = {'needed': [['coord1', 'coord2']], 'possible':['color']}
            elif type == 2:
                type = 'line'
                items = {'needed': [['coord1', 'coord2']], 'possible':['color']}
            elif type == 3:
                type = 'point'
                items = {'needed': [['center']], 'possible':['color','width','radius']}
            elif type == 4:
                type == 'circle'
                items = {'needed': [['center','radius']], 'possible':['color','width',]}

            elif type == 5:
                type = 'ellipse'
                items = {'needed': [['center', 'radiusDimensions']], 'possible':['color','width']}
            
            elif type == 6:
                type = 'arrow'
                items = {'needed': [['coord1', 'coord2']], 'possible':['color', 'width', 'text', 'textColor']}
            
            elif type == 7:
                type = 'text'
                items = {'needed': [['coord1', 'coord2', 'text']], 'possible':['color']}
            
        pleaseProvide = []
        foundNeededItems = False
        currentObject = {'name' : name,
                         'id': self.objectId,
                         'type': type,
                         'data': {}}
                
        for itemIndex in range(0, len(items['needed'])):
            if foundNeededItems == False:
                if isinstance(items['needed'][itemIndex], list):
                    pleaseProvide.append([])
                    foundAllItemsInList = True
                    for neededItem in items['needed'][itemIndex]:
                        if inputs[neededItem] == None:
                            pleaseProvide[-1].append(neededItem)
                            foundAllItemsInList = False
                    
                    if foundAllItemsInList == True:
                        for neededItem in items['needed'][itemIndex]:
                            currentObject['data'][neededItem] = inputs[neededItem]
                            foundNeededItems = True
                else:
                    if inputs[items['needed'][itemIndex]] != None: 
                        currentObject['data'][items['needed'][itemIndex]] = inputs[neededItem]
                        foundNeededItems = True
                    else:
                        pleaseProvide.append([])
                        pleaseProvide[-1].append(items['needed'][itemIndex])


        if foundNeededItems == False:
            message = '( '
            for possibility in range(0, len(pleaseProvide) - 1):
                for item in pleaseProvide[possibility]:
                    message = message + ', ' + item
                
                if possibility != len(pleaseProvide) - 1:
                    message = message + ') or ('
                else:
                    message = message + ')'


            return print('Please provide: ' + message)

        
        for possibility in items['possible']:
            if inputs[possibility] != None:
                currentObject['data'][possibility] = inputs[possibility]

        self.objectId += 1
        
        self.objects.append(currentObject)    
    
    def set_simField_dimensions(self, simFieldDimensions = (10, 10)):
        self.simFieldDimensions[0] = simFieldDimensions[0]
        self.simFieldDimensions[1] = simFieldDimensions[1]            

    def calc_simField_to_pixel(self, x = None, y=None):        
        if isinstance(x, tuple):
            if isinstance(x[0], (int, float)) and isinstance(x[1], (int, float)):
                return ( x[0] / self.simFieldDimensions[0] * (self.coord2[0] - self.coord1[0]) + self.coord1[0], x[1] / self.simFieldDimensions[1] * (self.coord2[1] - self.coord1[1]) - self.coord1[1])
        elif x != None:
            return  x / self.simFieldDimensions[0] * (self.coord2[0] - self.coord1[0]) + self.coord1[0]
        elif y != None:
            return  y / self.simFieldDimensions[1] * (self.coord2[1] - self.coord1[1]) - self.coord1[1]
        else:    
            print("did not put in a valid x, y or a coord in calc_game_to_pixel_coords()")
            
    
    def name_to_id(name):
        return list(menuNames.keys())[list(menuNames.values()).index(name)]

    def id_to_name(id):
        return list(menuNames.values())[list(menuNames.keys()).index(id)]
     
    def calc_dimensions(self, screenX, screenY, divisions):
        self.width = (screenX - 20) / divisions[0] * self.divisions[0] 
        self.height = (screenY - 20) / divisions[1] * self.divisions[1]
            

            
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

                    currentMenu.coord1 = (X1, Y1)
                    currentMenu.coord2 = (X2, Y2)

                
                currentHeightPixels += heigth
            
            currentColumnWidth += columnWidth

        for menu in menus['all']:
            if menu.name in self.menuSortNames or menu in menus['solid']:
                menu.draw_menu()
