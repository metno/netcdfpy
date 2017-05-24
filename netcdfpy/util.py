import sys

def error(message):
    """ Write error message to console and abort """
    print "\033[1;31mError: " + message + "\033[0m"
    sys.exit(1)

def info(message):
    """ Write a information message to console """
    print "\033[1;92mINFO: " + message + "\033[0m"

def warning(message):
    """ Write a warning message to console """
    print "\033[1;33mWarning: " + message + "\033[0m"

def get_nearest_neighbour(lat, lon, lats, lons):
   """
   Arguments:
      lat (float):
      lon (float):

   Returns:
      I (int): I coordinate
      J (int): J coordinate
   """

   raise NotImplementedError()
