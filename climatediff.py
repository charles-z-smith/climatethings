#Written By Charles Smith
#
#Can be used to compare how cold/warm a certain period was compared to another period
#
#Some of this code uses the basemap examples on
#http://matplotlib.org/basemap/users/examples.html
########################################################
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from datetime import datetime
import os

def findDifference(arr1, arr2):
    new = [] # initalize difference to 0.0.
    for lat in range(0, nlats):
        inner = []
        for lon in range(0, nlons):
            inner.append(arr1[lat][lon] - arr2[lat][lon])
        new.append(inner)
    return new

#Compare Jan/Feb of 2011 and 2014.
#Reason for doing this is to give a visual quantitya
#of how warm 2011 was vs hold cold 2014 is/was
#Feb was 28 days both years. Therefore
#looking at days [0:31+28]
nc11 = Dataset(os.path.realpath("./") +"/air.sfc.2011.nc")
nc14 = Dataset(os.path.realpath("./") +"/air.sfc.2014.nc")

#declare world basemap
m = Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=90,projection='mill')
fig=plt.figure(figsize=(24,12))
ax = fig.add_axes([0.05,0.05,0.9,0.85])
#same for both years
lats = nc11.variables["lat"]
lons = nc11.variables["lon"]

nlats = len(lats)
nlons = len(lons)

lons, lats = np.meshgrid(lons, lats)
x, y = m(lons, lats)

#grab data for Jan-Feb
temp11 = nc11.variables["air"][0:59]
temp14 = nc14.variables["air"][0:59]

#Generate difference for Jan-Feb
difference = []
for day in range(0,59):#Calculate it
    difference.append(findDifference(np.array(temp11[day]), np.array(temp14[day])))
    
#init/declare 2-d matrix of correct size for avg diff
avgDifference = [[0.0] * nlons]* nlats
avgDifference = np.array(avgDifference)

for lat in range(0,nlats):
    for lon in range(0,nlons):
        avgDiff = 0
        for day in range(0,59):
            avgDiff = avgDiff + difference[day][lat][lon]
        avgDifference[lat][lon] = avgDiff/59


clevs = np.arange(-15,15,0.5)
colorfilled = m.contourf(x,y,avgDifference ,clevs,cmap=plt.cm.RdBu_r)
parallels = np.arange(-80.,90,20.)
meridians = np.arange(0.,360.,20.)
m.drawcoastlines()
m.drawparallels(parallels)
m.drawmeridians(meridians)
cb = m.colorbar(colorfilled, "bottom", "5%", pad="2%")
cb.set_label("Kelvin")
ax.set_title("Jan/Feb(2011) - Jan/Feb(2014)")
plt.savefig("figure.png", pad_inches=0.0, bbox_inches="tight")
plt.clf()
