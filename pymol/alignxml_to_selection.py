"""
Defines the pymol commands selectAlignment, displayAlignment, and displayAlignmentBlocks
"""
from xml.dom.minidom import *
from pymol import cmd, stored

#Pymol functions
def selectAlignment(alignFile, name1=None, name2=None):
    """usage: selectAlignment, [name1, [name2]]
    
    Defines two new selections based on the alignment given in alignFile.
    AlignFile is in the XML format used by CE and BioJava.

    If specified, the selections will be called name1 and name2. Otherwise the
    names will be taken from the alignment file.
    
    return the names of the two selections (sele_name1, sele_name2)
    """
    align = Alignment(alignFile)

    if name1 is None:
        name1 = align.name1[:4]
    if name2 is None:
        name2 = align.name2[:4]

    select1 = "%s and ( %s )" % (name1, align.getSelect1())
    select2 = "%s and ( %s )" % (name2, align.getSelect2())
    cmd.select("sele_"+name1, select1)
    cmd.select("sele_"+name2, select2)

    cmd.deselect()

    return ("sele_"+name1,"sele_"+name2,)

cmd.extend( "selectAlignment", selectAlignment )

def selectAlignmentBlocks(alignFile, name1=None, name2=None):
    """usage: selectAlignment, [name1, [name2]]
    
    Defines two new selections based on the alignment given in alignFile.
    AlignFile is in the XML format used by CE and BioJava.

    If specified, the selections will be called name1 and name2. Otherwise the
    names will be taken from the alignment file.
    
    return the names of the two selections (sele_name1, sele_name2)
    """
    align = Alignment(alignFile)

    if name1 is None:
        name1 = align.name1[:4]
    if name2 is None:
        name2 = align.name2[:4]

    blocks1 = align.getSelect1ByBlock()
    blocks2 = align.getSelect2ByBlock()
    selections = []
    for blk in xrange(len(blocks1)):
        select1 = "%s and ( %s )" % (name1, blocks1[blk])
        select2 = "%s and ( %s )" % (name2, blocks2[blk])

        align1="sele_%s_%s"%(name1,blk)
        align2="sele_%s_%s"%(name2,blk)
        selections.append(align1)
        selections.append(align2)

        cmd.select(align1,select1)
        cmd.select(align2,select2)
    cmd.deselect()

    return selections

cmd.extend( "selectAlignmentBlocks", selectAlignmentBlocks )


def displayAlignment(alignFile, name1, name2):
    """usage: displayAlignment alignFile.xml, name1, name2
    
    Reads an alignment from the specified XML file, then formats the objects
    name1 and name2 to show off the alignment
    """
    # Calculate selections
    (sele1,sele2) = selectAlignment(alignFile, name1, name2)

    align1=name1+"_aligned"
    align2=name2+"_aligned"

    cmd.create(align1, name1+" and "+sele1)
    cmd.create(align2, name2+" and "+sele2)

    cmd.show("cartoon", " or ".join([name1,name2,align1,align2]))
    cmd.set("cartoon_transparency", .5, " or ".join([name1,name2]))

    cmd.color("orange",align1)
    cmd.color("lightorange",name1)
    cmd.color("cyan",align2)
    cmd.color("palecyan",name2)

#    cmd.hide("everything", name1+" or "+name2)
#    cmd.show("ribbon", name1+" or "+name2)
#    cmd.set("ribbon_smooth",1)
#    cmd.set("ribbon_sampling",20)
#
#    cmd.color("grey",name1)
#    cmd.color("black",name2)
#
#    cmd.show("ribbon", name1)
#    cmd.show("ribbon", name2)
#    cmd.show("ribbon", align1)
#    cmd.show("ribbon", align2)
#
#    cmd.set("ribbon_width",4)
#    cmd.set("ribbon_width",8,align1+" or "+align2)
#
#    cmd.color("cyan",align1)
#    cmd.color("orange",align2)

cmd.extend( "displayAlignment", displayAlignment)


