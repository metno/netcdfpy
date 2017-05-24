import netCDF4
from netcdfpy.interpolation import Interpolation
import netcdfpy.util
import netcdfpy.variable
import netCDF4
import numpy as np


class Netcdf(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = netCDF4.Dataset(filename, "r")


    def num_height(self, field):
        pass

    def num_time(self, field):
        """
        :param field: 
        :return: (int) length of time dimension 
        """
        pass

    def slice(self, var_name, height=None, ens=None, time=None, xcoords=None, ycoords=None, lons=None, lats=None,
              deaccumulate=False):
        """
        Assembles a 5D field in order lon,lat,time,height,ensemble

        Arguments:
           var_name (str): Name of field to retrieve
           height (list): Height index. If None, return all.
           ens (list): Ensemble index. If None, return all.
           time (list): Time index. If None, return all.
           xcoords: X-axis coordinates to subset
           ycords: Y-axis coordinates to subset
           lons (list): List of longitudes to interpolate to
           lats (list): List of latitudes to interpolate to 
           deaccumulate (boolean): Deaccumulate field

        Returns:
         np.array: 5D array with values
        """

        var=netcdfpy.variable.Variable(self.file,var_name)

        print "Reading variable"
        if time == None:
            time=[]
            times=var.times
            for i in range(0,times.shape[0]):
                time.append(times[i])
            print time

        heights=[]
        levels = var.levels
        if height == None:
            for i in range(0, levels.shape[0]):
                heights.append(i)
                print "der"
                print heights[i]
        else:
            for i in range(0, levels.shape[0]):
                for j in range (0,len(height)):
                    if height[j] == levels[i]:
                        heights.append(i)

            print "Her"
            print heights

        if ens == None: ens = [0]

        lons=var.lons
        lats=var.lats
        height=var.levels

        print lons.shape
        print lats.shape
        dim_x = lons.shape[0]
        dim_y = lats.shape[0]
        dim_t = len(time)
        dim_height = len(heights)

        #dim_ens = var.members[0]
        print "Dimensions"
        print(str(dim_x) + " " + str(dim_y) + " " + str(dim_t) + " " + str(dim_height))# + " " + str(dim_ens))
        print(time)
        #print(height)
        #print(ens)

        # This is a test assuming this structure
        print "Read"
        field_read = self.file[var.var_name][time,heights, :, :]

        field = np.reshape(field_read, [dim_x, dim_y, dim_t, dim_height,1])
        print field.shape
        return field

    def point(self, field, lat, lon, height=0, ens=0, time=None, interpolation=None):
        """
        Assembles a 2D horizontal field for a specific time step

        Arguments:
         field (str): Name of field to retrieve
         I (np.array): I coordinate
         J (np.array): J coordinate
         height (int): Height index. If None, return all.
         time (int): Index. If None, return all.

        Returns:
         np.array: 2D array with values
        """

        raise NotImplementedError()
