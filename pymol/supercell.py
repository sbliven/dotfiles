'''
(c) 2010 Thomas Holder

PyMOL python script (load with `run supercell.py`)
Usage: See "help supercell" and "help symexpcell"
'''

from pymol import cmd, cgo, xray
from math import cos, sin, radians, sqrt
import numpy

def cellbasis(angles, edges):
	'''
	For the unit cell with given angles and edge lengths calculate the basis
	transformation (vectors) as columns of a 4x4 numpy.array
	'''
	rad = [radians(i) for i in angles]
	basis = numpy.identity(4)
	basis[0][1] = cos(rad[2])
	basis[1][1] = sin(rad[2])
	basis[0][2] = cos(rad[1])
	basis[1][2] = (cos(rad[0]) - basis[0][1]*basis[0][2])/basis[1][1]
	basis[2][2] = sqrt(1 - basis[0][2]**2 - basis[1][2]**2)
	edges.append(1.0)
	return basis * edges # numpy.array multiplication!

def supercell(a=1, b=1, c=1, object=None, color='blue', name='supercell', withmates=1,prefix="m",center=0,transformation=None,cutoff=None):
	'''
DESCRIPTION

    Draw a supercell, as requested by Nicolas Bock on the pymol-users
    mailing list (Subject: [PyMOL] feature request: supercell construction
    Date: 04/12/2010 10:12:17 PM (Mon, 12 Apr 2010 14:12:17 -0600))

USAGE

    supercell a, b, c [, object [, color [, name [, withmates]]]]

ARGUMENTS

    a, b, c = integer: repeat cell in x,y,z direction a,b,c times
    {default: 1,1,1}

    object = string: name of object to take cell definition from

    color = string: color of cell {default: blue}

    name = string: name of the cgo object to create {default: supercell}

    withmates = bool: also create symmetry mates in displayed cells
    {default: 1}

    prefix = string: prefix for the symmetry mates {default: m}

    center = boolean: If 1, indicates that the lattice should be centered on the
    origin, as opposed to having the corner at the origin cell. {default: 0}

    transformation = list: a 16-element list giving the 4x4 transformation
    matrix, as described in get_object_matrix() {default: identity matrix}

    cutoff = int: restrict symmetry mates to within cutoff angstroms of the origin.
    Use 0 to generate all symmetry mates. {default: 0}
SEE ALSO

    show cell

    cmd
	'''
	if object is None:
		object = cmd.get_object_list()[0]
	withmates = int(withmates)

	sym = cmd.get_symmetry(object)
	if sym is None:
		print("No symmetry operators found")
		return

	cell_edges = sym[0:3]
	cell_angles = sym[3:6]

	basis = cellbasis(cell_angles, cell_edges)

	if transformation is not None:
		transmat = transformation_to_numpy(transformation)
	assert isinstance(basis, numpy.ndarray)

	ts = list()
	a = int(a)
	b = int(b)
	c = int(c)
	if int(center) == 0:
		astart = 0
		bstart = 0
		cstart = 0
	else:
		#TODO Maybe would be more useful to center at the asymmetric unit?
		# For now, center on the origin cell.
		astart = (1-a)/2
		bstart = (1-b)/2
		cstart = (1-c)/2
	for i in range( astart,astart+a ):
		for j in range( bstart,bstart+b ):
			for k in range( cstart,cstart+c ):
				ts.append([i,j,k])

	obj = [
		cgo.BEGIN,
		cgo.LINES,
		cgo.COLOR,
	]
	obj.extend(cmd.get_color_tuple(color))

	for t in ts:
		# draw bounding box around cell t
		shift = basis[0:3,0:3] * t
		shift = shift[:,0] + shift[:,1] + shift[:,2]

		for i in range(3):
			# vi is direction of the edges to draw
			vi = basis[0:3,i]
			# vj are starting points for the four edges in that direction
			vj = [
				numpy.array([0.,0.,0.]),
				basis[0:3,(i+1)%3],
				basis[0:3,(i+2)%3],
				basis[0:3,(i+1)%3] + basis[0:3,(i+2)%3]
			]
			for j in range(4):
				start = shift + vj[j]
				end = start + vi

				if transformation is not None:
					start = numpy.dot(transmat, numpy.append(start,1))[:3]
					end   = numpy.dot(transmat, numpy.append(end  ,1))[:3]

				obj.append(cgo.VERTEX)
				obj.extend(start.tolist())
				obj.append(cgo.VERTEX)
				obj.extend(end.tolist())

		if withmates:
			symexpcell('%s%d%d%d_' % (prefix,t[0]-astart,t[1]-bstart,t[2]-cstart), object, *t,transformation=transformation,cutoff=cutoff)

	obj.append(cgo.END)

	cmd.delete(name)
	cmd.load_cgo(obj, name)

