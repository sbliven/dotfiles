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
    """Mirror's Corex's version of what an "Atom" is.
    """
    def __init__(self,resName, resNum, num, name, sa, pdbResNum, chain, isHet=False):
        self.name = name
        self.num = int(num)

        self.res = CorexResidue(resName, resNum, chain)
        self.res.pdbNum = int(pdbResNum)

        self.sa = float(sa)

        self.isHet = isHet

    def __str__(self):
        return "%s\t%d\t%d\t%s\t%.2f\t%d\t%s" % (
            self.res.resName,
            self.res.resNum,
            self.num,
            self.name,
            self.sa,
            self.res.pdbNum,
            self.res.chain,
            )

class CorexResidue:
    def __init__(self,resName, resNum, chain):
        self.resName = resName
        self.resNum = int(resNum)
        self.chain = chain

        self.pdbNum = None

        self.exchangeRate = None
        self.intrinsicExchangeRate = None

        self.exposedAmideSA = None
        self.protectionFactor = None
        self.modifiedProtectionFactor = None
        self.minProtectionFactor = None

    def __str__(self):
        return "%s\t%d\t%s" % (self.resName, self.resNum, self.chain)

def assignPDBNums(srcResidues, dstResidues):
    """Tries to match residues in src and dst, setting the pdbNum in dst
    accordingly.
    """
    pdb = {}
    for res in srcResidues:
        pdb[res.resNum] = res.pdbNum
    for res in dstResidues:
        res.pdbNum = pdb.get(res.resNum)

class CorexAtomInfo:
    """Parses a corex .info file and stores the result as an array of
    CorexAtoms.
    """
    def __init__(self,filename):
        self.atoms = self.parse(filename)

    def parse(self,filename):
        atoms = []
        file = open(filename,"r")
        if not file:
            sys.stderr.write("Error reading %s\n"%filename)
            #throw shit!
            return []
        # Read number of atoms
        fields = file.next().split()
        numAtoms = int(fields[0])
        numHetAtoms = int(fields[2]) if len(fields)>2 else 0
        # Header
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
            if lineNr-2 > numAtoms: # Het atom
                atoms[-1].isHet = True
            lineNr += 1
        return atoms

    def getAtoms(self):
        return self.atoms

class CorexExchangeRates:
    """Parses a corex .Exchange_Rates file
    """
    def __init__(self, filename):
        self.residues = self.parse(filename)

    def parse(self, filename):
        residues = []
        file = open(filename, "r")
        if not file:
            sys.stderr.write("Error reading %s\n"%filename)
            #throw shit!
            return []
        file.next() #header
        lineNr=2
        for line in file:
            # ResName
            # ResNum
            # Ensemble_HDexchange_Rate
            # Intrinsic_HDexchange_Rate
            fields=line.split()
            if len(fields) == 0:
                continue
            if len(fields) != 5:
                sys.stderr.write("Bad format at line %d\n"%lineNr)
                #throw shit!
                continue
            res = CorexResidue(fields[0],fields[1],fields[4])
            res.exchangeRate = float(fields[2])
            res.intrinsicExchangeRate = float(fields[3])

            residues.append(res)
            lineNr += 1
        return residues

    def getResidues(self):
        return self.residues
 
class CorexProtectionFactors:
    """Parses a corex .Exchange_Rates file
    """
    def __init__(self, filename):
        self.residues = self.parse(filename)

    def parse(self, filename):
        residues = []
        file = open(filename, "r")
        if not file:
            sys.stderr.write("Error reading %s\n"%filename)
            #throw shit!
            return []
        file.next() #header
        lineNr=2
        for line in file:
            # ResName
            # ResNum
            # Famide_exp_Nat
            # ProtectionFactor
            # Modified_PF
            # Min_PF
            # Chain
            fields=line.split()
            if len(fields) == 0:
                continue
            if len(fields) != 7:
                sys.stderr.write("Bad format at line %d\n"%lineNr)
                #throw shit!
                continue

            res = CorexResidue(fields[0],fields[1],fields[6])
            res.exposedAmideSA = float(fields[2])
            res.protectionFactor = float(fields[3])
            res.modifiedProtectionFactor = float(fields[4])
            res.minProtectionFactor = float(fields[5])

            residues.append(res)
            lineNr += 1
        return residues

    def getResidues(self):
        return self.residues           # ResName

