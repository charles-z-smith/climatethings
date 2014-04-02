#Charles Smith
#Graphs global average temperature from 1979-2013
#Uses data from 
#
#Data obtained from
#http://www.esrl.noaa.gov/psd/thredds/catalog/Datasets/ncep/catalog.html
###################################################################
from glob import glob
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import time
"""Some of the plotting code is directly from
http://matplotlib.org/basemap/users/examples.html"""
def plotMap():
    fig=plt.figure(figsize=(24,12))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    m = Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=90,projection='mill')
    m.drawmapboundary(fill_color='0.3')
    mlons, mlats = np.meshgrid(lons,lats)
    clevs = np.arange(230,305,3)
    colorfilled = m.contourf(mlons,mlats,avgTempPeriod,clevs,cmap=plt.cm.jet,latlon=True)
    m.drawcoastlines()
    cb = m.colorbar(colorfilled,"bottom", size="5%", pad="2%")
    ax.set_title("Global Average Temp 1979 - 2013")
    plt.savefig("globalavg.png", pad_inches=0.0, bbox_inches="tight")
    plt.clf()

files = glob("C:/Python32/climatethings/*.nc")
nc = Dataset("C:/Python32/climatethings/air.sfc.2011.nc")
lats = nc.variables["lat"]
lons = nc.variables["lon"]
files = files[:len(files)-1]

avgTempPeriod = []
for i in range(0,len(lats)):
	avgTempPeriod.append([0.0] * len(lons))
avgTempPeriod = np.array(avgTempPeriod)
#Could do this in parallel if we had the CPUs.
#Get the sum of all the temperatures for a lat lon location.
nlats = len(lats)
nlons = len(lons)
start = time.clock()
for i in files:
    nc = Dataset(i)
    tempK = np.array(nc.variables['air'])
    avgTempsYr = []
    #Empty avg year.
    for i in range(0,nlats):
            avgTempsYr.append([0.0] * nlons)
    avgTempsYr = np.array(avgTempsYr)
    for day in range(0,len(tempK)):
        for lat in range(0, nlats):
            for lon in range(0, nlons):
                avgTempsYr[lat][lon] += tempK[day][lat][lon]
    #average for the Year, put in in the period, 1976 -2013 for now.
    for lat in range(0,nlats):
        for lon in range(0, nlons):
            avgTempPeriod[lat][lon] += avgTempsYr[lat][lon]/len(tempK)


total = time.clock() - start
print("total time %f" % total)
#now Average Period
for lat in range(0,len(lats)):
    for lon in range(0, len(lons)):
        avgTempPeriod[lat][lon] = avgTempPeriod[lat][lon]/len(files)

plotMap()
            
            
    
