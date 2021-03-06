#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Researching generating gcode for the rembot
License is available in LICENSE
since: 2018-MAR-01
"""

import os
import sys
import datetime
from math import floor, ceil
import cv2 as cv
import numpy as np
import __version__

class GCode(object):
    ''' GCode generation object '''
    def __init__(self, safety_height=1, pre_script="", post_script="", output=lambda string: print(string)):
        self.last_x = None
        self.last_y = None
        self.last_z = None
        self.last_f = None
        self.last_gcode = None
        self.write = output
        self.pre_script = pre_script
        self.post_script = post_script
        self.safety_height = safety_height

    def begin(self):
        ''' Setup GCODE '''
        self.write(self.pre_script)
        self.write("M90 X0.0000 Y0.0000")

    def end(self):
        ''' End gcode generation '''
        self.write("M100")
        self.write(self.post_script)

    def move_common(self, _x=None, _y=None, _z=None, _f=None, gcode="G1"):
        '''
        Internal function for G0 and G1 moves
        _x: X absolute position
        _y: Y absolute position
        _z: Z Position of pen
        _f: F Feed rate / speed
        gcode: Gcode string
        '''
        gcode_string = ""
        string_x = ""
        string_y = ""
        string_z = ""
        string_f = ""

        if _x == None: _x = self.last_x
        if _y == None: _y = self.last_y
        if _z == None: _z = self.last_z
        if _f == None: _f = self.last_f

        if _x != self.last_x:
            string_x = " X%.4f" %_x
            self.last_x = _x

        if _y != self.last_y:
            string_y = " Y%.4f" %_y
            self.last_y = _y

        if _z != self.last_z:
            string_z = " Z%.4f" %_z
            self.last_z = _z

        if _f != self.last_f:
            string_f = " F%.4f" %_f
            self.last_f = _f

        if string_x == "" and string_y == "" and string_z == "" and string_f == "":
            return

        gcode_string = gcode
        self.last_gcode = gcode

        command = "".join([
            gcode_string,
            string_x,
            string_y,
            string_z,
            string_f
        ])

        if command:
            self.write(command)

    def move_rapid(self, _x=None, _y=None, _z=None, _f=None):
        '''
        Perform rapid move to specified coordinates
        _x: X absolute position
        _y: Y absolute position
        _z: Z Position of pen
        '''
        self.move_common(_x, _y, _z, _f, "G0")

    def safety(self):
        ''' Go to safe pen height / raise pen. Transitioning from drawing to moving '''
        self.move_rapid(_z=self.safety_height)

    def draw(self, _x=None, _y=None, _z=None):
        '''
        Perfrom drawing move at specified rate
        _x: X absolute position
        _y: Y absolute position
        _z: Z Position of pen
        '''
        self.move_common(_x, _y, _z=1)

class Generator(object):
    ''' Worker class for gcode generation '''
    EPSILON = 1e-5

    def __init__(self,
        image,
        pixel_size,
        pixel_step,
        split_step,
        safety_height,
        pre_script,
        post_script,
        x_offset,
        y_offset
        ):
        # GCode initializations
        self.gclass = None
        self.safety_height = safety_height
        self.pre_script = pre_script
        self.post_script = post_script

        # Image offset from origin
        self.x_offset = x_offset
        self.y_offset = y_offset

        # Pixel transforIMGion to real world units
        split_pixels = 0
        if split_step > self.EPSILON:
            pixel_step = int(pixel_step * split_step * 2)
            split_pixels = int(pixel_step * split_step)

        self.pixel_size = pixel_size
        self.pixel_step = pixel_step
        self.split_pixels = split_pixels

        # Get image properties
        self.image = image # greyscale image
        self.rows, self.cols = image.shape

    def generate(self):
        '''
        Generate gcode lists of gcode from given greyscale image
        return: list of gcodes
        '''
        gcodes = []
        self.gclass = GCode(
            safety_height=self.safety_height,
            pre_script=self.pre_script,
            post_script=self.post_script,
            output=lambda cmd: gcodes.append(cmd+"\r\n")
        )
        gclass = self.gclass

        gclass.begin()
        self.run()
        gclass.end()

        return gcodes

    def run(self):
        '''
        Move through rows and cols and generate code for lines
        '''
        gclass = self.gclass
        rows, cols = self.rows, self.cols
        recording = False

        for row in range(rows):
            for col in range(cols):
                # While recodring check if the next pixel either does not exist
                # or if it ends the line
                if recording:
                    try:
                        if self.image[row][col+1] == 0:
                            # draw to end of line
                            gclass.draw(_x=col,_y=row,_z=1)
                            recording = False
                    except IndexError:
                        # move to end of row
                        gclass.draw(_x=col,_y=row,_z=1)
                        recording = False          
                # Scan until beginning of a line
                else:
                    if self.image[row][col] == 255:
                        # If line is found start recording it
                        recording = True
                        # move to start of line
                        gclass.move_common(_x=col, _y=row, _z=0)

if __name__ == "__main__":
    pass
