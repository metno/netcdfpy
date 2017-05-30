from netcdfpy.interpolation import Interpolation
from netcdfpy.util import error,info,log,warning,setup_custom_logger
from netcdfpy.variable import Variable,Axis
from netcdfpy.interpolation import NearestNeighbour,Bilinear,Linear
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import cfunits

logger = setup_custom_logger('root')

class Netcdf(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = netCDF4.Dataset(filename, "r")

    def __del__(self):
        self.file.close()

    def num_height(self, field):
        pass

    def num_time(self, field):
        """
        :param field: 
        :return: (int) length of time dimension 
        """
        pass

    def slice(self, var_name, levels=None, members=None, times=None, xcoords=None, ycoords=None,
              deaccumulate=False, plot=False, var=None, instantanious=0., units=None ):
        """
        Assembles a 5D field in order lon,lat,time,height,ensemble

        Arguments:
            var_name (str): Name of field to retrieve
            height (list): Height index. If None, return all.
            ens (list): Ensemble index. If None, return all.
            time (list): Time index. If None, return all.
            xcoords: X-axis coordinates to subset
            ycords: Y-axis coordinates to subset
            deaccumulate (boolean): Deaccumulate field
            var
            plot
            instantanious
            units
            var(object): Call slice with an existing var object

        Returns:
         np.array: 5D array with values
        """

        if var == None:
            var=Variable(self.file,var_name)
        else:
            if var.var_name != var_name: error("Mismatch in variable name!")

        log(1,"Reading variable "+var.var_name)
        times_to_read=[]
        prev_time_steps=[]
        if times == None:
            for i in range(0,var.times.shape[0]):
                times_to_read.append(i)
                if i > 0:
                    prev_time_steps.append(i-1)
                else:
                    prev_time_steps.append(0)
        else:
            log(2,"Time provided in call "+str(times))
            times_in_var = var.times
            for i in range(0, times_in_var.shape[0]):
                for j in range(0, len(times)):
                    # Time steps requested
                    if i == times[j]:
                        times_to_read.append(times[j])
                        if i > 0:
                            prev_time_steps.append(i-1)
                        else:
                            prev_time_steps.append(0)

                    # TODO: possible to set array indices from input time values?


        levels_to_read=[]
        if levels == None:
            for i in range(0, var.levels.shape[0]):
                levels_to_read.append(i)
        else:
            log(2,"Level provided in call. Set index from value")
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
            log(2,"Ensemble members provided in call")
            members_in_var=var.members
            for i in range(0, members_in_var.shape[0]):
                for j in range(0, len(members)):
                    if members_in_var[i] == members[j]:
                        members_to_read.append(i)

            if len(members_to_read) == 0: error("No ensemble members found for " + var.var_name)

        lons=var.lons
        lats=var.lats

        # Dimensions of the "problem"
        dim_x = lons.shape[1]
        dim_y = lats.shape[0]
        dim_t = max(len(times_to_read),1)
        dim_levels = max(len(levels_to_read),1)
        dim_members = max(len(members_to_read),1)

        log(3,"Dimensions in output")
        log(3,str(dim_x) + " " + str(dim_y) + " " + str(dim_t) + " " + str(dim_levels) + " " + str(dim_members))


        lon_ind=[(i) for i in range(0,dim_x)]
        lat_ind = [(i) for i in range(0,dim_y)]
        dims=[]
        prev_dims=[]
        types=var.axis_types
        mapping={} # Map axis to output axis
        for i in range(0,len(types)):
            if types[i] == Axis.GeoX or types[i] == Axis.Lon:
                dims.append(lon_ind)
                prev_dims.append(lon_ind)
                mapping[0]=i
            if types[i] == Axis.GeoY or types[i] == Axis.Lat:
                dims.append(lat_ind)
                prev_dims.append(lat_ind)
                mapping[1]=i
            if types[i] == Axis.Time:
                dims.append(times_to_read)
                prev_dims.append(prev_time_steps)
                mapping[2]=i
            if types[i] == Axis.Height or types[i] == Axis.Pressure:
                dims.append(levels_to_read)
                prev_dims.append(levels_to_read)
                mapping[3]=i
            if types[i] == Axis.Realization:
                dims.append(members_to_read)
                prev_dims.append(members_to_read)
                mapping[4]=i


        log(2,"Read "+var.var_name+" with dimensions: "+str(dims))
        if deaccumulate: log(2,"Deaccumulate previous dimensions: "+str(prev_dims))
        field = self.file[var.var_name][dims]
        if units != None: field=cfunits.Units.conform(field,cfunits.Units(var.units),cfunits.Units(units))

        # Deaccumulation
        if deaccumulate:
            original_field=field
            previous_field= self.file[var.var_name][prev_dims]
            if units != None: previous_field = cfunits.Units.conform(previous_field,cfunits.Units(var.units),cfunits.Units(units))
            field =np.subtract(original_field,previous_field)

        # Create instantanious values
        if instantanious > 0:
            field = np.divide(field,instantanious)

        # Add extra dimensions
        i=0
        reverse_mapping=[]
        for d in range(0,5):
            if d not in mapping:
                log(3,"Adding dimension " + str(d))
                field=np.expand_dims(field,len(dims)+i)
                reverse_mapping.append(d)
                i=i+1
            else:
                reverse_mapping.append(mapping[d])

        # Transpose to 5D array
        log(1,"Transpose to 5D array")
        field=np.transpose(field,reverse_mapping)

        if ( plot):
            for t in range(0,dim_t):
                for z in range(0,dim_levels):
                    for m in range(0,dim_members):
                        plt.imshow(np.reshape(field[:,:,t,z,m],[dim_x,dim_y]),interpolation='nearest')
                        plt.show()


        log(2,"Shape of output: "+str(field.shape))
        return field

    def points(self, var_name, lons,lats, levels=None, members=None, times=None, xcoords=None, ycoords=None,
              deaccumulate=False, interpolation="nearest"):

        """
        Assembles a 5D slice and interpolates it to requested positions

        Arguments:


        Returns:
         np.array: 4D array with inpterpolated values in order pos,time,height,ensemble

        """

        var = Variable(self.file, var_name)
        field=self.slice(var_name,levels=levels, members=members, times=times, xcoords=xcoords, ycoords=ycoords,
              deaccumulate=deaccumulate)

        if lons == None or lats == None:
            error("You must set lons and lats when interpolation is set!")

        if interpolation == "nearest":
            log(2,"Nearest neighbour")
            if not hasattr(self,"interpolated_values"):
                nn = NearestNeighbour()
                self.interpolated_values=nn.interpolated_values(field,lons,lats,var)

            log(3,"Closest grid points: "+str(self.interpolated_values))

            interpolated_field=np.empty([len(lons),field.shape[2],field.shape[3],field.shape[4]])
            for i in range(0,len(lons)):
                ind_x = self.interpolated_values[i][0]
                ind_y = self.interpolated_values[i][1]
                for t in range(0, field.shape[2]):
                    for z in range(0, field.shape[3]):
                        for m in range(0, field.shape[4]):
                            interpolated_field[i][t][z][m]=field[ind_x][ind_y][t][z][m]
                            print ind_x,ind_y,t,z,m,field[ind_x][ind_y][t][z][m]
            # Comparison
            #field = nn.__interpolated_values__(field,lons,lats,var)

        else:
            error("Interpolation type "+interpolation+" not implemented!")

        log(3,str(interpolated_field.shape))
        return interpolated_field