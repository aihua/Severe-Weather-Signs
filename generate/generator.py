#-*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
from string import Template
import json

file_warning = open( 'warnings.json')
warnings = json.loads(file_warning.read(  ).decode('utf8'))

color_mapping = warnings['colors']

svg_tpl = open( 'template.svg.txt' )
src = Template( svg_tpl.read() )

for warning in warnings['warnings']:
    icon_svg_dom = xml.dom.minidom.parse(warning['weather_icon'])
    icon_path = icon_svg_dom.getElementsByTagName('path')[0].getAttributeNode('d').nodeValue
    for color in warning['colors']:
        d = {\
        'color_hex': color_mapping[color]['hex'], \
        'color_text': color_mapping[color]['zh'] + u'预警', \
        'weather_char1':warning['weather'][0],\
        'weather_char2':warning['weather'][1],\
        'weather_en': warning['weather_en'],\
        'weather_icon_path': icon_path\
        }
        output = open('../set1/' + warning['weather_en'] + '_' + color + '.svg','w')
        output.write(src.substitute(d).encode('utf8'))