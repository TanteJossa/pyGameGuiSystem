from pygameGui import *
from pygameGui.gui_handler import pyGameGui, screenMenu

pygameGui = pyGameGui()


test = screenMenu('test', True, divisions={'hi': 1, 'test' : 2}, settings=[{'settings': 1},{}])
hi2 = screenMenu('hi2', True, divisions={'hi': 1, 'test2' : 2}, settings=[{'settings': 1}, {}])
hi3 = screenMenu('hi3', True, divisions={'hi': 1, 'test3' : 2}, settings=[{'settings': 1}, {}])
simField = screenMenu('simField', True, True, hasAxis=True)
simField2 = screenMenu('simField2', True, isSimField=True)

menuSort = [{'width': 3, 'data': {'simField': 3, 'hi2': 1}},{'width': 1, 'data':{'simField2': 3, }}]

simField.add_simObject('rectangle1', type=1, coord1=(5, 5), coord2=(7, 7))

while True:
    pygameGui.update(menuSort)
    