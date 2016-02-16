#! /usr/bin/env python

# author: Pierre Poulain
# contributors: Justine Guegan, Edithe Selwa
# last update: 20110414
#
# this Python script compute principal axes from a PDB file
# it also produces a .pml script for a nice rendering with Pymol

#==========================================================================
# import required modules
#==========================================================================
import sys
import os.path
import numpy
from pymol import cmd, stored
from pymol.cgo import *

#--------------------------------------------------------------------------
# compute principal axes
#--------------------------------------------------------------------------
def computeprincipalaxes(coord):
    """
    xyz: numpy nx3 array giving the input points
    returns: axis1, axis2, axis3, and center point
    """

    # compute geometric center
    center = numpy.mean(coord, 0)
    #print "geometric center coordinates:\n", center

    # center with geometric center
    coord = coord - center

    # compute principal axis matrix
    inertia = numpy.dot(coord.transpose(), coord)
    e_values, e_vectors = numpy.linalg.eig(inertia)
    # warning eigen values are not necessary ordered!
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eig.html
    #print "(unordered) eigen values:"
    #print e_values
    #print "(unordered) eigen vectors:"
    #print e_vectors

    #--------------------------------------------------------------------------
    # order eigen values (and eigen vectors)
    #
    # axis1 is the principal axis with the biggest eigen value (eval1)
    # axis2 is the principal axis with the second biggest eigen value (eval2)
    # axis3 is the principal axis with the smallest eigen value (eval3)
    #--------------------------------------------------------------------------
    for i in xrange(len(e_values)):
            # find biggest eigen value
            if e_values[i] == max(e_values):
                    eval1 = e_values[i]
                    axis1 = e_vectors[:,i]
            # find smallest eigen value
            elif e_values[i] == min(e_values):
                    eval3 = e_values[i]
                    axis3 = e_vectors[:,i]
            # middle eigen value
            else:
                    eval2 = e_values[i]
                    axis2 = e_vectors[:,i]

    #print "inertia axis are now ordered !"
    #print "Sizes: %f,%f,%f" % ( numpy.sqrt(numpy.dot(axis1.transpose(),axis1)),
    #        numpy.sqrt(numpy.dot(axis2.transpose(),axis2)),
    #        numpy.sqrt(numpy.dot(axis3.transpose(),axis3)),
    #        )

    # Normalize axes to the bounds of the coordinates
    proj1 = numpy.dot(coord,axis1)
    range1 = numpy.max(numpy.abs(proj1))
    proj2 = numpy.dot(coord,axis2)
    range2 = numpy.max(numpy.abs(proj2))
    proj3 = numpy.dot(coord,axis2)
    range3 = numpy.max(numpy.abs(proj3))
    #print "Ranges: %s, %s, %s" %(range3,range2,range3)
    return axis1*range1,axis2*range2,axis3*range3,center

