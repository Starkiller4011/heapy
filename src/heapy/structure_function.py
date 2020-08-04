#!/usr/bin/env python3
from __future__ import division, print_function

# %% Imports
import sys
import numpy as np
from matplotlib import pyplot as plt

#%%
class StructureFunction:
    """
    Structure Function class
    """
    def __init__(self, time_series, name='structure_function'):
        self.time_series = time_series
        self.name = name
        self.duration = self.time_series.time[len(self.time_series.time)-1]-self.time_series.time[0]
        self.CalculateResolution()
        self.bins = int(self.duration/self.resolution)
        self.Initialize()
        self.calculated = False
        self.Calculate()
    def CalculateResolution(self):
        deltas = []
        for i in range(1, len(self.time_series.time)):
            deltas.append(self.time_series.time[i]-self.time_series.time[i-1])
        self.resolution = np.median(deltas)
    def Initialize(self):
        self.sf = {}
        self.raw_sf = {}
        self.raw_errors = {}
        for i in range(1, self.bins+1):
            midpoint = ((i-(1/2))*self.resolution)
            self.raw_sf[midpoint] = []
            self.raw_errors[midpoint] = []
    def Calculate(self):
        time = self.time_series.time
        value = self.time_series.value
        error = self.time_series.error
        N_e = len(time)
        for i in range(0, N_e - 1):
            for j in range(i, N_e):
                tau = time[j] - time[i]
                for btau in self.raw_sf.keys():
                    if tau >= (btau - (self.resolution/2)) and tau < (btau + (self.resolution/2)):
                        self.raw_sf[btau].append(np.power(value[j] - value[i], 2))
                        self.raw_errors[btau].append(error[i])
                        self.raw_errors[btau].append(error[j])
                        break
        self.BinRawSF()
        self.calculated = True
    def BinRawSF(self):
        taus = []
        values = []
        errors = []
        sigmas = []
        for tau in self.raw_sf.keys():
            sigmas.append(np.var(self.raw_errors[tau]))
        sigma_noise = 2.0 * np.average(sigmas)
        for tau in self.raw_sf.keys():
            if len(self.raw_sf[tau]) > 6:
                value = (np.average(self.raw_sf[tau] - sigma_noise)/self.time_series.sigma)
                sf_err = (np.sqrt(np.var(self.raw_sf[tau]))/np.sqrt(len(self.raw_sf[tau])/2))/self.time_series.sigma
                taus.append(tau)
                values.append(value)
                errors.append(sf_err)
        self.sf['tau'] = taus
        self.sf['sf'] = values
        self.sf['error'] = errors
    def ConvertToXspec(self):
        tau_start = []
        tau_stop = []
        taus = self.sf['tau'].copy()
        values = self.sf['sf'].copy()
        errors = self.sf['error'].copy()
        for i in range(0, len(taus) - 1):
            diff = (taus[i+1] - taus[i])/2
            tau_start.append(taus[i]-diff)
            tau_stop.append(taus[i]+diff)
        diff = (taus[len(taus)-1]-taus[len(taus)-2])/2
        tau_start.append(taus[len(taus)-1]-diff)
        tau_stop.append(taus[len(taus)-1]+diff)
        xsf = {'start':tau_start,'stop':tau_stop,'sf':values,'error':errors}
        return xsf
    def Plot(self, fmt='.', cutoff=None, save=False):
        if not self.calculated:
            print('Structure function not calculated, nothing to plot')
            return
        taus = self.sf['tau']
        values = self.sf['sf']
        errors = self.sf['error']
        if cutoff is not None:
            index = 0
            while taus[index] < cutoff:
                index += 1
                if index >= len(taus):
                    index = len(taus)
                    break
            taus = taus[:index-1]
            values = values[:index-1]
            errors = errors[:index-1]
        fig = plt.figure(figsize=(7, 10))
        plot = fig.add_subplot(1, 1, 1)
        fig.suptitle('Structure Function', fontsize=18)
        plot.set_xlabel(r'$\tau$', fontsize=16)
        plot.set_ylabel(r'$SF\left(\tau\right)$', fontsize=16)
        plt.errorbar(taus, values, yerr=errors, fmt=fmt, label='SF')
        plt.xscale('log')
        plt.yscale('log')
        if save:
            savename = '%s_sf.png' % self.name
            plt.savefig(savename)
        else:
            plt.show()
