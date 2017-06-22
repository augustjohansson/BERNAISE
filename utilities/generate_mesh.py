__author__ = "Asger J. S Bolet <asgerbolet@gmail.com>"
__date__ = "2017-04-28"
__copyright__ = "Copyright (C) 2017 " + __author__
__license__ = "MIT"

''' "StoreMeshHDF5(mesh, meshpath)",
"StraightCapilar(res, height, length, usemshr)" and 
"BarbellCapilar(res, diameter, length)" 
'''

import dolfin as df
import mshr as mshr
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def StoreMeshHDF5(mesh, meshpath):
    '''
    Function that stores generated mesh in both "HDMF5"
    (.h5) format and in "XDMF" (.XMDF) format.
    '''
    meshpathhdf5 = meshpath + ".h5"
    hdf5 = df.HDF5File(mesh.mpi_comm(), meshpathhdf5, "w")
    if rank == 0:
        print 'Storing the mesh in /meshes'
    hdf5.write(mesh, "mesh")
    hdf5.close()
    meshpathxdmf = meshpath + "_xdmf.xdmf"
    xdmff1 = df.XDMFFile(mesh.mpi_comm(), meshpathxdmf)
    xdmff1.write(mesh)
    if rank == 0:
        print 'Done.'


def StraightCapilar(res=10, height=1, length=5, usemshr=False):
    '''
    Function That Generates a mesh for a straight capilar,
    defualt meshing method is dolfin's "RectangleMesh" but have option for mshr.
    Note: Should be run form "BERNAISE/utilies/" in order to work.
    Note: The generarted mesh is storred in "BERNAISE/meshes/".
    '''
    if usemshr: # use mshr for the generation
        if rank == 0:
            print "Genrating mesh using the mshr-tool"
        # Define coners of Rectangle
        a = df.Point(0, 0)
        b = df.Point(height, length)
        domain = mshr.Rectangle(a, b)
        mesh = mshr.generate_mesh(domain, res)
        meshpath = "../meshes/StraightCapilarMshr_h" + str(height) + "_l" + \
                     str(length) + "_res" + str(res)
        if rank == 0:
            print "Done."
    else: # use the dolfin build in function
        if rank == 0:
            print "Genrating mesh using the dolfin build in function"
        # Define coners of rectangle/capilar
        a = df.Point(0, 0)
        b = df.Point(height, length)
        # Setting the reselution
        if height <= length:
            numberofpointsheight = res
            numberofpointslength = res*int(length/height)
        else:
            numberofpointsheight = res*int(height/length)
            numberofpointslength = res
        mesh = df.RectangleMesh(a, b, numberofpointsheight, numberofpointslength)
        meshpath = "../meshes/StraightCapilarDolfin_h" + str(height) + "_l" + \
                     str(length) + "_res" + str(res)
        if rank == 0:
            print "Done."
    StoreMeshHDF5(mesh, meshpath)

def BarbellCapilar(res=50, diameter=1., length=5.):
    '''
    Function That Generates a mesh for a barbell capilar,
    Meshing method is mshr.
    Note: Should be run form "BERNAISE/utilies/" in order to work.
    Note: The generarted mesh is storred in "BERNAISE/meshes/".
    '''
    if rank == 0:
        print "Genrating mesh using the mshr-tool"

    inletdiameter = diameter*5.
    inletlength = diameter*4.

    # Define coners of "capilar"
    a = df.Point(-diameter/2., -length/2-inletlength/2.)
    b = df.Point(diameter/2., length/2+inletlength/2.)
    capilar = mshr.Rectangle(a, b)
    # Define coners of "leftbell
    c = df.Point(-inletdiameter/2., -length/2-inletlength)
    d = df.Point(inletdiameter/2., -length/2)
    leftbell = mshr.Rectangle(c, d)
    # Define coners of "rightbell"
    e = df.Point(-inletdiameter/2., length/2)
    f = df.Point(inletdiameter/2., length/2+inletlength)
    rightbell = mshr.Rectangle(e, f)

    domain = capilar +leftbell +rightbell
    mesh = mshr.generate_mesh(domain, res)
    meshpath = "../meshes/BarbellCapilarDolfin_d" + str(diameter) + "_l" + \
                 str(length) + "_res" + str(res)
    if rank == 0:
        print "Done."
    StoreMeshHDF5(mesh, meshpath)

def main():
    StraightCapilar()
    BarbellCapilar()


if __name__ == "__main__":
    main()
 