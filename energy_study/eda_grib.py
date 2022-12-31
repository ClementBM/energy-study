import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pygrib
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_dataset("interim.grib", engine="cfgrib")
t0_ds = ds.isel(step=0)

# clear overview of the available data fields
for v in ds:
    print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

# filtering the dataset’s contents to a single variable of interest is very straightforward:
ds_u10 = ds.get("u10")

# multiple variables is also possible by using an array of strings as the input
# ds = ds.get([var1, var2])

df = ds_u10.to_dataframe()

latitudes = df.index.get_level_values("latitude")
longitudes = df.index.get_level_values("longitude")

grbs = pygrib.open("interim.grib")
grbs.seek(0)

for grb in grbs:
    print(grb)

grbs.seek(0)
grbs[1]


plt.imshow(grbs[1].values)

lats, lons = grbs[1].latlons()
map_crs = ccrs.LambertConformal(
    central_longitude=-100, central_latitude=35, standard_parallels=(30, 60)
)
data_crs = ccrs.PlateCarree()

fig = plt.figure(1, figsize=(14, 12))
ax = plt.subplot(1, 1, 1, projection=map_crs)
ax.set_extent([-130, -72, 20, 55], data_crs)
ax.add_feature(cfeature.COASTLINE.with_scale("50m"))
ax.add_feature(cfeature.STATES.with_scale("50m"))

ax.contourf(lons, lats, grbs[1].values, transform=data_crs)
