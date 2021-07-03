#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from libs.constants import DEFAULT_ENCODING

TXT_EXT = '.txt'
ENCODE_METHOD = DEFAULT_ENCODING
FORMAT = "FORMAT_ICDAR"
class IcdarWriter:

    def __init__(self, folder_name, filename, img_size, database_src='Unknown', local_img_path=None):
        self.folder_name = folder_name
        self.filename = filename
        self.database_src = database_src
        self.img_size = img_size
        self.box_list = []
        self.local_img_path = local_img_path
        self.verified = False

    def add_bnd_box(self, x_min, y_min, x_max, y_max):
        bnd_box = {'xmin': x_min, 'ymin': y_min, 'xmax': x_max, 'ymax': y_max}
        self.box_list.append(bnd_box)

    def bnd_box_to_icdar_line(self, box):
        x_min = box['xmin']
        x_max = box['xmax']
        y_min = box['ymin']
        y_max = box['ymax']
        
        x1 = x4 = x_min
        x2 = x3 = x_max
        y1 = y2 = y_min
        y3 = y4 = y_max

        return x1, y1, x2, y2, x3, y3, x4, y4

    def save(self, target_file=None):

        out_file = None  # Update icdar .txt

        if target_file is None:
            out_file = open(
            self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)

        else:
            out_file = codecs.open(target_file, 'w', encoding=ENCODE_METHOD)

        # dataset format 
        out_file.write(FORMAT + '\n')
        for box in self.box_list:
            points = self.bnd_box_to_icdar_line(box)
            out_file.write("%d,%d,%d,%d,%d,%d,%d,%d\n"%(points))
        out_file.close()



class IcdarReader:

    def __init__(self, file_path, image):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.file_path = file_path

        img_size = [image.height(), image.width(),
                    1 if image.isGrayscale() else 3]

        self.img_size = img_size
        self.verified = False

        # # try:
        self.parse_icdar_format()
        # # except:
        # #     pass

    def get_shapes(self):
        return self.shapes

    def add_shape(self, label, x_min, y_min, x_max, y_max, difficult=False):
        points = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
        self.shapes.append((label, points, None, None, difficult))
    # def add_shape(self, x1, y1, x2, y2, x3, y3, x4, y4):
    #     points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    #     self.shapes.append(points)

    def get_dataset_format(): 
        return FORMAT

    def parse_icdar_format(self):
        bnd_box_file = open(self.file_path, 'r')
        for bndBox in bnd_box_file:
            if bndBox.strip() == FORMAT:
                continue
            x1, y1, x2, y2, x3, y3, x4, y4 = bndBox.strip().split(',')
            x_min = x1 if x1 == x4 else 0
            x_max = x2 if x2 == x3 else 0
            y_min = y1 if y1 == y2 else 0
            y_max = y3 if y3 == y4 else 0

            self.add_shape('text', int(x_min), int(y_min), int(x_max), int(y_max), False)
