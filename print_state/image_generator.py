#!/usr/bin/env python

import xml.etree.cElementTree as ET
import doctest

def rgb_to_hex(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

class MemoryField(object):

    width = 25
    height = 25
    margin = 5

    def __init__(self, pos, text ):
        self.text = text
        self.pos = pos

    def to_svg(self):
        ''' Writes SVG element
        >>> MemoryField(pos=(25,50), text='bla').to_svg()
        '<rect height="25" style="fill:#663;" width="25" x="25" y="50" />'
        '''
        return ET.tostring(self.to_svg_elem())

    def to_svg_elem(self):
        ''' Creates SVG element '''
        return ET.Element('rect', y=str(self.pos[1]), x=str(self.pos[0]),
                          width=str(self.width), height=str(self.height),
                          style="fill:"+rgb_to_hex((100,100,50))+";")

class ProgramState(object):

    fields = {}

    def __init__(self, pos, fields):

        self.pos = pos

        for idx, field in enumerate(fields.keys()):

            pos[0] = pos[0] + (MemoryField.margin + MemoryField.width) * idx
            self.fields[field] = MemoryField(pos[:], fields[field])

    def to_svg(self):
        ''' Writes SVG elements
        >>> ProgramState([10,20], {'a':12, 'b':13}).to_svg()
        '<rect height="25" style="fill:#663;" width="25" x="10" y="20" />\\n<rect height="25" style="fill:#663;" width="25" x="40" y="20" />'
        '''

        result  = []

        for fieldname, field in self.fields.items():
            result.append(field.to_svg())

        return "\n".join(result)

    def to_svg_elems(self):
        ''' Writes SVG elements '''

        return [field.to_svg_elem() for _, field in self.fields.iteritems()]

class SVGdrawing(object):

    height= 500
    width = 500

    children = []

    def to_svg(self):
        ''' Writes SVG elements
        >>> SVGdrawing().to_svg()
        '<svg height="500" width="500"><g style="fill-opacity:1.0; stroke:black;" /></svg>'
        '''
        svg_root = ET.Element('svg',
                       height=str(self.height),
                      width=str(self.width))
        drawing = ET.SubElement(svg_root, 'g', style="fill-opacity:1.0; stroke:black;")

        for child in self.children:
            for children in child.to_svg_elems():
                drawing.append(children)

        return ET.tostring(svg_root)

import csv
def create_image(path):

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)

        drawing = SVGdrawing()
        offset = 20
        for idx, row in enumerate(reader):
            drawing.children += [ProgramState([offset, offset*idx], row)]

        print(drawing.to_svg())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
