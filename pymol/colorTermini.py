from pymol import cmd, stored
import sys

def getNterm(selection):
    stored.nterm = dict()
    obj="\"sele\"" #TODO iterate through all objects in selection
    command = "if int(resi) < stored.nterm.get((%s,chain),sys.maxint):\n" \
        "\tstored.nterm[(%s,chain)]=int(resi);\n" %(obj,obj)
    cmd.iterate(selection+" and n. ca and elem c", command)
    nterms= "(%s) and (%s)" %(selection,
            " or ".join( \
                ["(chain %s and resi %d)"%(chain, res) for ((obj,chain),res) in stored.nterm.items()] ) )
    return nterms

def getCterm(selection):
    stored.cterm = dict()
    obj="\"sele\"" #TODO iterate through all objects in selection
    command = "if int(resi) > stored.cterm.get((%s,chain),-1):\n" \
        "\tstored.cterm[(%s,chain)]=int(resi)\n" %(obj,obj)
    cmd.iterate(selection+" and n. ca and elem c", command)
    cterms= "(%s) and (%s)" %(selection,
            " or ".join( \
                ["(chain %s and resi %d)"%(chain, res) for ((obj,chain),res) in stored.cterm.items()] ) )
    return cterms

def selectNterm(selection="*",name="sele"):
    cmd.select(name,getNterm(selection))
cmd.extend("selectNterm",selectNterm)
def selectCterm(selection="*",name="sele"):
    cmd.select(name,getCterm(selection))
cmd.extend("selectCterm",selectCterm)
def selectTermini(selection="*",name="sele"):
    cmd.select(name,"(%s) or (%s)"%(getNterm(selection), getCterm(selection)) )
cmd.extend("selectTermini",selectTermini)

def colorTermini(selection="*"):
    nterms = getNterm(selection)
    cterms = getCterm(selection)
    cmd.color("blue",nterms)
    cmd.color("red",cterms)
    cmd.show("spheres","((%s) or (%s)) and n. ca"%(nterms,cterms))
cmd.extend("colorTermini",colorTermini)
