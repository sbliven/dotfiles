# PyMOL script to superimpose latices
# By Spencer Bliven, June 2015
# This code is public domain.
#
# Requires a modified version of the supercell script which supports the center, transformation, and cutoff arguments

from pymol import cmd, cgo, xray
from math import cos, sin, radians, sqrt
import numpy
from supercell import supercell


def alignlattice(target,mobile, a,b,c,color1='blue',color2='red',name1='supercell1',name2='supercell2',prefix1="m",prefix2="n",withmates=1,cutoff=None):
    '''
DESCRIPTION

    Align two lattices. This facilitates the comparison of lattice contacts.

USAGE

    alignlattice target, mobile, a, b, c, [color1/2, name1/2, prefix1/2, withmates, cutoff]

ARGUMENTS

    target = string: name of object to generate the first lattice. This lattice
    is generated aligned to the original coordinates.

    mobile = string: name of the second object. The generated lattice will
    align to the original object.

    a, b, c = integer: repeat cell in x,y,z direction a,b,c times
    {default: 1,1,1}

    color1/2 = string: color of unit cell cgo objects {default: blue/red}

    name1/2 = string: name of the cgo object to create {default: supercell1/2}

    prefix1/2 = string: prefix for the symmetry mates {default: m/n}

    withmates = bool: also create symmetry mates in displayed cells
    {default: 1}

    cutoff = int: restrict symmetry mates to within cutoff angstroms of the origin.
    Use 0 to generate all symmetry mates. {default: 0}

SEE ALSO

    show cell

    cmd
	'''
    # Check that selections contain a single object each
    mobileobj = "(byobj (%s))" % mobile
    targetobj = "(byobj (%s))" % target

    if len(cmd.get_object_list(mobileobj)) != 1:
        print("Expected single object for %s" % mobile)
        return
    if len(cmd.get_object_list(targetobj)) != 1:
        print("Expected single object for %s" % target)
        return

    mobilecopy = "mobile2823" #todo use unique name
    # Copy the mobile unit and get its superposition with the target
    cmd.create(mobilecopy,mobile)
    initial_mat = cmd.get_object_matrix(mobilecopy)
    cmd.super(mobilecopy,target)
    final_mat = cmd.get_object_matrix(mobilecopy)
    cmd.delete(mobilecopy)

    #TODO handle non-identity initial matrix
    orig_objects = set(cmd.get_object_list())

    # Generate primary grid
    supercell(a,b,c,targetobj,color=color1,name=name1,withmates=withmates,prefix=prefix1,center=1,transformation=None,cutoff=cutoff)
    # Generate rotated grid
    supercell(a,b,c,mobileobj,color=color2,name=name2,withmates=withmates,prefix=prefix2,center=1,transformation=final_mat,cutoff=cutoff)

    colored_objects1 = set(cmd.get_object_list("(%s*)"%prefix1)) - orig_objects
    colored_objects2 = set(cmd.get_object_list("(%s*)"%prefix2)) - orig_objects

    for obj in colored_objects1:
        cmd.color(color1, obj)
    for obj in colored_objects2:
        cmd.color(color2, obj)

cmd.extend('alignlattice',alignlattice)
cmd.auto_arg[0]['alignlattice'] = [cmd.object_sc, 'mobile', '']
cmd.auto_arg[1]['alignlattice'] = [cmd.object_sc, 'target', '']

