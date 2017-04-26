import netCDF4
from netcdfpy.interpolation import Interpolation
import netCDF4
import numpy as np

class Netcdf(object):

    def __init__(self, filename):
        self.filename = filename
        self.file=netCDF4.Dataset(filename,"r")

    @property
    def lats(self):
        """
        Returns:
           np.array: 2D array of latitudes
        """
        raise NotImplementedError()

    @property
    def lons(self):
        """
        Returns:
           np.array: 2D array of longitudes
        """
        raise NotImplementedError()

    def num_ens(self, field):
        pass

    def num_height(self, field):
        pass

    def num_time(self, field):
        pass

    def slice(self, field, height=None, ens=None, time=None, xcoords=None, ycoords=None, lons=None, lats=None, deaccumulate=False):
        """
        Assembles a 2D horizontal field for a specific time step

        Arguments:
           field (str): Name of field to retrieve
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


        if "latitude" in self.file.variables:
             latvar = self.file.variables["latitude"]
             lonvar = self.file.variables["longitude"]
        elif "lat" in self.file.variables:
             latvar = self.file.variables["lat"]
             lonvar = self.file.variables["lon"]

        lons = lonvar[:]
        lats = latvar[:]

        print(lons.shape)
        print(lats.shape)

        if ( time == None): time=[0]
        if ( height == None): height=[0]
        if ( ens == None): ens=[0]
        dim_x=len(lons)
        dim_x=739
        dim_y=len(lats)
        dim_t=len(time)
        dim_height=len(height)
        dim_ens=len(ens)
        print(str(dim_x)+" "+str(dim_y)+" "+str(dim_t)+" "+str(dim_height)+" "+str(dim_ens))
        print(time)
        print(height)
        print(ens)

        # This is a test assuming this structure
        field_read=self.file[field][time,height,0:dim_y,0:dim_x]


        field=np.reshape(field_read,[dim_x,dim_y,dim_t,dim_height,dim_ens])
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