def displayAlignmentBlocks(alignFile, name1, name2):
    """Reads an alignment from the specified XML file, then formats the objects
    name1 and name2 to show off the alignment
    """

    fgColors1 = ["brightorange","raspberry"]
    bgColor1 = "lightorange"
    fgColors2 = ["skyblue","deepteal",]
    bgColor2 = "palecyan"

    # Calculate selections
    align = Alignment(alignFile)

    #display background
    cmd.show("cartoon", " or ".join([name1,name2]))
    cmd.set("cartoon_transparency", .3, " or ".join([name1,name2]))
    cmd.set("cartoon_rect_length", .5, " or ".join([name1,name2]))
    cmd.set("cartoon_oval_length", .75, " or ".join([name1,name2]))
    cmd.set("cartoon_loop_radius", .1, " or ".join([name1,name2]))
    cmd.color(bgColor1,name1)
    cmd.color(bgColor2,name2)

    #create blocks
    blocks1 = align.getSelect1ByBlock()
    blocks2 = align.getSelect2ByBlock()
    for blk in xrange(len(blocks1)):
        select1 = "%s and ( %s )" % (name1, blocks1[blk])
        select2 = "%s and ( %s )" % (name2, blocks2[blk])

        align1="%s_aligned_%s"%(name1,blk)
        align2="%s_aligned_%s"%(name2,blk)

        cmd.create(align1, name1+" and "+select1)
        cmd.create(align2, name2+" and "+select2)

        #display blocks
        cmd.show("cartoon", " or ".join([align1,align2]))
        cmd.set("cartoon_transparency", 0.0, " or ".join([align1,align2]))
        cmd.color(fgColors1[blk%len(fgColors1)],align1)
        cmd.color(fgColors2[blk%len(fgColors2)],align2)

cmd.extend( "displayAlignmentBlocks", displayAlignmentBlocks)


#Class to parse alignment xml
class Alignment:

    def __init__(self, file=None):
        self._blocks = []
        if file is not None:
            doc = parse(file)
            self.handleAlignmentXML(doc)

    def handleAlignmentXML(self, doc):
        afpchain = doc.getElementsByTagName("AFPChain")[0]
        self.handleAFPChain(afpchain)

    def handleAFPChain(self, chain):
        self.name1 = chain.attributes["name1"].value
        self.name2 = chain.attributes["name2"].value
        blocks = chain.getElementsByTagName("block")

        for block in blocks:
            self.handleBlock(block)

    def handleBlock(self, block):
        eqrs = block.getElementsByTagName("eqr")
        matrix = block.getElementsByTagName("matrix")
        shift = block.getElementsByTagName("shift")

        self._blocks.append( [self.handleEQR(eqr) for eqr in eqrs] )

    def handleEQR(self, eqr):
        pdb1 = eqr.attributes["pdbres1"].value
        pdb2 = eqr.attributes["pdbres2"].value
        chain1 = eqr.attributes["chain1"].value
        chain2 = eqr.attributes["chain2"].value
        #print("%s%s-%s%s"%(pdb1,chain1,pdb2,chain2))
        return (pdb1,chain1,pdb2,chain2)

    def __str__(self):
        s = "%s\t%s\n" % (self.name1, self.name2)
        for block in self._blocks:
            for eqr in block:
                s += "%s%s\t%s%s\n" % eqr
            s += "\n"
        return s

    def getSelect1(self):
        """Returns a pymol selector string selecting the residues of name1."""
        res = []
        for block in self._blocks:
            for (pdb1,chain1,pdb2,chain2) in block:
                res.append("( resi %s and chain %s )"%(pdb1,chain1))
        return " or ".join(res)

    def getSelect2(self):
        """Returns a pymol selector string selecting the residues of name2."""
        res = []
        for block in self._blocks:
            for (pdb1,chain1,pdb2,chain2) in block:
                res.append("( resi %s and chain %s )"%(pdb2,chain2))
        return " or ".join(res)

    def getSelect1ByBlock(self):
        return [" or ".join( \
            ["( resi %s and chain %s )"%(pdb1,chain1) \
                for (pdb1,chain1,pdb2,chain2) in block]) \
            for block in self._blocks]
    def getSelect2ByBlock(self):
        return [" or ".join( \
            ["( resi %s and chain %s )"%(pdb2,chain2) \
                for (pdb1,chain1,pdb2,chain2) in block]) \
            for block in self._blocks]


if __name__ == "__main__":
    file = "/Users/blivens/dev/bourne/1iu9 1h0r.xml"
    alignment = Alignment(file)
    print(str(alignment))
    print(__package__)
