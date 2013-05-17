#!/usr/bin/python
from pymol import cmd,util

def chainbow_obj(selection="(all)"):
    """DESCRIPTION

    Colors each chain as a rainbow from N (blue) to C (red)

USAGE

    chainbow_obj [selection]

ARGUMENTS

    selection = the objects to be colored

NOTES

    Any objects present in the selection will be recolored completely. There is no
    way to color only part of an object.

EXAMPLES

AUTHOR

    Spencer Bliven
"""

    for object in cmd.get_object_list(selection):
        util.chainbow(object)
cmd.extend("chainbow_obj", chainbow_obj)
