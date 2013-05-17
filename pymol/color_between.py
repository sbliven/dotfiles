#!/usr/bin/python
from pymol import cmd, stored

def color_between(color,selection="(sele)"):
    """DESCRIPTION

    Given a selection of two residues, colors residues between them.

USAGE

    color_between color[, selection]

ARGUMENTS

    color       A pymol color name or number
    selection   A selection containing two residues bounding the region to
                color. [default: (sele)]
"""
    objects = cmd.get_object_list(selection)
    if len(objects) > 1:
        print "Error: Please select residues from one object only"
        return

    myspace = {'residues':{},'chains':{}}
    cmd.iterate(selection, "residues[resi] = 1; chains[chain] = 1",space=myspace)

    residues = [int(i) for i in myspace["residues"].keys()]
    if len(residues) != 2:
        print "Error: Please select exactly 2 residues"
        return
    residues.sort()
    print(residues)

    chains = myspace['chains'].keys()
    if len(chains) != 1:
        print "Error: Please select 2 residues on the same chain"
        return


    object = objects[0]
    chain = chains[0]
    cmd.color(color, "%s and chain %s and resi %d-%d"%(object,chain,residues[0],residues[1]))

cmd.extend("color_between", color_between)
