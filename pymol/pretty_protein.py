#
# Pretty pretty proteins
#
# by Spencer Bliven

from pymol import cmd,util

def pretty_protein(sele="(all)"):
    """DESCRIPTION

    This is my default display. It displays the protein as cartoon, but
    highlights ligands and ions as sticks or spheres.

USAGE

    pretty_protein [selection]

AUTHOR

    Spencer Bliven
"""
    cmd.hide("lines",sele)
    cmd.hide("everything","( %s ) and solvent"%sele)
    cmd.show("cartoon",sele)
    # disulfides
    cmd.show("sticks","( %s ) and (cys/ca+cb+sg) and byres (cys/sg and bound_to cys/sg)"%sele)
    # ligands
    cmd.show("sticks","( %s ) and hetatm and not solvent and not hydrogen"%sele)
    # metals
    cmd.show("spheres","( %s ) and not elem c+n+o+h+s"%sele)
    # color carbon by chain & others by element
    util.cbc(sele)
    util.cnc(sele)

cmd.extend("pretty_protein",pretty_protein)
