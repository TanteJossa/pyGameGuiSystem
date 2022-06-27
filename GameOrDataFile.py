from pygameGui import *
from pygameGui.gui_handler import pyGameGui, screenMenu

pygameGui = pyGameGui()


menu = screenMenu('test', True, divisions={'hi': 1, 'test' : 2}, settings=[{'settings': 1},{}])
menu2 = screenMenu('hi2', True, divisions={'hi': 1, 'test2' : 2}, settings=[{'settings': 1}, {}], isVertical=True)
menu3 = screenMenu('hi3', True, divisions={'hi': 1, 'test3' : 2}, settings=[{'settings': 1}, {}])
menu4 = screenMenu('hi3',leftup=(100, 100), rightdown=(300, 400), divisions={'hi': 1, 'test3' : 2}, settings=[{'settings': 1}, {}], priority=10)


menuSort = [{'width': 1, 'data': {'empty': {'height': 1, 'isEmpty': True}, 'hi2': 3}},{'width': 1, 'data':{'hi3': 3, }}]

while True:
    pygameGui.update(menuSort)
    