def symexpcell(prefix='mate', object=None, a=0, b=0, c=0,transformation=None,cutoff=None):
	'''
DESCRIPTION

    Creates all symmetry-related objects for the specified object that
    occur with their bounding box center within the unit cell.

USAGE

    symexpcell prefix, object, [a, b, c]

ARGUMENTS

    prefix = string: prefix of new objects

    object = string: object for which to create symmetry mates

    a, b, c = integer: create neighboring cell {default: 0,0,0}

    transformation = list: list of 16 floats giving the transformation matrix
    to apply to the generated symmetry mates {default: identity matrix}

    cutoff = int: restrict symmetry mates to within cutoff angstroms of the origin.
    Use 0 to generate all symmetry mates. {default: 0}
SEE ALSO

    symexp, http://www.pymolwiki.org/index.php/SuperSym
	'''
	#print "symexpcell %s,%s,%d,%d,%d,%s"%(prefix,object,int(a),int(b),int(c),transformation)
	if object is None:
		object = cmd.get_object_list()[0]
	if cutoff is not None:
		cutoff = int(cutoff)
		if cutoff <= 0: cutoff = None

	sym = cmd.get_symmetry(object)
	cell_edges = sym[0:3]
	cell_angles = sym[3:6]
	spacegroup = sym[6]

	basis = cellbasis(cell_angles, cell_edges)

	extent = cmd.get_extent(object)
	center = sum(numpy.array(extent)) * 0.5
	center = numpy.append(center,1.0).reshape(4,1)
	center_cell = numpy.linalg.inv(basis) * center

	extra_shift = numpy.array([[float(i)] for i in (a,b,c)])

	origin = numpy.array([[0,0,0,1]]).T
	if transformation is not None:
		transmat = transformation_to_numpy(transformation)
		#print "%s\n*\n%s\n=\n%s\n" % (origin,transmat,
		#		numpy.dot(numpy.linalg.inv(transmat),origin) )
		origin = numpy.dot(numpy.linalg.inv(transmat),origin)

	i = 0
	matrices = xray.sg_sym_to_mat_list(spacegroup)
	for mat in matrices:
		i += 1

		mat = numpy.array(mat)
		shift = numpy.floor(numpy.dot(mat, center_cell))
		mat[0:3,3] -= shift[0:3,0]
		mat[0:3,3] += extra_shift[0:3,0]

		mat = numpy.dot(numpy.dot(basis, mat), numpy.linalg.inv(basis) )
		mat_list = list(mat.flat)

		new_center = numpy.dot(mat,center)
		#print "%s\n* (%d)\n%s\n=\n%s\n" % (center,i,mat, new_center)

		if cutoff is not None:
			dist = new_center - origin
			dist = numpy.dot(dist.T,dist)
			if dist > cutoff**2:
				#print "Skipping %d%d%d_%d at distance %f" % (a,b,c,i,sqrt(dist))
				continue

		name = '%s%d' % (prefix, i)
		cmd.create(name, object)
		cmd.transform_object(name, mat_list)
		# Apply extra transformation afterwards
		if transformation is not None:
			cmd.transform_object(name, transformation)
		cmd.color(i+1, name)

cmd.extend('symexpcell', symexpcell)
cmd.extend('supercell', supercell)

def transformation_to_numpy(transformation):
	if len(transformation) != 16:
		print "Invalid transformation. Expect 16-element transformation matrix, found %d."%len(transformation)
		return None

	mat = numpy.array(transformation).reshape(4,4)
	return mat

def numpy_to_transformation(mat):
	return mat.reshape(-1).tolist()


# tab-completion of arguments
cmd.auto_arg[3]['supercell'] = [ cmd.object_sc, 'object', '']

# vim:ts=4 sw=4 noet
