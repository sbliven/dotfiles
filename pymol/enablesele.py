# Disable or enable selected objects
# By Spencer Bliven

from pymol import cmd

def disablesele(selection="sele"):
    for obj in cmd.get_object_list("(%s)"%selection):
        cmd.disable(obj)
cmd.extend(disablesele)

def disablenotsele(selection="sele"):
    for obj in cmd.get_object_list("(not byobj (%s))"%selection):
        cmd.disable(obj)
cmd.extend(disablenotsele)


def enablesele(selection="sele"):
    for obj in cmd.get_object_list("(%s)"%selection):
        cmd.enable(obj)
cmd.extend(enablesele)


