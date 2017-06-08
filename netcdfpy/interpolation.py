from scipy.interpolate import griddata,NearestNDInterpolator
from netcdfpy.variable import Variable
from netcdfpy.util import log,error
import numpy as np
import abc
import scipy.interpolate as spint
import scipy.spatial.qhull as qhull
import itertools





def distance(lat1, lon1, lat2, lon2):
    """
    Computes the great circle distance between two points using the
    haversine formula. Values can be vectors.
    """
    # Convert from degrees to radians
    pi = 3.14159265
    lon1 = lon1 * 2 * pi / 360
    lat1 = lat1 * 2 * pi / 360
    lon2 = lon2 * 2 * pi / 360
    lat2 = lat2 * 2 * pi / 360
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = 6.367e6 * c
    return distance

class Interpolation(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,type):
        self.type=type


class NearestNeighbour(Interpolation):

    def __init__(self,interpolated_lons,interpolated_lats,var):
        self.index=self.create_index(interpolated_lons, interpolated_lats, var)
        super(NearestNeighbour, self).__init__("nearest")

    def create_index(self,interpolated_lons, interpolated_lats, var):
        lats = var.lats
        lons = var.lons

        dim_x = var.lons.shape[0]
        dim_y = var.lats.shape[1]
        npoints = len(interpolated_lons)

        lons_vec = np.reshape(lons, lons.size)
        lats_vec = np.reshape(lats, lats.size)
        points = (lons_vec, lats_vec)

        values = np.empty([dim_x, dim_y])
        x = []
        y = []
        ii = 0
        for i in range(0, dim_x):
            for j in range(0, dim_y):
                values[i, j] = ii
                x.append(i)
                y.append(j)
                ii = ii + 1

        values_vec = values.reshape(dim_x * dim_y)

        log(0, "Interpolating..." + str(len(interpolated_lons)) + " points")
        nn = NearestNDInterpolator(points, values_vec)
        log(0, "Interpolation finished")

        grid_points = []
        for n in range(0, npoints):
            ii = nn(interpolated_lons[n], interpolated_lats[n])
            ii = int(ii)
            i = x[ii]
            j = y[ii]
            # print ii,i,j
            grid_points.append([i, j])
        return grid_points

class Linear(Interpolation):

    def __init__(self,int_lons,int_lats,var):
        self.setup_weights(int_lons, int_lats, var)
        super(Linear, self).__init__("linear")

    def setup_weights(self, int_lons, int_lats, var):
        log(1, "Setup weights for linear interpolation")

        # Posistions in input file
        lons=var.lons
        lats=var.lats
        xy = np.zeros([lons.shape[0] * lons.shape[1], 2])
        xy[:, 0] = lons.flatten()
        xy[:, 1] = lats.flatten()

        # Target positions
        [Xi, Yi] = [np.asarray(int_lons), np.asarray(int_lats)]
        uv = np.zeros([len(Xi), 2])
        uv[:, 0] = Xi.flatten()
        uv[:, 1] = Yi.flatten()

        # Setup the weights
        self.interp_weights(xy, uv)

    def interp_weights(self,xy, uv, d=2):
        tri = qhull.Delaunay(xy)
        simplex = tri.find_simplex(uv)
        vertices = np.take(tri.simplices, simplex, axis=0)
        temp = np.take(tri.transform, simplex, axis=0)
        delta = uv - temp[:, d]
        bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
        self.vtx=vertices
        self.wts=np.hstack((bary, 1 - bary.sum(axis=1, keepdims=True)))

    def interpolate(self,values):
        values=values.flatten()
        return np.einsum('nj,nj->n', np.take(values, self.vtx), self.wts)

