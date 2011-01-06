#!/usr/bin/python
"""Functions for mapping COREX output onto pymol molecules.

Functions provided:
    * corexSAUpdateB obj, corexFile
        loads surface areas from the corex file into the b-factors of obj
    * corexDiffSAUpdateB obj, corex1, corex2
        loads the difference in surface areas between two corex runs into the
        b-factors of obj
    * colorByB obj
        Colors obj in a rainbow according to the b-factors.
    * corexColorBySSA obj, corexFile
        Helper function combining corexSAUpdateB and colorByB in a nice way
        Amides not reported by corex are colored white

By Spencer Bliven <sbliven@ucsd.edu>
"""

import sys
from pymol import cmd, stored

class CorexAtom:
    def __init__(self,resName, resNum, num, name, sa, pdbNum, pdbChain):
        self.name = name
        self.num = int(num)
        self.resName = resName
        self.resNum = int(resNum)
        self.sa = float(sa)
        self.pdbNum = int(pdbNum)
        self.pdbChain = pdbChain

    def __str__(self):
        return "%s\t%d\t%d\t%s\t%.2f\t%d\t%s" % (
            self.resName,
            self.resNum,
            self.num,
            self.name,
            self.sa,
            self.pdbNum,
            self.pdbChain,
            )

class CorexAtomInfo:
    def __init__(self,filename):
        self.atoms = self.parse(filename)

    def parse(self,filename):
        atoms = []
        file = open(filename,"r")
        if not file:
            sys.stderr.write("Error reading %s\n"%filename)
            #throw shit!
            return []
        file.next()
        file.next()
        lineNr=3
        for line in file:
            fields=line.split()
            if len(fields) == 0:
                continue
            if len(fields) != 7:
                sys.stderr.write("Bad format at line %d\n"%lineNr)
                #throw shit!
                continue
            atoms.append(CorexAtom(*fields))
            lineNr += 1
        return atoms

    def getAtoms(self):
        return self.atoms

def corexSAUpdateB(obj, corexFile):
    """Sets the B-factor column to the surface area specified in corexFile"""
    corex = CorexAtomInfo(corexFile)
    if corex is None:
        print "Error parsing %s" % corexFile
        return
    cmd.alter(obj, "b = -10")
    for atom in corex.getAtoms():
        sel = "%s and n. %s and i. %s and chain %s" % (
                obj, atom.name, atom.pdbNum, atom.pdbChain)
        cmd.alter( sel, "b = %f" % atom.sa)
    cmd.sort(obj)
cmd.extend("corexSAUpdateB", corexSAUpdateB)

def corexDiffSAUpdateB(obj, corex1, corex2):
    """Sets the B-factor column to the difference in surface areas between
    files corex1-corex2
    """
    corex1 = CorexAtomInfo(corex1)
    if corex1 is None:
        print "Error parsing %s" % corex1
        return

    corex2 = CorexAtomInfo(corex2)
    if corex2 is None:
        print "Error parsing %s" % corex2
        return

    atoms1 = corex1.getAtoms()
    atoms2 = corex2.getAtoms()

    if len(atoms1) != len(atoms2):
        print "Error: Corex files must have identical atoms"
        #TODO line up atoms1 and atoms2 somehow
    for i in xrange(len(atoms1)):
        sel = "%s and n. %s and i. %s and chain %s" % (
                obj, atoms1[i].name, atoms1[i].pdbNum, atoms1[i].pdbChain)
        cmd.alter( sel, "b = %f" % (atoms1[i].sa-atoms2[i].sa))
        print "b = %f" % (atoms1[i].sa-atoms2[i].sa)
    cmd.sort(obj)
cmd.extend("corexDiffSAUpdateB", corexDiffSAUpdateB)

def corexColorBySSA(obj, corexFile):
    """colorBySA -- color according to solvent-exposed surface area

    PARAMS

        obj The object to color

        corexFile A COREX info file giving the SSA

    RETURNS
        None.

    SIDE-EFFECTS
        Modifies the B-factor columns in obj
    """
    # Update B-factors
    corexSAUpdateB(obj, corexFile)

    cmd.select("missingSA", obj+" and b < 0")
    cmd.color("white","missingSA")
    cmd.spectrum("b", 'rainbow', "( %s and not missingSA )" % obj)
    cmd.disable("missingSA")
cmd.extend("corexColorBySSA",corexColorBySSA)


def colorByB(obj):
    cmd.spectrum("b", 'rainbow', "( %s )" % obj)
cmd.extend("color_by_b",colorByB)



if __name__ == "__main__":
    corex = CorexAtomInfo(sys.argv[1]);
    for atom in corex.getAtoms():
        print(atom)
