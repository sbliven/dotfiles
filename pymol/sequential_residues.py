#!/usr/bin/python
# Written by Spencer Bliven
# based on http://pymolwiki.org/index.php/Zero_residues

from pymol import cmd, stored

def sequential_residues(sel1,offset=1):
        """
        PURPOSE: renumbers the selected residues sequentially, regardless of gaps
        USAGE: sequential_residues protName    # first residue is 1
        USAGE: sequential_residues protName, 5 # first residue is 5
        EXAMPLE: sequential_residues *
        """
        offset = int(offset)

        # A counter from offset up
        stored.offset = int(offset) - 1
        stored.curr_res = None

        cmd.alter(sel1,"""
if stored.curr_res != int(resi):
    stored.offset=stored.offset + 1
    stored.curr_res=int(resi)
    resi=stored.offset
else:
    resi=stored.offset
""" )
        cmd.sort()

# let pymol know about the function
cmd.extend("sequential_residues", sequential_residues)
