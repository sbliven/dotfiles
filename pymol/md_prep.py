#!/usr/bin/python
from pymol import cmd,util

def rename_h(selection="(all)"):
    """DESCRIPTION

USAGE

ARGUMENTS

NOTES

EXAMPLES

AUTHOR

    Spencer Bliven
"""
    mappings = {
            #"resn" : ["H01","H02",...]
            "ALA": ["HB1","H","HA","HB3","HB2"],
            "ARG" : ["HH11","H","HA","HB2","HG2","HD2","HE","HH12","HH21","HB3","HG3","HH12"],
            "ASN" : [],
            "ASP" : [],
            "CYS" : [],
            "GLN" : [],
            "GLU" : [],
            "GLY" : [],
            "HIS" : [],
            "ILE" : [],
            "LEU" : [],
            "LYS" : [],
            "MET" : [],
            "PHE" : [],
            "PRO" : [],
            "SER" : [],
            "THR" : [],
            "TRP" : [],
            "TYR" : [],
            "VAL" : [],
            }

    for resn, names in mappings.items():
        for i in xrange(len(names)):
            cmd.alter("( %s ) and resn %s and name H%02d" % (selection,resn,i+1),
                    "name=\"%s\"" % names[i] )

    print("Renamed standard hydrogens. Be sure to check ligands and non-standard amino acids.")

cmd.extend("rename_h",rename_h)

