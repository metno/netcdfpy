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

   def get_gridded_slice(self, field, height=0, ens=0, time=None):
      """
      Assembles a 2D horizontal field for a specific time step

      Arguments:
         field (str): Name of field to retrieve
         height (int): Height index. If None, return all.
         ens (int): Ensemble index. If None, return all.
         time (int): Time index. If None, return all.

      Returns:
         np.array: 2D array with values
      """

      raise NotImplementedError()

   def get_point_slice(self, field, I, J, height=0, time=None):
      """
      Assembles a 2D horizontal field for a specific time step

      Arguments:
         field (str): Name of field to retrieve
         I (int): I coordinate
         J (int): J coordinate
         height (int): Height index. If None, return all.
         time (int): Index. If None, return all.

      Returns:
         np.array: 2D array with values
      """

      raise NotImplementedError()

   def get_nearest_neighbour(self, lat, lon):
      """
      Arguments:
         lat (float):
         lon (float):

      Returns:
         I (int): I coordinate
         J (int): J coordinate
      """

      raise NotImplementedError()
