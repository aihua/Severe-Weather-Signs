#-*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
from string import Template
import json
#import cairo
#import rsvg

file_warning = open( 'warnings.json')
warnings = json.loads(file_warning.read(  ).decode('utf8'))

color_mapping = warnings['colors']

svg_tpl = open( 'template.svg.txt' )
src = Template( svg_tpl.read() )

for warning in warnings['warnings']:
    icon_svg_dom = xml.dom.minidom.parse(warning['weather_icon'])
    icon_path = icon_svg_dom.getElementsByTagName('path')[0].getAttributeNode('d').nodeValue
    for color in warning['colors']:
        output_path_prefix = '../set1/svg/' + warning['weather_en'] + '_' + color
        output_path_svg = output_path_prefix + '.svg'
        output_path_png = output_path_prefix + '.png'
        d = {\
        'color_hex': color_mapping[color]['hex'], \
        'color_text': color_mapping[color]['zh'] + u'预警', \
        'weather':warning['weather'],\
        'weather_en': warning['weather_en'],\
        'weather_icon_path': icon_path\
        }
        svg_src = src.substitute(d).encode('utf8');
        output = open(output_path_svg,'w')
        output.write(svg_src)
        #cairosvg.svg2png(bytestring=svg_src, write_to=output_path_png)