def corexSAUpdateB(obj, corexFile):
    """Sets the B-factor column to the surface area specified in corexFile"""
    corex = CorexAtomInfo(corexFile)
    if corex is None:
        print "Error parsing %s" % corexFile
        return
    cmd.alter(obj, "b = -10")
    for atom in corex.getAtoms():
        sel = "%s and n. %s and i. %s and chain %s" % (
                obj, atom.name, atom.res.pdbNum, atom.res.chain)
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
                obj, atoms1[i].name, atoms1[i].res.pdbNum, atoms1[i].res.chain)
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


def corexHDXRateUpdateB(obj, infoFile, exchangeRateFile):
    """Sets the B-factor column to the HDX rate.
    infoFile is used to establish the mapping between pdb and corex numbers
        (*.info).
    exchangeRateFile gives the HDX rates (*.Exchange_Rates).
    """
    hdx = CorexExchangeRates(exchangeRateFile)
    info = CorexAtomInfo(infoFile)

    if info is None:
        print "Error parsing %s" % infoFile
        return
    if hdx is None:
        print "Error parsing %s" % exchangeRateFile
        return

    assignPDBNums(
            [atom.res for atom in info.getAtoms() if not atom.isHet],
            hdx.getResidues()
        )

    cmd.alter(obj, "b = -10")
    for res in hdx.getResidues():
        if res.pdbNum is not None and res.exchangeRate is not None:
            sel = "%s and i. %s and chain %s" % (
                    obj,  res.pdbNum, res.chain)
            cmd.alter( sel, "b = %f" % res.exchangeRate)
    cmd.sort(obj)
cmd.extend("corexHDXRateUpdateB", corexHDXRateUpdateB)

def corexProtectionFactorUpdateB(obj, infoFile, pfFile):
    """Sets the B-factor column to the protection factors.
    infoFile is used to establish the mapping between pdb and corex numbers
        (*.info).
    pfFile gives the protection factors (*.Protection_Factors).
    """
    pf = CorexProtectionFactors(pfFile)
    info = CorexAtomInfo(infoFile)

    if info is None:
        print "Error parsing %s" % infoFile
        return
    if pf is None:
        print "Error parsing %s" % exchangeRateFile
        return

    assignPDBNums(
            [atom.res for atom in info.getAtoms() if not atom.isHet],
            pf.getResidues()
        )

    cmd.alter(obj, "b = -10")
    for res in pf.getResidues():
        if res.pdbNum is not None and res.modifiedProtectionFactor is not None:
            sel = "%s and i. %s and chain %s" % (
                    obj,  res.pdbNum, res.chain)
            cmd.alter( sel, "b = %f" % res.modifiedProtectionFactor)
    cmd.sort(obj)
cmd.extend("corexProtectionFactorUpdateB", corexProtectionFactorUpdateB)




if __name__ == "__main__":
    import optparse
    import os

    parser = optparse.OptionParser( usage="usage: python %prog corexFiles..." )
    (options, args) = parser.parse_args()

    """
    for filename in args:
        ext = os.path.splitext(filename)[1]
        if ext == ".info":
            corex = CorexAtomInfo(filename);
            for atom in corex.getAtoms():
                print(atom)
        elif ext == ".Exchange_Rates":
            corex = CorexExchangeRates(filename)
            for res in corex.getResidues():
                print("%s\t%f\t%f" % (str(res),
                    res.exchangeRate,
                    res.intrinsicExchangeRate,
                    ))
        elif ext == ".Protection_Factors":
            corex = CorexProtectionFactors(filename)
            for res in corex.getResidues():
                print("%s\t%f\t%f\t%f\t%f" % (str(res),
                    res.exposedAmideSA,
                    res.protectionFactor,
                    res.modifiedProtectionFactor,
                    res.minProtectionFactor,
                    ))
        else:
            print("Unknown extension for file %s"%filename)
    """

    hdx = CorexExchangeRates(args[1])
    info = CorexAtomInfo(args[0])
    assignPDBNums(
            [atom.res for atom in info.getAtoms() if not atom.isHet],
            hdx.getResidues()
        )
    for res in hdx.getResidues():
        print("%s\t%d\t%f\t%f" % (str(res), res.pdbNum,
            res.exchangeRate,
            res.intrinsicExchangeRate,
            ))

