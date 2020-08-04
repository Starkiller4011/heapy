heapy - High Energy Astrophysics in Python

Version 0.1.4

Installation:

Packaged Release:
Download a release from the release folder and extract it to where your python analysis script is
import heapy as hp

Normal:
    git clone https://github.com/Starkiller4011/heapy.git .
copy the contents of src to the location of your python analysis script
import heapy as hp

Usage:

Load your time series data and ensure you have a time, value, and error list. Pass the time, value, and error lists to the TimeSeries object constructor:

    ts = hp.TimeSeries(time, value, error, name="Time Series")

bin the time series if needed:

    ts.bin(bin_width)

make sure to detrend the time series before structure function analysis to remove any artificial steepening:

    ts.Detrend()

generate the structure function:

    sf = hp.StructureFunction(ts, name="Structure Function")

plot and/or save the structure function data:

    sf.Plot(save=False)

prepare data for fitting with XSPEC:

    xdf = sf.ConvertToXspec()


