"""
SUMMARY

    A pymol script which runs all the other python scripts in the ~/.pymol directory.

    To add new scripts to pymol, just drop them in your .pymol directory. They
    will be automatically available in PyMol, without editing .pymolrc for each
    script.

USAGE

    Include the following line in your .pymolrc file:
        run ~/.pymol/autorun.py

    No additional run commands are needed for other scripts

AUTHOR

    Originally written by Spencer Bliven.

    This script is released to the public domain.
"""
import os, sys, cmd, glob
import inspect
import traceback

bin = os.path.expanduser("~/.pymol/")
sys.path.append(bin)

# Print each script as it's executed
verbose = False

# workaround for __file__ being set to pymol's init script
_myfile = inspect.currentframe().f_code.co_filename

for file in glob.glob(bin+"*.py"):
    if file != _myfile:
        if verbose:  print "run %s"%file
        try:
            __import__(os.path.basename(file)[:-3])
        except Exception:
            print "ERROR while importing %s"%file
            traceback.print_exc()

if verbose: print "Done"
