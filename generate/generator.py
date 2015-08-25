#-*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
from string import Template
import json
import subprocess
import os

file_warning = open( 'warnings.json')
warnings = json.loads(file_warning.read(  ).decode('utf8'))

color_mapping = warnings['colors']

svg_tpl = open( 'template.svg.txt' )
src = Template( svg_tpl.read() )

for warning in warnings['warnings']:
    icon_svg_dom = xml.dom.minidom.parse(warnings['iconset'] + '/' + warning['weather_en'].replace(' ','') + '_icon.svg')
    icon_path = icon_svg_dom.getElementsByTagName('path')[0].getAttributeNode('d').nodeValue
    for color in warning['colors']:
        output_path_temp = '../set1/{format}/' + warning['weather_en'].replace(' ','') + '_' + color + '.{format}'
        output_path_svg = output_path_temp.format(format = 'svg')
        output_path_png = output_path_temp.format(format = 'png')
        d = {\
        'color_hex': color_mapping[color]['hex'], \
        'color_text': color_mapping[color]['zh'] + u'预警', \
        'weather': warning['weather'],\
        'weather_en': warning['weather_en'],\
        'weather_icon_path': icon_path\
        }
        svg_src = src.substitute(d).encode('utf8');
        with open(output_path_svg, "wb") as outputFile:
            outputFile.write(svg_src)
            print "SVG Output Done"
        command = ['./content-screenshot/contentScreenshot.py', os.path.abspath(output_path_svg), os.path.abspath(output_path_png)]
        p = subprocess.Popen(command, shell = False, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        stdout, stderr = p.communicate()
        if (stdout.startswith("Done")):
            print "SVG Convert Done"
        else:
            print stderr