def principalaxes(selection,name="axes",scale_factor=1,state=1,radius=.5,hlength=-1,hradius=-1):
    """Display the principal axes of the selection as arrows
    """

    xyz = []
    cmd.iterate_state(state,selection,"xyz.append( (x,y,z) )", space={'xyz':xyz} )

    #create coordinates array
    coord = numpy.array(xyz, float)

    axis1,axis2,axis3,center = computeprincipalaxes(coord)

    if hlength < 0:
        hlength = radius * 3
    if hradius < 0:
        hradius = hlength * .6

    start1 = -scale_factor * axis1 + center
    end1 = scale_factor * axis1 + center
    mid1 = -axis1/numpy.linalg.norm(axis1)*hlength + end1

    start2 = -scale_factor * axis2 + center
    end2 = scale_factor * axis2 + center
    mid2 = -axis2/numpy.linalg.norm(axis2)*hlength + end2

    start3 = -scale_factor * axis3 + center
    end3 = scale_factor * axis3 + center
    mid3 = -axis3/numpy.linalg.norm(axis3)*hlength + end3

    #axis1=  [
    #        BEGIN, LINES,
    #        COLOR, 1.0, 0.0, 0.0,
    #        VERTEX, start1[0],start1[1],start1[2],
    #        VERTEX, end1[0],end1[1],end1[2],
    #        END ]
    #axis2=  [
    #        BEGIN, LINES,
    #        COLOR, 0.0, 1.0, 0.0,
    #        VERTEX, start2[0],start2[1],start2[2],
    #        VERTEX, end2[0],end2[1],end2[2],
    #        END ]
    #axis3=  [
    #        BEGIN, LINES,
    #        COLOR, 0.0, 0.0, 1.0,
    #        VERTEX, start3[0],start3[1],start3[2],
    #        VERTEX, end3[0],end3[1],end3[2],
    #        END ]
    axis1 =  [
            CYLINDER, start1[0],start1[1],start1[2],
            mid1[0],mid1[1],mid1[2],
            radius,
            1.0,0.0,0.0,
            1.0,0.0,0.0,
            CONE, mid1[0],mid1[1],mid1[2],
            end1[0],end1[1],end1[2],
            hradius, 0.0,
            1.0,0.0,0.0,
            1.0,0.0,0.0,
            1.0,0.0
            ]
    axis2 =  [
            CYLINDER, start2[0],start2[1],start2[2],
            mid2[0],mid2[1],mid2[2],
            radius,
            0.0,1.0,0.0,
            0.0,1.0,0.0,
            CONE, mid2[0],mid2[1],mid2[2],
            end2[0],end2[1],end2[2],
            hradius, 0.0,
            0.0,1.0,0.0,
            0.0,1.0,0.0,
            1.0,0.0
            ]
    axis3 =  [
            CYLINDER, start3[0],start3[1],start3[2],
            mid3[0],mid3[1],mid3[2],
            radius,
            0.0,0.0,1.0,
            0.0,0.0,1.0,
            CONE, mid3[0],mid3[1],mid3[2],
            end3[0],end3[1],end3[2],
            hradius, 0.0,
            0.0,0.0,1.0,
            0.0,0.0,1.0,
            1.0,0.0
            ]
    cmd.load_cgo(axis1+axis2+axis3, name)
    #cmd.load_cgo(axes, name)
    #cmd.set('cgo_line_width', 4)

    ##--------------------------------------------------------------------------
    ## create .pml script for nice rendering in Pymol
    ## output usage
    ##--------------------------------------------------------------------------
    #print "the first principal axis is in red"
    #print "coordinates: ", axis1
    ##print "eigen value: ", eval1
    #print
    #print "the second principal axis is in green"
    #print "coordinates:", axis2
    ##print "eigen value:", eval2
    #print
    #print "the third principal axis is in blue"
    #print "coordinates:", axis3
    ##print "eigen value:", eval3
cmd.extend("principalaxes",principalaxes)
cmd.auto_arg[0]["principalaxes"] = [cmd.object_sc,"selection",", "]


try:
    # If the ellipsoid script is installed, add more functions
    import ellipsoid


    def principalellipsoid(selection, name="ellipsoid", scale_factor=1,
            state=1, color="red red green green blue blue",segments=40,**kwargs):
        """Fit an ellipsoid to the selection based on the principal axes
        """

        scale_factor = float(scale_factor)

        xyz = []
        cmd.iterate_state(state,selection,"xyz.append( (x,y,z) )", space={'xyz':xyz} )

        #create coordinates array
        coord = numpy.array(xyz, float)

        axis1,axis2,axis3,center = computeprincipalaxes(coord)


        a = numpy.linalg.norm(axis1)
        b = numpy.linalg.norm(axis2)
        c = numpy.linalg.norm(axis3)

        # Convert axes into transformation matrix
        M = numpy.vstack((axis1/a,axis2/b,axis3/c,center)).transpose()
        M = numpy.vstack((M,numpy.array([[0,0,0,1]])))
        # Convert to row-major array
        transf = M.reshape(-1).tolist()

        ellipsoid.ellipsoid(name,0,0,0,
                a*scale_factor, b*scale_factor, c*scale_factor,
                color=color, segs=segments, transformation=transf, **kwargs)

    cmd.extend("principalellipsoid",principalellipsoid)
    cmd.auto_arg[0]["principalellipsoid"] = [cmd.object_sc,"selection",", "]

except:
    pass
