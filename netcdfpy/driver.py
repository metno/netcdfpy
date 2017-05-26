import sys
import argparse
from netcdfpy.netcdf import Netcdf
import matplotlib.pyplot as plt
import numpy as np

def run(argv):
    parser = argparse.ArgumentParser(description="Driver for netcdfpy")

    if len(sys.argv) != 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()


    filename="http://thredds.met.no/thredds/dodsC/meps25files/meps_det_extracted_2_5km_latest.nc"
    file = Netcdf(filename)


    data = file.slice("air_temperature_2m",times=[0,3],levels=[2])
    #grid=np.reshape(data[:,:,:,:,:],(data.shape[0],data.shape[1]))
    #plt.imshow(grid)
    #plt.show()
    #print data.shape
    x=file.slice("longitude",plot=True)
    data = file.slice("relative_humidity_2m",times=[3])
    print data.shape
    data = file.slice("air_temperature_z",times=[7,8,12],levels=[120,80])

if __name__ == '__main__':
    run(sys.argv)
