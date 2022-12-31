from ecmwfapi import ECMWFDataServer
from dotenv import load_dotenv
import pygrib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import shiftgrid
import numpy as np

load_dotenv()  # take environment variables from .env.

server = ECMWFDataServer()

server.retrieve(
    {
        "class": "ei",  # ERA Interim
        "dataset": "interim",
        "date": "2019-07-01/to/2019-07-02",
        "expver": "1",  # Version
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "49.128/165.128/166.128/167.128/243.128/244.128",
        "step": "3/6/9/12",
        "stream": "oper",  # Atmospheric Level
        "time": "00:00:00/12:00:00",
        "type": "fc",  # Forecast
        "target": "interim.grib",
    }
)

server.retrieve(
    {
        "class": "od",  # Operational Archive
        "date": "2020-01-01",
        "expver": "1",  # Version
        "levtype": "sfc",
        "param": "167.128",
        "step": "0/1/2/3/4",
        "stream": "oper",  # Atmospheric Level
        "time": "00:00:00",
        "type": "fc",  # Forecast
        "target": "output",
    }
)


plt.figure(figsize=(12, 8))

grib = "interim.grib"  # Set the file name of your input GRIB file
grbs = pygrib.open(grib)

grb = grbs.select()[0]
data = grb.values

# need to shift data grid longitudes from (0..360) to (-180..180)
lons = np.linspace(
    float(grb["longitudeOfFirstGridPointInDegrees"]),
    float(grb["longitudeOfLastGridPointInDegrees"]),
    int(grb["Ni"]),
)
lats = np.linspace(
    float(grb["latitudeOfFirstGridPointInDegrees"]),
    float(grb["latitudeOfLastGridPointInDegrees"]),
    int(grb["Nj"]),
)
data, lons = shiftgrid(180.0, data, lons, start=False)
grid_lon, grid_lat = np.meshgrid(lons, lats)  # regularly spaced 2D grid

m = Basemap(
    projection="cyl",
    llcrnrlon=-180,
    urcrnrlon=180.0,
    llcrnrlat=lats.min(),
    urcrnrlat=lats.max(),
    resolution="c",
)

x, y = m(grid_lon, grid_lat)

cs = m.pcolormesh(x, y, data, shading="flat", cmap=plt.cm.gist_stern_r)

m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.0, 120.0, 30.0), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180.0, 180.0, 60.0), labels=[0, 0, 0, 1])

plt.colorbar(cs, orientation="vertical", shrink=0.5)
plt.title("CAMS AOD forecast")  # Set the name of the variable to plot
plt.savefig(grib + ".png")  # Set the output file name
