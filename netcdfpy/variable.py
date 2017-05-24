import netCDF4
from netcdfpy.interpolation import Interpolation
import netCDF4
import numpy as np
import netcdfpy.util
import re

from enum import Enum
class Axis(Enum):
    Undefined = 0
    GeoX = 1
    GeoY = 2
    GeoZ = 3
    Time = 4
    Lon = 5
    Lat = 6
    Pressure = 7
    Height = 8
    ReferenceTime = 9
    Realization = 10


class Variable(object):
    def __init__(self,fh,var_name):
        self.file = fh
        self.var_name=var_name

    @property
    def axis_types(self):
        types=[]
        if self.file.variables[self.var_name]:
            for i in range(0, len(self.file.variables[self.var_name].dimensions)):
                dim_name = self.file.variables[self.var_name].dimensions[i]
                if dim_name == "longitude" or dim_name == "lon":
                    types.append(Axis.Lon)
                elif dim_name == "x":
                    types.append(Axis.GeoX)
                elif dim_name == "latitude" or dim_name == "lat":
                    types.append(Axis.Lat)
                elif dim_name == "y":
                    types.append(Axis.GeoY)
                elif re.search("height[0-9]*",dim_name):
                    types.append(Axis.Height)
                elif dim_name == "ensemble_member":
                    types.append(Axis.Realization)
                else:
                    types.append(Axis.Undefined)
        return types

    @property
    def dim_names(self):
        names=[]
        if self.file.variables[self.var_name]:
            for i in range(0, len(self.file.variables[self.var_name].dimensions)):
                names.append(self.file.variables[self.var_name].dimensions[i])
        return names

    @property
    def lats(self):
        """
        Returns:
           np.array: 2D array of latitudes
        """

        latvals=None
        axis_types = self.axis_types
        for i in range(0, len(axis_types)):
            if axis_types[i] == Axis.Lat:
                latvals = self.file.variables[self.dim_names[i]]
            elif axis_types[i] == Axis.GeoY:
                latvals = self.file.variables[self.dim_names[i]]

                # TODO: if lat/lon are 1D, create a 2D mesh
                # TODO: Reorder dimensions if x/y are flipped

        if latvals == None:  netcdfpy.util.error("No latitude found for " + self.var_name)
        print latvals.shape
        return latvals

    @property
    def lons(self):
        """
        Returns:
           np.array: 2D array of longitudes
        """

        lonvals=None
        axis_types=self.axis_types
        for i in range(0,len(axis_types)):
            if axis_types[i] == Axis.Lon:
                lonvals = self.file.variables[self.dim_names[i]]
            elif axis_types[i] == Axis.GeoX:
                lonvals = self.file.variables[self.dim_names[i]]

                # TODO: if lat/lon are 1D, create a 2D mesh
                # TODO: Reorder dimensions if x/y are flipped

        if lonvals == None:  netcdfpy.util.error("No longitude found for " + self.var_name)
        return lonvals

    @property
    def times(self):
        """
            Return:
            np.array: 1D array of times
        """

        times = None
        axis_types = self.axis_types
        for i in range(0, len(axis_types)):
            if axis_types[i] == Axis.Time:
                times = self.file.variables[self.dim_names[i]]

        if times == None: netcdfpy.util.warning("No time found for "+self.var_name)
        return times

    @property
    def members(self):
        """
            Return:
            np.array: 1D array of ensemble members
        """

        members=None
        axis_types = self.axis_types
        for i in range(0, len(axis_types)):
            if axis_types[i] == Axis.Realization:
                members = self.file.variables[self.dim_names[i]]
        return members


        if members == None: netcdfpy.util.warning("No ensemble members found for " + self.var_name)
        return members

    @property
    def levels(self):
        """
            Return:
            np.array: 1D array of levels
        """

        levels = None
        axis_types = self.axis_types
        for i in range(0, len(axis_types)):
            if axis_types[i] == Axis.Height:
                levels = self.file.variables[self.dim_names[i]]

        if levels == None: netcdfpy.util.warning("No levels found for " + self.var_name)
        return levels


