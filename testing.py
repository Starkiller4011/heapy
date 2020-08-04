import os
import numpy as np
import pandas as pd
from astropy.io import fits
from heapy import *
from matplotlib import pyplot as plt

print("Analyzing Sophia's data")
for fits_file in os.listdir('sophia_data'):
    path = 'sophia_data/%s' % fits_file
    name = 'mrk478_%s' % fits_file[:10]
    print(path)
    hdu_list = fits.open(path, memmap=True)
    time = hdu_list[1].data['TIME'].tolist().copy()
    flux = hdu_list[1].data['RATE'].tolist().copy()
    error = hdu_list[1].data['ERROR'].tolist().copy()
    hdu_list.close()
    del hdu_list, path
    lc = TimeSeries(time, flux, error, name=name)
    del time, flux, error
    lc.Bin(200)
    lc.Detrend()
    lc.Plot(original=True, detrended=True, trendline=False, fmt='+', save=True)
    sf = StructureFunction(lc, name=name)
    sf.Plot(save=True)
    del lc, sf
