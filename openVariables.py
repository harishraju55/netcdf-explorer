# *- coding: utf-8 - *-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import netCDF4
from netCDF4 import Dataset

from io import BytesIO
import base64

import matplotlib.colors as mcolors
import h5py
import h5netcdf

import numpy as np
import sys, io, json

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    lines = read_in()
    WRFOUT_FILE_PATH = lines[0]

    varslist = []
    try:
        wrfdataset = netCDF4.Dataset(WRFOUT_FILE_PATH, 'r')
        for name, variable in wrfdataset.variables.items():
            if len(variable.dimensions) == 3:
                varslist.append({'value': name, 'name': name})
    except:
        hdfdataset = h5py.File(WRFOUT_FILE_PATH, mode='r')
        for name in hdfdataset.keys():
            if len(variable.dimensions) == 3 or len(variable.dimensions) == 2:
                varslist.append({'value': name, 'name': name})

    print(json.dumps(varslist))

# Start process
if __name__ == '__main__':
    main()