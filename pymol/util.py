
import sys
from pymol import cmd, stored

def getrange(selection, expression):
    """range selection, expression
    
    'expression' must be a variable accessable from iterate, eg one of
    name, resn, resi, chain, alt, elem, q, b, segi, ATOM,HETATM, formal_charge,
    partial_charge, numeric_type, text_type, ID, vdw

    EXAMPLE:
    range all, b
    """

    stored._range = []
    cmd.iterate(selection, "stored._range.append( %s )" % expression)
    a=min(stored._range)
    b=max(stored._range)
    print("%f %f"%(a,b))
    return (a,b)
cmd.extend("range",getrange)

def loadInfo(selection, filename, column=1, header=0, sep=None):
    data = []
    f = open(filename,"r")
    for i in range(header):
        #discard header
        f.next()
    lineNr=header+1
    for line in f:
        fields = line.split(sep)
        if len(fields) < column:
            print("Error at line %d of %s: Too few columns"%(lineNr,filename))
        
        data.append(fields[column-1])
