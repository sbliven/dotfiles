# PyMOL script to superimpose latices
# By Spencer Bliven, June 2015
# This code is public domain.

from pymol import cmd, cgo, xray
from math import cos, sin, radians, sqrt
import numpy
from supercell import supercell


def alignlattice(mobile,target, a,b,c,color1='blue',color2='red',name1='supercell1',name2='supercell2',prefix1="m",prefix2="n",withmates=1):
    mobilecopy = "mobile2"
    # Copy the mobile unit and get its superposition with the target
    cmd.create(mobilecopy,mobile)
    initial_mat = cmd.get_object_matrix(mobilecopy)
    cmd.super(mobilecopy,target)
    final_mat = cmd.get_object_matrix(mobilecopy)
    cmd.delete(mobilecopy)

    #TODO handle non-identity initial matrix
    orig_objects = set(cmd.get_object_list())

    # Generate primary grid
    supercell(a,b,c,target,color=color1,name=name1,withmates=withmates,prefix=prefix1,center=1,transformation=None)
    # Generate rotated grid
    supercell(a,b,c,mobile,color=color2,name=name2,withmates=withmates,prefix=prefix2,center=1,transformation=final_mat)


    colored_objects1 = set(cmd.get_object_list("(%s*)"%prefix1)) - orig_objects
    colored_objects2 = set(cmd.get_object_list("(%s*)"%prefix2)) - orig_objects

    for obj in colored_objects1:
        cmd.color(color1, obj)
    for obj in colored_objects2:
        cmd.color(color2, obj)

cmd.extend('alignlattice',alignlattice)
cmd.auto_arg[0]['alignlattice'] = [cmd.object_sc, 'mobile', '']
cmd.auto_arg[1]['alignlattice'] = [cmd.object_sc, 'target', '']

