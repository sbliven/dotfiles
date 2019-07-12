# Pymol script to save a selection string
from pymol import cmd,stored

@cmd.extend
def toselect(selection="sele",quiet=False,_self=cmd):
    """
DESCRIPTION

USAGE

ARGUMENTS
"""
    stored._toselect = []
    cmd.iterate(selection, "stored._toselect.append( (model, segi, chain, resi) )")

    root = {}
    for terms in stored._toselect:
        group_heirarchically(terms,root)

    expressions = []
    for model, segidict in root.items():
        for segi, chaindict in segidict.items():
            for chain, resilist in chaindict.items():
                #TODO buggy if complex sort order. Should really map onto sorted residue list to determine sequence
                resis = combine_resi(resilist)
                expr = "/{}/{}/{}/{}".format(model,segi,chain,resis)
                expressions.append(expr)
    selectstr = " or ".join(expressions)
    if not quiet:
        print(selectstr)
    return selectstr
cmd.auto_arg[0]['toselect'] = [cmd.object_sc, 'selection', '']

def group_heirarchically(terms,root):
    if len(terms) < 2:
        raise Exception("Too short")
    elif len(terms) == 2:
        root.setdefault(terms[0], []).append(terms[1])
    else:
        sub = root.setdefault(terms[0], dict())
        group_heirarchically(terms[1:], sub)
    return root

def combine_resi(resilist):
    if len(resilist) < 1:
        return ""

    groups = []


    start = None
    end = None
    for r in resilist:
        # parse
        try:
            resv = int(r)
            if start is None:
                start = resv
                end = resv
            elif end <= resv <= end+1:
                #next sequential residue
                end = resv
            else:
                # non-sequential, so output
                if start == end:
                    groups.append(str(start))
                else:
                    groups.append( "{}-{}".format(start,end) )
                start = resv
                end = resv
        except:
            #insertion code; skip it
            if start is not None:
                if start == end:
                    groups.append(str(start))
                else:
                    groups.append( "{}-{}".format(start,end) )
                start = None
            groups.append(r)

    if start is not None:
        if start == end:
            groups.append(str(start))
        else:
            groups.append( "{}-{}".format(start,end) )

    return "+".join(groups)
