from pymol import cmd, stored
import sys

def getTermini(selection):
    stored.nterm = dict()
    stored.cterm = dict()
    obj="\"sele\"" #TODO iterate through all objects in selection
    command = "if int(resi) < stored.nterm.get((%s,chain),sys.maxint):\n" \
        "\tstored.nterm[(%s,chain)]=int(resi);\n" %(obj,obj)
    cmd.iterate(selection+" and n. ca and elem c", command)
    command = "if int(resi) > stored.cterm.get((%s,chain),-1):\n" \
        "\tstored.cterm[(%s,chain)]=int(resi)\n" %(obj,obj)
    cmd.iterate(selection+" and n. ca and elem c", command)
    return (stored.nterm, stored.cterm)
if sys.version_info > (2,5,0,'',0):
    cmd.extend("getTermini",lambda sele: sys.stdout.write("%s %s"%getTermini(sele)))

def colorTermini(selection):
    (nterms, cterms) = getTermini(selection)
    for chainID in nterms.keys():
        cmd.color("blue","%s and resi %d"%(selection,nterms[chainID]))
        cmd.color("red","%s and resi %d"%(selection,cterms[chainID]))
        cmd.show("spheres","%s and resi %d+%d and n. ca"%(selection,nterms[chainID],cterms[chainID]))
cmd.extend("colorTermini",colorTermini)
