import pygame

#Colors
white = (255,255,255)
blue = (0,0,255)
liteblue = (80, 80, 255)
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
simFieldColor = (20,20,20)
gray = (50, 50, 50)
litegray = (100, 100, 100)
litergray = (150, 150, 150)
green = (34,139,34)

#Settings
#screen (dont change)
screenX = 1200
screenY = 600

#TIME
#In hoeveel aparte berekeningen de animatie wordt opgedeeld per seconde
StepsPerSec = 30 #0.0001   
#Hoeveel gesimuleerde secondes in een echte seconde voorkomen
SpeedMultiplier = 10 #100000

#screen layout [[viewer x, viewer y], [menu under x, menu under y], [menu right x, menu right y]]
screenlayout = [[7, 1], [0,0], [5, 1]]
singleSettingList = ["Settings", "Settings"]


#START PYGAME
#initialize pygame
pygame.init()
screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)

#caption and icon
pygame.display.set_caption("engine")

#text fonts
fontfreesan = pygame.font.Font('freesansbold.ttf', 20)

#SIMFIELD
#simfieldsize in m
simfieldsizex = 5 #8e11 #None  #
#simfieldsizey = None
simfieldsizey = None






