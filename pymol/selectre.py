# Select objects by regular expression
# By Spencer Bliven

from pymol import cmd
import re

def filter_object_list(pattern):
    regex = re.compile(pattern)
    objects = cmd.get_object_list()
    return [o for o in objects if regex.match(o)]

def disablere(pattern):
    for obj in filter_object_list(pattern):
        cmd.disable(obj)
cmd.extend('disablere',disablere)

def enablere(pattern):
    for obj in filter_object_list(pattern):
        cmd.enable(obj)
cmd.extend('enablere',enablere)

def deletere(pattern):
    for obj in filter_object_list(pattern):
        cmd.delete(obj)
cmd.extend('deletere',deletere)

def selectre(name,pattern=None):
    if pattern is None:
        pattern = name
        name = "sele"
    objects = " or ".join([obj for obj in filter_object_list(pattern)])
    cmd.select(name,objects)
cmd.extend('selectre',selectre)

# vim: sw=4 ts=4 et
