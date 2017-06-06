from scipy.interpolate import griddata
from netcdfpy.variable import Variable
from netcdfpy.util import log,error
import numpy as np
import abc


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

    @abc.abstractmethod
    def interpolated_values(self):
        raise NotImplementedError('users must define interpolated_values to use this base class')


class NearestNeighbour(Interpolation):

    def __init__(self):
        super(NearestNeighbour, self).__init__("nearest")



    def get_i_j(self, lat, lon, var):
        dist = distance(lat, lon, var.lats, var.lons)
        indices = np.unravel_index(dist.argmin(), dist.shape)
        X = var.lats.shape[0]
        Y = var.lats.shape[1]
        if (indices[0] > 0 and indices[0] < X - 1 and indices[1] > 0 and indices[1] < Y - 1):
            I = indices[0]
            J = indices[1]
        else:
            error("Interpolated point outside domain!")
            I = 0
            J = 0
        return I, J

    def interpolated_values(self, interpolated_lons, interpolated_lats, var):
        npoints = len(interpolated_lons)
        grid_points = []
        log(1, "Interpolation for:"+str(var.var_name))
        for n in range(0, npoints):
            j,i=self.get_i_j(interpolated_lats[n], interpolated_lons[n], var)
            print i,j,interpolated_lats[n], interpolated_lons[n],n,npoints
            grid_points.append([i,j])

        log(1, "Interpolation finished")

        return grid_points

    def griddata_values(self,field,interpolated_lons,interpolated_lats,var):

        lats = var.lats
        lons = var.lons

        lons_vec = np.reshape(lons, lons.size)
        lats_vec = np.reshape(lats, lats.size)
        points = (lons_vec, lats_vec)
        log(0,"Interpolation to lons:",str(interpolated_lons)+" lats:"+str(interpolated_lats)+" for " +str(var.var_name))
        interpolated_fields=np.empty([len(interpolated_lons),field.shape[2],field.shape[3],field.shape[4]])
        for t in range(0,field.shape[2]):
            for z in range(0,field.shape[3]):
                for m in range(0,field.shape[4]):
                    values=np.reshape(field[:, :, t, z, m], [field.shape[0],field.shape[1]])
                    values_vec = values.reshape(values.size)
                    grid_x = np.array(interpolated_lons)
                    grid_y = np.array(interpolated_lats)
                    xi = (grid_x, grid_y)

                    interpolated_field = griddata(points, values_vec, xi, method='nearest')
                    for i in range(0,len(interpolated_lons)):
                        interpolated_fields[i][t][z][m]=interpolated_field[i]

        log(0, "Interpolation finished")
        return interpolated_fields

    def griddata_index(self,field,interpolated_lons,interpolated_lats,var):
        lats = var.lats
        lons = var.lons

        dim_x=var.lons.shape[0]
        dim_y=var.lats.shape[1]
        npoints=len(interpolated_lons)

        lons_vec = np.reshape(lons,lons.size)
        lats_vec = np.reshape(lats,lats.size)
        points = (lons_vec, lats_vec)
        log(2,"Interpolation to lons:"+str(interpolated_lons) + " lats:" + str(interpolated_lats) + " for " + \
                                        str(var.var_name))


        values=np.empty([dim_x,dim_y])
        ii=0
        for i in range(0,dim_x):
            for j in range(0,dim_y):
                values[i,j]=ii
                ii=ii+1

        values_vec = values.reshape(dim_x*dim_y)
        grid_x = np.array(interpolated_lons)
        grid_y = np.array(interpolated_lats)
        xi = (grid_x, grid_y)

        log(3,"Dimensions: "+str(dim_x)+" "+str(dim_y)+" "+str(values_vec.shape[0])+" "+
            str(grid_x.shape[0])+" "+str(grid_y.shape[0]))
        interpolated_field = griddata(points, values_vec, xi, method='nearest')
        log(3, "griddata finished")

        grid_points=[]
        ii = 0
        for i in range(0, dim_x):
            for j in range(0, dim_y):
                for k in range(0,npoints):
                    if interpolated_field[k] == ii:
                        grid_points.append([i,j])
                ii=ii+1

        log(3, "Interpolation finished")
        return grid_points

class Bilinear(Interpolation):
   pass


class Linear(object):
   def get(self, x, y, xx):
      return yy
