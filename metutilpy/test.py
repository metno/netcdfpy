file = Netcdf(filename)

data = file.slice("air_temperature_2m", time=0, ens=0)
