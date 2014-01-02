#!/usr/bin/python
import sys
from pymol import cmd,util,stored

try:
    from geo import *

    def rename_h(selection="(all)"):
        """DESCRIPTION

    USAGE

    ARGUMENTS

    NOTES

    EXAMPLES

    AUTHOR

        Spencer Bliven
    """
        # iterate sele and elem h, print "/%s/%s/%s/%s/%s %s" % (model,state,chain,resn,name,ID)
        stored.mdp_hydrogens = []
        cmd.iterate("( %s ) and elem h"%selection,"stored.mdp_hydrogens.append((model,ID))")

        print "Found %d hydrogens in '%s'"%(len(stored.mdp_hydrogens),selection)
        hcache = {} #cache hydrogen names
        numchanged = 0

        for hydrogen in stored.mdp_hydrogens:

            if not hcache.has_key(hydrogen):
                heavy = "neighbor (%s and ID %s)" % hydrogen

                # Assign names to hydrogens attached to this heavy
                attachedH = assignHNames(heavy)
                for h in attachedH:
                    hcache[ (h.model,h.ID) ] = h

            try:
                hcache[hydrogen].alterName()
                numchanged += 1
            except KeyError:
                raise RuntimeError("Unable to assign name to model %s ID %s"%hydrogen)



        print("Renamed %d standard hydrogens. Be sure to check ligands and non-standard amino acids."%numchanged)

    def greekCmp(a,b):
        """Compare a and b based on abbreviations for greek letters

        A<B<G<D<E<Z<H

        Comparison is case insensitive and raises a ValueError if any other
        characters are present in a or b
        """
        order = "ABGDEZH"
        ai = [order.index(i) for i in a.upper()]
        bi = [order.index(i) for i in b.upper()]
        return cmp(ai,bi)

    def assignHNames(center,state=1):
        """assignHNames(single_atom_selection) -> [Atom] """

        # Store some information about the center atom and its neighbors
        stored.mdp_neighbor_coords = []
        cmd.iterate_state(int(state),"( %s )" % center,
                "stored.mdp_neighbor_coords.append( (model, chain, ID, resn,resi, name,elem,x,y,z) )")
        cmd.iterate_state(int(state),"neighbor ( %s )" % center,
                "stored.mdp_neighbor_coords.append( (model, chain, ID, resn,resi, name,elem,x,y,z) )")

        atoms = []
        for model, chain, ID, resn,resi, name,elem,x,y,z in stored.mdp_neighbor_coords:
            atoms.append( Atom(ID, model, state, chain, resn,resi, name, elem, x, y, z) )

        if len(atoms) < 1:
            return []

        # Switch based on center atom name
        centName = atoms[0].name

        # count number of hydrogens
        hydrogens = [atm for atm in atoms if atm.elem == "H"]
        heavy = [atm for atm in atoms if atm.elem != "H"]

        hNum = len(hydrogens)

        #print("/{0[0]}/{1}/?/{0[2]}/{0[3]} ({0[1]}) = ({0[5]},{0[6]},{0[7]})".format(coords[0],state))

        if hNum == 1:
            # Single hydrogens take their name from their attached atom
            hydrogens[0].name = "H"+centName[1:]

        elif hNum == 2:
            # Double hydrogens usually take their name from the attached atom plus
            # a number, with a few exceptions
            if centName == "N":
                # N-terminus
                hydrogens[0].name = "H"
                hydrogens[1].name = "H2"
            elif centName == "CA":
                #Glycine
                if len(heavy) == 3:
                    try:
                        n = [atm for atm in heavy if atm.name == "N"][0]
                        ca = [atm for atm in heavy if atm.name == "CA"][0]
                        c = [atm for atm in heavy if atm.name == "C"][0]
                    except:
                        raise RuntimeError("Missing backbone atoms around %s"%atoms[0])

                    hydrogens = orderbyplane(n,ca,c,*hydrogens)
                    hydrogens[0].name = "HA3"
                    hydrogens[1].name = "HA2"
            elif centName == "O":
                #Water
                hydrogens.sort(key=lambda a:(a.x,a.y,a.z))
                hydrogens[0].name = "H1"
                hydrogens[1].name = "H2"

            else:
                # Normal sidechain center

                # sort heavy atoms by sidechain position
                try:
                    heavy.sort(cmp=greekCmp,key=lambda a:a.name[1])
                except IndexError, e:
                    for hv in heavy:
                        if len(hv.name)<2:
                            print hv
                    raise e


                if len(heavy) < 1:
                    raise ValueError("Error: only 1 heavy atom found")
                elif len(heavy) == 2:
                    # Only 2 heavy atoms, so probably nitrogen
                    # Number as 1 & 2
                    hydrogens = orderbyvector(heavy[0],heavy[1], *hydrogens)
                    assert(len(hydrogens)==hNum)

                    for i in xrange(hNum):
                        hydrogens[i].name = "H%s%d" %( centName[1:],i+1 )
                elif len(heavy) == 3:
                    # tetrahedral center
                    hydrogens = orderbyplane(heavy[0],heavy[1],heavy[2],*hydrogens)
                    assert(len(hydrogens)==hNum)

                    # Most AAs number them (3,2), with a couple exceptions
                    if atoms[0].resn in ["LEU", "MET"]:
                        hydrogens[0].name = "H%s2" % centName[1:]
                        hydrogens[1].name = "H%s3" % centName[1:]
                    elif atoms[0].resn == "ARG" and centName in ["CB","CG"]:
                        hydrogens[0].name = "H%s2" % centName[1:]
                        hydrogens[1].name = "H%s3" % centName[1:]
                    elif atoms[0].resn == "ILE" and centName[:2] == "CG":
                        hydrogens[0].name = "H%s2" % centName[1:]
                        hydrogens[1].name = "H%s1" % centName[1:]
                    else:
                        hydrogens[0].name = "H%s3" % centName[1:]
                        hydrogens[1].name = "H%s2" % centName[1:]

                else:
                    raise ValueError("Error: {} heavy atoms bound to {}, but has 2 hydrogens".format(len(heavy)-1,atoms[0]))

        elif hNum == 3:
            if len(heavy) == 2:
                heavy.sort(cmp=greekCmp,key=lambda a:a.name[1])

                hydrogens = orderbyvector(heavy[0],heavy[1],*hydrogens)
                assert(len(hydrogens)==hNum)

                for i in xrange(hNum):
                    hydrogens[i].name = "H%s%d" % (centName[1:],i+1)
            else:
                raise ValueError("Error: unexpected geometry around atom {}".format(atoms[0]) )
        else:
            raise ValueError("Error: {} hydrogens on atom {}".format(hNum,atoms[0]) )


        # hydrogens should now all have updated names
        return hydrogens


    def orderbyplane(ca,cb,cg,*hydrogens):
        """Provides a stable ordering for two hydrogen atoms based on the positions
        of three heavy atoms.

        Returns the hydrogen atoms ordered like the following fischer diagram

        CA
        0-CB-1
        CG

        Assumes CB is roughly tetrahedral

        If more than two hydrogens are specified, orders them from left to right.
        """
        ref = Plane( Point(cb.x, cb.y, cb.z),
                Point(ca.x, ca.y, ca.z),
                Point(cg.x, cg.y, cg.z) )
        pts = [Point(h.x,h.y,h.z) for h in hydrogens]
        dists = [ref.distance_to(p)*ref.orientation(p) for p in pts]

        return zip(*sorted(zip(dists,hydrogens),reverse=True))[1]

    def orderbyvector(ca,cb,*hydrogens):
        """Provides a stable ordering of hydrogen atoms around a single bond.
        Starting with the hydrogen with minimal x coordinate, labels
        them in a counterclockwise manner (with the CA-CB vector pointing out of
        the page. For instance, with three hydrogens:

        CA
        2-CB-1
        0
        """
        caPt = Point(ca.x,ca.y,ca.z)
        cbPt = Point(cb.x,cb.y,cb.z)

        hydrogens = list(hydrogens)
        hydrogens.sort(key=lambda a:(a.x,a.y,a.z))
        hpts = [Point(h.x,h.y,h.z) for h in hydrogens]

        # project points along the vector, and sort them by angle
        frame = CylindricalReferenceFrame(cbPt, caPt, hpts[0])
        angles = [frame.from_global(h,False).coordinates()[1] for h in hpts]

        hydrogens = zip(*sorted(zip(angles,hydrogens)))[1]
        return hydrogens

    class Atom(object):
        """ Simple container for atom info"""
        def __init__(self, ID, model, state, chain, resn, resi, name, elem, x, y, z):
            self.model = model
            self.ID = ID
            self.state = int(state)
            self.chain = chain
            self.resn = resn
            self.resi = resi
            self.name = name
            self.elem = elem
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        def __repr__(self):
            return "Atom({0.ID},{0.model},{0.state},{0.chain},{0.resn},{0.resi},{0.name},{0.elem},{0.x},{0.y},{0.z})".format(self)
        def __str__(self):
            return "/{0.model}/{1}/{0.chain}/{0.resn}`{0.resi}/{0.name}#{0.ID}({0.elem})=({0.x},{0.y},{0.z})".format(self,self.state if self.state>1 else "")
        def __key(self):
            """Unique identifier, for equality"""
            return (self.model,self.ID,self.state)
        def __eq__(x,y):
            return type(x) == type(y) and x.__key() == y.__key()
        def __hash__(self):
            return hash(self.__key())
        def alterName(self):
            """Updates pymol with the name of this atom. Should be called after assigning self.name"""
            cmd.alter("{} and ID {}".format(self.model,self.ID), "name=\"%s\""%self.name )

    cmd.extend("rename_h",rename_h)


except:
    sys.stderr.write("Error: No geo module found. Install from https://github.com/sbliven/geometry-simple\n")
