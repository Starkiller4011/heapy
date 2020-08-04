#!/usr/bin/env python3
from __future__ import division, print_function
import sys
import concurrent.futures as cf
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

class TimeSeries:
    """
    Time Series class
    """
    def __init__(self, time, value, error, name='time_series'):
        self.time = time
        self.value = value
        self.error = error
        self.name = name
        self.original_data = {'time': self.time.copy(), 'value': self.value.copy(), 'error': self.error.copy()}
        self.FitLinear()
        self.original_trendline = self.trendline
        self.CaculateVarance()
        self.Duration = self.time[-1]-self.time[0]
        self.Bins = len(self.time)
    def Bin(self, tau):
        self.time = self.original_data['time'].copy()
        self.value = self.original_data['value'].copy()
        self.error = self.original_data['error'].copy()
        self.binning = {}
        nbins = 0
        tval = self.time[0]
        index = 0
        while tval < (self.time[0] + self.Duration):
            tval += tau
            nbins += 1
            index = self.FillBin(index, tval)
        self.time.clear()
        self.value.clear()
        self.error.clear()
        for time in self.binning.keys():
            self.time.append(time)
            self.value.append(self.binning[time][0])
            self.error.append(self.binning[time][1])
        del self.binning
        self.Bins = nbins
    def FillBin(self, last_index, bin_end):
        new_time_bin = []
        new_value_bin = []
        new_error_bin = []
        for i in range(last_index, len(self.time)):
            if self.time[i] >= bin_end:
                time = np.average(new_time_bin)
                value = np.average(new_value_bin)
                error = np.average(new_error_bin)
                self.binning[time] = (value, error)
                return i
            else:
                new_time_bin.append(self.time[i])
                new_value_bin.append(self.value[i])
                new_error_bin.append(self.error[i])
    def CaculateVarance(self):
        mu = np.average(self.value)
        diffs = []
        for i in range(0, len(self.value)):
            diffs.append(np.power(self.value[i] - mu - self.error[i], 2))
        self.sigma = np.average(diffs)
    def FitLinear(self):
        model = LinearRegression().fit(np.array(self.time).reshape(-1, 1), np.array(self.value))
        predicted = model.predict(np.array(self.time).reshape(-1, 1))
        self.trendline = predicted.tolist()
    def Detrend(self):
        self.FitLinear()
        self.value = (np.array(self.value) - np.array(self.trendline)).tolist()
    def Plot(self, original=True, detrended=False, trendline=False, fmt='.', save=False):
        if not original and not detrended:
            print('Nothing given to plot', file=sys.stderr)
            return
        fig = plt.figure(figsize=(10, 5))
        plot = fig.add_subplot(1, 1, 1)
        fig.suptitle('Time Series', fontsize=18)
        plot.set_xlabel(r'$Time$', fontsize=16)
        plot.set_ylabel(r'$\mathfrak{F}lux$', fontsize=16)
        if original:
            otime = self.original_data['time']
            ovalue = self.original_data['value']
            oerror = self.original_data['error']
            plt.errorbar(otime, ovalue, yerr=oerror, fmt=fmt, label='Original')
        if detrended:
            plt.errorbar(self.time, self.value, yerr=self.error, fmt=fmt, label='Detrended')
        if trendline:
            plt.plot(self.time, self.original_trendline, linewidth='0.7', color='r')
        plt.axhline(y=0, linestyle='-', linewidth='0.7', color='k')
        if original and detrended:
            plt.legend()
        if save:
            savename = '%s_ts.png' % self.name
            plt.savefig(savename)
        else:
            plt.show()

class FakeTimeSeries:
    time = []
    value = []
    error = []
    def __init__(self, start, stop, avg_diff, amplitude=10, seed=1):
        np.random.seed(seed)
        self.scaling = stop - start
        self.start = start
        self.stop = stop
        self.avg_diff = avg_diff
        self.amplitude = amplitude
    def test_f(self, x):
        a = ((-5.0*x)/40.0)
        b = ((10.0*np.sin(x/30.0))+(3.0*np.cos((x/40.0)*np.sin(x/200.0))))
        c = (4.0*np.sin(x*np.cos(x/90.0)))
        d = (2.0*np.sin(x))
        e = np.cos(x/30.0)
        return ((a*(b+c+d)*e)+60)
    def Generate(self):
        self.time.clear()
        self.value.clear()
        self.error.clear()
        for i in np.arange(self.start, self.stop, self.avg_diff):
            diff = np.random.normal(0, 0.5*self.avg_diff, 1).tolist()[0]
            self.time.append(i+diff)
            self.value.append(self.test_f(i+diff))
            self.error.append(np.random.normal()*(self.amplitude))
        self.ts = TimeSeries(self.time, self.value, self.error)
