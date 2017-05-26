import netCDF4
from netcdfpy.interpolation import Interpolation
import netcdfpy.util
from netcdfpy.variable import Variable,Axis
import netcdfpy.variable
import netCDF4
import numpy as np
import matplotlib.pyplot as plt

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

    def slice(self, var_name, levels=None, members=None, times=None, xcoords=None, ycoords=None, lons=None, lats=None,
              deaccumulate=False, plot=False):
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

        var=Variable(self.file,var_name)

        print "Reading variable "+var.var_name
        times_to_read=[]
        if times == None:
            for i in range(0,var.times.shape[0]):
                times_to_read.append(i)
        else:
            print "Time provided in call"
            times_in_var = var.times
            for i in range(0, times_in_var.shape[0]):
                for j in range(0, len(times)):
                    if i == j:
                        times_to_read.append(times[j])

                    # TODO: possible to set array indices from input
                    #if times_in_var[i] == times[j]:
                    #    times_to_read.append(i)


        # TODO: If accuumulated, read extra time step if needed


        levels_to_read=[]
        if levels == None:
            for i in range(0, var.levels.shape[0]):
                levels_to_read.append(i)
                print levels_to_read[i]
        else:
            print "Level provided in call. Set index from value"
            # TODO: specify index
            levels_in_var=var.levels
            for i in range(0, levels_in_var.shape[0]):
                for j in range (0,len(levels)):
                    if levels_in_var[i] == levels[j]:
                        levels_to_read.append(i)

        members_to_read = []
        if members == None:
            for i in range(0, var.members.shape[0]):
                members_to_read.append(i)
        else:
            print "Ensemble members provided in call"
            members_in_var=var.members
            for i in range(0, members_in_var.shape[0]):
                for j in range(0, len(members)):
                    if members_in_var[i] == members[j]:
                        members_to_read.append(i)

            if len(members_to_read) == 0: netcdfpy.util.error("No ensemble members found for " + var.var_name)

        lons=var.lons
        lats=var.lats

        # Dimensions of the "problem"
        dim_x = lons.shape[0]
        dim_y = lats.shape[0]
        dim_t = max(len(times_to_read),1)
        dim_levels = max(len(levels_to_read),1)
        dim_members = max(len(members_to_read),1)

        print "Dimensions in output"
        print str(dim_x) + " " + str(dim_y) + " " + str(dim_t) + " " + str(dim_levels) + " " + str(dim_members)


        lon_ind=[(i) for i in range(0,len(lons))]
        lat_ind = [(i) for i in range(0, len(lats))]
        dims=[]
        types=var.axis_types
        mapping={} # Map axis to output axis
        for i in range(0,len(types)):
            if types[i] == Axis.GeoX or types[i] == Axis.Lon:
                dims.append(lon_ind)
                mapping[i]=0
            if types[i] == Axis.GeoY or types[i] == Axis.Lat:
                dims.append(lat_ind)
                mapping[i]=1
            if types[i] == Axis.Time:
                dims.append(times_to_read)
                mapping[i]=2
            if types[i] == Axis.Height or types[i] == Axis.Pressure:
                dims.append(levels_to_read)
                mapping[i]=3
            if types[i] == Axis.Realization:
                dims.append(members_to_read)
                mapping[i]=4


        print "Read "+var.var_name+" with dimensions: "+str(dims)
        field_read = self.file[var.var_name][dims]

        # TODO: It must be a clever way for this.... Native numpy routines???
        print "Prepare output in 5-D array"
        field=np.empty([dim_x,dim_y,dim_t,dim_levels,dim_members])
        for i in range(0, dim_x):
            for j in range(0, dim_y):
                for k in range(0, dim_t):
                    for l in range(0, dim_levels):
                        for m in range(0, dim_members):

                            for x in range(0, len(types)):
                                ind = -1
                                # Longitude
                                if mapping[x] == 0:
                                    ind = i
                                # Latitude
                                elif mapping[x] == 1:
                                    ind = j
                                elif mapping[x] == 2:
                                    ind = k
                                elif mapping[x] == 3:
                                    ind = l
                                elif mapping[x] == 4:
                                    ind = m
                                else:
                                    netcdfpy.util.error("This should never happen!")

                                if x == 0:
                                    ii = ind
                                elif x == 1:
                                    jj = ind
                                elif x == 2:
                                    kk = ind
                                elif x == 3:
                                    ll = ind
                                elif x == 4:
                                    mm = ind
                                else:
                                    netcdfpy.util.error("This should never happen!")

                            if len(types) == 2:
                                read_value = field_read[ii,jj]
                            elif len(types) == 3:
                                read_value = field_read[ii,jj,kk]
                            elif len(types) == 4:
                                read_value = field_read[ii,jj,kk,ll]
                            elif len(types) == 5:
                                read_value = field_read[ii,jj,kk,ll,mm]
                            else:
                                netcdfpy.util.error("Dimensions must be between 2 and 5")

                            # Finally set value
                            field[i][j][k][l][m]=read_value

        #TODO:  Deaccumulate

        #TODO: Interpolations


        if ( plot):
            for t in range(0,dim_t):
                for z in range(0,dim_levels):
                    for m in range(0,dim_members):
                        plt.imshow(np.reshape(field[:,:,t,z,m],[dim_x,dim_y]),interpolation='nearest')
                        plt.show()


        print "Shape of output: "+str(field.shape)
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
