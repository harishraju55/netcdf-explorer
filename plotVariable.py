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

def anyplot(v, description):

    plt.gcf().clear()
    plt.contourf(v)

    plt.colorbar()
    plt.title(' ' + description)

    figfile = BytesIO()
    # plt.savefig('foo.png')

    plt.savefig(figfile, format='png', dpi = (100))

    figfile.seek(0)  # rewind to beginning of file
    
    figdata_png = base64.b64encode(figfile.getvalue())
    
    return figdata_png

def main():
    # #get our data as an array from read_in()
    lines = read_in()
    filePath = lines[0]
    varName = lines[1]

    dataset = netCDF4.Dataset(filePath, 'r')

    cur_var = dataset[varName]

    cur_var_arr = np.array(cur_var)

    if len(cur_var_arr.shape) == 2:
        var_val = cur_var_arr[:]
    if len(cur_var_arr.shape) == 3:
        var_val = cur_var_arr[0,:,:]

    # varDesc = []
    # plot_image_data = anyplot(var_val, cur_var.name)
    # var_data = {'desc': varDesc, 'plot': plot_image_data.decode('utf8')}

    plot_image_data = anyplot(var_val, cur_var.name)

    varDesc = []
    varDesc.append({'value': cur_var.name, 'name': cur_var.name})
    for attrname in cur_var.ncattrs():
        # print("{} : {}".format(attrname, getattr(cur_var, attrname)))
        varDesc.append({'value': "{} : {}".format(attrname, getattr(cur_var, attrname)), 
        'name': "{} : {}".format(attrname, getattr(cur_var, attrname))})

    var_data = {'desc': varDesc, 'plot': plot_image_data.decode('utf8')}

    print(json.dumps(var_data))

# Start process
if __name__ == '__main__':
    main()