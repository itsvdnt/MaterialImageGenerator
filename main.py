#!/usr/bin/env python

import PIL
import os
import pickle
from pathlib import Path
from shutil import copy
from xml.dom.minidom import *
import convert 
import sys

path = os.path.dirname(os.path.abspath(__file__))
icons = path+'/icons/'
f=[]
class MIG:
    def setDimensions(self, width, height):
        self.width = width
        self.height = height
    def getImages(self, kw):
        for filename in Path(icons).rglob('*'+kw+'*.xml'):
            convert.convert_vector_drawable(str(filename), None, None, '#000')
            f.append(str(filename)[:-3]+'svg')
    def lets(self):
        import svgutils.transform as sg
        import sys 

        #create new SVG figure
        fig = sg.SVGFigure("100", "50")

        # load matpotlib-generated figures
        fig1 = sg.fromfile(f[0])
        fig2 = sg.fromfile(f[1])

        # get the plot objects
        plot1 = fig1.getroot()
        plot2 = fig2.getroot()
        plot2.moveto(50, 0, scale=0.5)

        # append plots and labels to figure
        fig.append([plot1, plot2])

        # save generated SVG files
        fig.save("fig_final.svg")
mig = MIG()
mig.getImages('local')
mig.lets()
print(f[0])
print(f[1])
