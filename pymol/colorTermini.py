from pymol import cmd, stored
import sys

def getTermini(selection):
    stored.nterm = sys.maxint
    stored.cterm = -1
    command = "if int(resi) < stored.nterm:\n" \
        "\tstored.nterm=int(resi);\n"
    cmd.iterate(selection+" and n. ca and elem c", command)
    command = "if int(resi) > stored.cterm:\n" \
        "\tstored.cterm=int(resi)\n"
    cmd.iterate(selection+" and n. ca and elem c", command)
    return (stored.nterm, stored.cterm)
if sys.version_info > (2,5,0,'',0):
    cmd.extend("getTermini",lambda sele: sys.stdout.write("%s %s"%getTermini(sele)))

def colorTermini(selection):
    (nterm, cterm) = getTermini(selection)
    cmd.color("blue","%s and resi %d"%(selection,nterm))
    cmd.color("red","%s and resi %d"%(selection,cterm))
cmd.extend("colorTermini",colorTermini)
