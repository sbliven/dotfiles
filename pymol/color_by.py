#!/usr/bin/python
"""
Pymol functions for coloring atoms

By Spencer Bliven <sbliven@ucsd.edu>
"""

import sys
from pymol import cmd, stored

def color_by_b(selection="all",palette='rainbow',**args):
    cmd.spectrum(expression="b", palette=palette, selection=selection,**args)
cmd.extend("color_by_b",color_by_b)

def color_by_q(selection="all",palette='rainbow',minimum=0,maximum=1,**args):
    cmd.spectrum(expression="q", palette=palette, selection=selection,minimum=minimum,maximum=maximum,**args)
cmd.extend("color_by_q",color_by_q)

