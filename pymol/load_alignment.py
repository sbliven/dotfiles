#!/usr/bin/python
import sys
import os
import random
from pymol import cmd, stored

def load_alignment(filename,object1=None,object2=None,delimiter="_"):
    """DESCRIPTION

    Structural comparison tools from the PDB website can save aligned
    structures as a two-model structure. This function loads such a file and
    splits the structures into two pymol objects for easy comparison.

USAGE

    load_alignment filename[, object1, object2][, delimiter]

ARGUMENTS

    filename    Path to the PDB file
    object1     What to name the first model from the file [optional]
    object2     What to name the second model from the file [optional]
    delimiter   Delimiter which separates object1 and object2 in the filename.
                See DETAILS. [default '_']

DETAILS

    The input file must contain at least two states (MODEL lines in the PDB
    file). Additional states are ignored.

    If object1 and object2 are ommitted, the script will attempt to generate
    them based on the filename. The extension is first removed from the
    filename, then the name is split around the first instance of <delimiter>.
    Thus, alignment files which follow the convention "object1_object2.pdb"
    will be properly split without additional arguments.

EXAMPLES

    # Results in objects '1AX8.A' and '3PIV.A'
    load_alignment 1AX8.A_3PIV.A.pdb

    # Results in objects 'query' and 'target'
    load_alignment alignment.pdb, query, target

    # Results in objects '1AX8.A' and '3PIV.A'
    load_alignment 1AX8.A_vs_3PIV.A.pdb, delimiter="_vs_"
"""
    #load the file, which should generate a new object
    num_objects = len(cmd.get_names("objects"))
    cmd.load(filename)
    objects = cmd.get_names("objects")
    if len(objects) != num_objects+1:
        #an error occured with loading
        print("Error loading file")
        return
    obj = objects[-1]

    if cmd.count_states(obj) >= 2:
        #split the object
        split_alignment(obj,object1,object2,delimiter)

        #clean up
        cmd.delete(obj)
    else:
        print("Error: Expected 2 models in %s, but found %d."%
                filename,cmd.count_states(obj))
        return
cmd.extend("load_alignment", load_alignment)

def split_alignment(object,object1=None, object2=None,delimiter="_"):
    """DESCRIPTION

    Splits a two-state object into two separate objects.

USAGE

    split_alignment object[, object1, object2][, delimiter]

ARGUMENTS

    object      Two-state input object
    object1     What to name the first state from the object [optional]
    object2     What to name the second state from the object [optional]
    delimiter   Delimiter which separates object1 and object2 in the object name.
                See DETAILS. [default '_']

DETAILS

    The input object must contain at least two states. Additional states are
    ignored.

    If object1 and object2 are ommitted, the script will attempt to generate
    them based on the input object's name. The name is split around the first
    instance of <delimiter>.  Thus, objects which follow the convention
    "object1_object2" will be properly split without additional arguments.

EXAMPLES

    # Results in objects '1AX8.A' and '3PIV.A'
    split_alignment 1AX8.A_3PIV.A

    # Results in objects 'query' and 'target'
    split_alignment alignment, query, target

    # Results in objects '1AX8.A' and '3PIV.A'
    split_alignment 1AX8.A_vs_3PIV.A, delimiter="_vs_"

"""
    # check that we have at least two states
    if cmd.count_states(object) < 2:
        print("Error: input object must contain at least two states.")
        return

    prefix="split%04d_"%random.randint(0,9999) #make unique

    # guess output names
    if object1 is None and object2 is None:
        try:
            d = object.index(delimiter)
            object1=object[:d]
            object2=object[d+len(delimiter):]
        except:
            object1="%s_%04d"%(object,1)
            object2="%s_%04d"%(object,2)
            print "Warning: '%s' not found in '%s'. Using names %s and %s."%(delimiter,object1,object2)

    #split them
    cmd.split_states(object,prefix=prefix)

    #rename to output names
    cmd.set_name("%s%04d"%(prefix,1),object1)
    cmd.set_name("%s%04d"%(prefix,2),object2)

    #delete other states
    for o in cmd.get_names('objects'):
        if o.startswith(prefix):
            cmd.delete(o)

cmd.extend("split_alignment", split_alignment)
