# coding: UTF-8

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import netCDF4

import sys, io, json
from io import BytesIO
import base64
import numpy as np

import matplotlib.style
import matplotlib as mpl
mpl.style.use('classic')

# plot with traditional coloring.
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def sounding_plot(ncfilepath, lonindex=None, latindex=None):
    
    plt.gcf().clear()
    
    # checking the arguments.
    if lonindex is None or latindex is None:
        # print("Missing argument")
        return
    
    # opening the file.
    dataset = netCDF4.Dataset(ncfilepath, 'r')
    
    # opening latitude and longitude bounds.
    max_lon = dataset.dimensions['west_east'].size
    max_lat = dataset.dimensions['south_north'].size
    
    # verify latitude and longitude bounds.
    if  lonindex not in range(-max_lon, max_lon):
        # print("lonindex out of bounds : " + str(lonindex))
        return
    if latindex not in range (-max_lat, max_lat):
        # print("latindex out of bounds : " + str(latindex))
        return
    
    # opening the variables.
    QVAPOR = dataset.variables['QVAPOR'][:]
    P = dataset.variables['P'][:]
    PB = dataset.variables['PB'][:]
    T = dataset.variables['T'][:]
    
    # pressure in milli bars.
    P_mb = (P + PB) * 0.01

    theta =  T + 300.0
    T_c = theta * ((P_mb)/1000.0)**(2.0/7.0) - 273.0
    
    # DewPoint Temperature Calculations.
    # converting the varialbe to Pa (Pascals) from KPa (Kilo Pascals).
    A_Pa = ((2.53 * (10**8)) * 1000.0)
    
    # varaible B is in K (Kelvin).
    B_c = (5.42 *(10**3))
    
    e = 0.622
    w = QVAPOR
    
    # maintaining the surface pressure in Pa (Pascals).
    P_Pa = (P + PB)
    
    # calculating depoint temperature and convertion to celcius.
    T_d = (B_c / (np.log(((A_Pa*e)/(w*P_Pa))))) - 273.0

    # all the soundings.
    t_sounding = T_c[0,:,latindex,lonindex]
    p_sounding = P_mb[0,:,latindex,lonindex]
    td_sounding = T_d[0,:,latindex,lonindex]

    # plotting the soundings.
    plt.semilogy(t_sounding, p_sounding)
    plt.semilogy(td_sounding, p_sounding)

    plt.ylim(ymin=50.0, ymax=1050.0)
    plt.gca().invert_yaxis()

    ylocations = np.arange(100,1000,100)
    plt.yticks(ylocations, ylocations)

    plt.title("Lat/Lon indices : " + str(latindex) + "/" + str(lonindex))

    figfile = BytesIO()

    plt.savefig(figfile, format='png', dpi = (100))

    figfile.seek(0)  # rewind to beginning of file
    
    figdata_png = base64.b64encode(figfile.getvalue())
    
    return figdata_png

def main():
    # #get our data as an array from read_in()
    lines = read_in()
    filePath = lines[0]
    latindex = int(lines[1])
    lonindex = int(lines[2])

    plot_image_data = sounding_plot(filePath, lonindex, latindex)

    varDesc = []
    varDesc.append({'value': "xxxx", 'name': "Vertical Sounding"})

    var_data = {'desc': varDesc, 'plot': plot_image_data.decode('utf8')}

    print(json.dumps(var_data))

# Start process
if __name__ == '__main__':
    main()