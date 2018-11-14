
#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: svg examples
# Created: 08.09.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

try:
    import svgwrite
except ImportError:
    # if svgwrite is not 'installed' append parent dir of __file__ to sys.path
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/..'))

import svgwrite

def linearGradient(name):
    dwg = svgwrite.Drawing(name, size=('15cm', '15cm'), profile='full', debug=True)

    # set user coordinate space
    dwg.viewbox(width=150, height=150)

    # dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(0,0,0)'))

    # create a new linearGradient element
    vertical_gradient = dwg.linearGradient((0, 1), (0, 0))

    # add gradient to the defs section of the drawing
    dwg.defs.add(vertical_gradient)

    # define the gradient from white to red
    vertical_gradient.add_stop_color(0, 'white', 1)
    vertical_gradient.add_stop_color(.25, 'white', 0)
    vertical_gradient.add_stop_color(.5, 'white', 1)
    vertical_gradient.add_stop_color(.75, 'white', 0)
    vertical_gradient.add_stop_color(1, 'white', 1)

    dwg.add(dwg.polyline(
        [(50, 50), (0, 75), (50, 100), (0, 125), (50, 150), (150, 150), (150, 50)],
        stroke='black', fill=vertical_gradient.get_paint_server(default='currentColor')))

    dwg.save()

if __name__ == '__main__':
    linearGradient("testYBasis.svg")