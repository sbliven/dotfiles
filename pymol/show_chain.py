#!/usr/bin/python
from pymol import cmd,util
from pretty_protein import pretty_protein

def show_chain(chain, selection="(all)", representation="cartoon"):
    """DESCRIPTION

    Shows the specified chain, hiding everything else.

USAGE

    show_chain chain [, selection [, representation ]]

ARGUMENTS

    chain = string: a chain specifier. May also use selection operators (eg A+B)

    selection = string: a selection-expression or name-pattern

    representation = lines, spheres, mesh, ribbon, cartoon, sticks,
       dots, surface, labels, extent, nonbonded, nb_spheres, slice,
       extent, slice, dashes, angles, dihedrals, cgo, cell, callback,
       or everything

NOTES

    If a selection is given, only shows/hides chains from within that selection.

    By default, the specified chain is shown using the cartoon representation.
    This can be changed using the representation parameter.

EXAMPLES

    show_chain A
    show_chain A, /4hhb
    show_chain B+D, /4hhb, sticks

AUTHOR

    Spencer Bliven
"""
    cmd.hide("( %s ) and not chain %s"%(selection,chain) );
    cmd.show(representation,"( %s ) and chain %s"%(selection,chain) );

cmd.extend("show_chain",show_chain)
