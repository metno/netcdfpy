from scipy.interpolate import griddata

class Interpolation(object):
   pass
   def get(self, lat, lon, lats, lons, field):
      pass


class NearestNeighbour(Interpolation):

   #points=self.lats

   #field_in = griddata(points,values_vec,xi,method='nearest')
   pass


class Bilinear(Interpolation):
   pass


class Linear(object):
   def get(self, x, y, xx):
      return yy
