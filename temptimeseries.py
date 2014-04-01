#Written by Charles Smith
#03-29-14
#
#An analysis of mean temperature near Milwaukee Wisconsin from 1979
#to 2013
#Data obtained from
#http://www.esrl.noaa.gov/psd/thredds/catalog/Datasets/ncep/catalog.html
#####################################
import glob
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
files = glob.glob("C:/python32/climatethings/*.nc")

yrAvgTemp = []#For the point of Milwaukee
for i in files:
    avg =0
    nc = Dataset(i)
    temp = np.array(nc.variables['air'])
    for day in range(len(temp)):#consider temp[][] len(temp[])=73, len(temp[][]) =144
        avg = avg + temp[day][19][107]#cords close to Milwaukee, feel free to change
    yrAvgTemp.append(avg/len(temp))#divide temp sum by how many days in temp

yrAvgTemp = yrAvgTemp[:len(yrAvgTemp)-1]#remove 2014, not done yet.

count = 0
while count != len(yrAvgTemp):
    yrAvgTemp[count] = yrAvgTemp[count]-273.15
    count+=1

dates = []
for i in range(1979,2014):
    dates.append(i)
dates = np.array(dates)
yrAvgTemp = np.array(yrAvgTemp)
plt.plot(dates, yrAvgTemp)
plt.title("Yearly Average Temperature Milwaukee")
plt.ylabel("Temperature (C)")
plt.xlabel("Year")
plt.savefig("avgtemp.png")

print(yrAvgTemp)
