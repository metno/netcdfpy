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

    data = file.slice("precipitation_amount_acc", times=[0, 3, 6, 9, 12, 15,],deaccumulate=True,plot=True)
    sw=file.slice("integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time",times=[0, 3, 6, 9, 12, 15,],deaccumulate=True,instantanious=3600.,plot=True)
    data = file.points("air_temperature_2m",times=[0,3],levels=[2],lons=[10,11],lats=[60,61],interpolation="nearest")
    print data.shape
    data= file.points("relative_humidity_2m",times=[0,3,6,9,12],levels=[2],lons=[10,11],lats=[60,61],interpolation="nearest")
    x=file.slice("longitude",plot=True)
    data = file.slice("relative_humidity_2m",times=[3])
    data = file.slice("air_temperature_z",times=[7,8,12],levels=[120,80])

if __name__ == '__main__':
    run(sys.argv)
