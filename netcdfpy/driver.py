import sys
import argparse
from netcdfpy.netcdf import Netcdf

def run(argv):
    parser = argparse.ArgumentParser(description="Driver for netcdfpy")

    if len(sys.argv) != 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()


    filename="http://thredds.met.no/thredds/dodsC/meps25files/meps_det_extracted_2_5km_latest.nc"
    file = Netcdf(filename)


    data = file.slice("air_temperature_2m",time=[0,3],height=[2])
    print data.shape
    #x=file.slice("x")
    data = file.slice("relative_humidity_2m",time=[3])
    print data.shape
    data = file.slice("air_temperature_z",time=[7,8,12],height=[120,80])

if __name__ == '__main__':
    run(sys.argv)
