"""A pymol script which runs all the other scripts in the ~/.pymol directory

in .pymolrc, include:
    run /Users/blivens/.pymol/run_all.py
"""
import os, sys, cmd, glob

bin = os.path.expanduser("~/.pymol/")
sys.path.append(bin)
for file in glob.glob(bin+"*.py"):
    if file != __file__:
        __import__(os.path.basename(file)[:-3])

