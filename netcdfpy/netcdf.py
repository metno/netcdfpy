from netcdfpy.interpolation import Interpolation

class Netcdf(object):
    def __init__(self, filename):
        self.filename = filename

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

    def slice(self, field, height=0, ens=0, time=None, xcoords=None, ycoords=None, deaccumulate=False):
        """
        Assembles a 2D horizontal field for a specific time step

        Arguments:
           field (str): Name of field to retrieve
           height (list): Height index. If None, return all.
           ens (list): Ensemble index. If None, return all.
           time (list): Time index. If None, return all.
           xcoords: X-axis coordinates to subset

        Returns:
         np.array: 2D array with values
        """

        raise NotImplementedError()

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
