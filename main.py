#!/usr/bin/env python

import PIL
import os
import pickle
from pathlib import Path
from shutil import copy
from xml.dom.minidom import Document, parse
import convert 
import sys
import random

path = os.path.dirname(os.path.abspath(__file__))
icons = path+'/icons/'
f=[]
class MIG:

    def __init__(self):
        self.width = 200
        self.height = 200
        self.density = 3

    def convert_paths(self, vd_container, svg_container, svg_xml, fcolor='none'):
        vd_paths = vd_container.getElementsByTagName('path')
        for vd_path in vd_paths:
            # only iterate in the first level
            if vd_path.parentNode == vd_container:
                svg_path = svg_xml.createElement('path')
                svg_path.attributes['d'] = vd_path.attributes[
                    'android:pathData'].value
                if vd_path.hasAttribute('android:fillColor'):
                    svg_path.attributes['fill'] = fcolor
                if vd_path.hasAttribute('android:strokeLineJoin'):
                    svg_path.attributes['stroke-linejoin'] = vd_path.attributes[
                        'android:strokeLineJoin'].value
                if vd_path.hasAttribute('android:strokeLineCap'):
                    svg_path.attributes['stroke-linecap'] = vd_path.attributes[
                        'android:strokeLineCap'].value
                if vd_path.hasAttribute('android:strokeMiterLimit'):
                    svg_path.attributes['stroke-miterlimit'] = vd_path.attributes[
                        'android:strokeMiterLimit'].value
                if vd_path.hasAttribute('android:strokeWidth'):
                    svg_path.attributes['stroke-width'] = vd_path.attributes[
                        'android:strokeWidth'].value
                if vd_path.hasAttribute('android:strokeColor'):
                    svg_path.attributes['stroke'] = get_color(
                        vd_path.attributes['android:strokeColor'].value)

                svg_container.appendChild(svg_path)

    def convertToSVG(self, vd_file_path, fcolor, viewbox_only=None, output_dir=None):
        svg_xml = Document()
        svg_node = svg_xml.createElement('svg')
        svg_xml.appendChild(svg_node)
        vd_xml = parse(vd_file_path)
        vd_node = vd_xml.getElementsByTagName('vector')[0]
        svg_node.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
        if not viewbox_only:
            svg_node.attributes['width'] = vd_node.attributes[
                'android:viewportWidth'].value
            svg_node.attributes['height'] = vd_node.attributes[
                'android:viewportHeight'].value
        svg_node.attributes['viewBox'] = '0 0 {} {}'.format(
            vd_node.attributes['android:viewportWidth'].value,
            vd_node.attributes['android:viewportHeight'].value)
        vd_groups = vd_xml.getElementsByTagName('group')
        for vd_group in vd_groups:
            svg_group = svg_xml.createElement('g')
            translate_x = translate_y = 0
            if vd_group.hasAttribute('android:translateX'):
                translate_x = vd_group.attributes['android:translateX'].value
            if vd_group.hasAttribute('android:translateY'):
                translate_y = vd_group.attributes['android:translateY'].value
            if translate_x or translate_y:
                svg_group.attributes['transform'] = 'translate({},{})'.format(
                    translate_x, translate_y)
            self.convert_paths(vd_group, svg_group, svg_xml, fcolor)
            svg_node.appendChild(svg_group)
        self.convert_paths(vd_node, svg_node, svg_xml, fcolor)
        svg_file_path = vd_file_path.replace('.xml', '.svg')
        if output_dir:
            svg_file_path = os.path.join(output_dir,
                                         os.path.basename(svg_file_path))
        svg_xml.writexml(open(svg_file_path, 'w'),
                         indent="",
                         addindent="  ",
                         newl='\n')

    def setColor(self, image, color):
        svg = parse(image)
        svg.getElementsByTagName('svg')[0].getElementsByTagName('path')[0].attributes['fill'] = color
        svg.writexml(open(image, 'w'),
                         indent="",
                         addindent="  ",
                         newl='\n')
    def isVD(self, image):
        if str(image)[-3:]=='xml':
            return True
        return False

    def isSVG(self, image):
        if str(image)[-3:]=='svg':
            return True
        return False

    def setDimensions(self, width, height):
        self.width = width
        self.height = height

    def getImages(self, keyword):
        for filename in Path(icons).rglob('*'+keyword+'*'):
            if self.isVD(filename):
                self.convertToSVG(str(filename), '#000')
                f.append(str(filename)[:-3]+'svg')
            elif self.isSVG(filename):
                f.append(str(filename)[:-3]+'svg')
            else:
                print('Skipping', filename)

    #Set the density of the output image. Defaults to 3            
    def setDensity(self, density):
        if density>0 and density<5:
            self.density = density
        else:
            density = 3
            print('Use density between 0-4. Using density=3')

    def draw(self):
        import svgutils.transform as sg
        import sys 

        fig = sg.SVGFigure(self.width, self.height)
        n = self.height*self.width*self.density/2500
        random.shuffle(f)
        x = f[:int(n)]
        fig1 = sg.fromfile(x[0])
        fig2 = sg.fromfile(x[1])

        plot1 = fig1.getroot()
        plot2 = fig2.getroot()
        plot2.moveto(50, 50, scale=0.5)

        fig.append([plot1, plot2])

        fig.save("fig_final.svg")
mig = MIG()
mig.getImages('local')
mig.setColor(str(f[0]), 'red')
mig.draw()
print(f[0])
print(f[1])
