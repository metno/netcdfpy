from scipy.interpolate import griddata
from netcdfpy.variable import Variable
import numpy as np
import abc

class Interpolation(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,type):
        self.type=type

    @abc.abstractmethod
    def interpolated_values(self):
        raise NotImplementedError('users must define interpolated_values to use this base class')

class NearestNeighbour(Interpolation):

    def __init__(self):
        print "Init NearestNeighbour"
        super(NearestNeighbour, self).__init__("nearest")


    def __interpolated_values__(self,field,interpolated_lons,interpolated_lats,var):

        lats = var.lats
        lons = var.lons

        lons_vec = np.reshape(lons, lons.size)
        lats_vec = np.reshape(lats, lats.size)
        points = (lons_vec, lats_vec)
        print "Interpolation to lons:",str(interpolated_lons)+" lats:"+str(interpolated_lats)+" for " +str(var.var_name)
        interpolated_fields=np.empty([len(interpolated_lons),field.shape[2],field.shape[3],field.shape[4]])
        for t in range(0,field.shape[2]):
            for z in range(0,field.shape[3]):
                for m in range(0,field.shape[4]):
                    values=np.reshape(field[:, :, t, z, m], [field.shape[0],field.shape[1]])
                    values_vec = values.reshape(values.size)
                    print values.shape
                    print values_vec.shape
                    grid_x = np.array(interpolated_lons)
                    grid_y = np.array(interpolated_lats)
                    xi = (grid_x, grid_y)

                    print "interpolating ",t,z,m
                    interpolated_field = griddata(points, values_vec, xi, method='nearest')
                    for i in range(0,len(interpolated_lons)):
                        print interpolated_field.shape
                        print interpolated_field[i]
                        print interpolated_fields[i][t][z][m]
                        interpolated_fields[i][t][z][m]=interpolated_field[i]
                    print "done interpolating"

            return interpolated_fields

    def interpolated_values(self,field,interpolated_lons,interpolated_lats,var):
        lats = var.lats
        lons = var.lons

        dim_x=739
        dim_y=949
        npoints=len(interpolated_lons)

        lons_vec = np.reshape(lons,lons.size)
        lats_vec = np.reshape(lats,lats.size)
        points = (lons_vec, lats_vec)
        print "Interpolation to lons:", str(interpolated_lons) + " lats:" + str(interpolated_lats) + " for " + \
                                        str(var.var_name)


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

        print "Interpolating "
        interpolated_field = griddata(points, values_vec, xi, method='nearest')

        grid_points=[]
        ii = 0
        for i in range(0, dim_x):
            for j in range(0, dim_y):
                for k in range(0,npoints):
                    if interpolated_field[k] == ii:
                        print "Found points ",i,j,ii
                        grid_points.append([i,j])
                ii=ii+1
        print "Done interpolating"

        return grid_points

class Bilinear(Interpolation):
   pass


class Linear(object):
   def get(self, x, y, xx):
      return yy
