import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import MaxNLocator
from FMAPlots.colors import Colors

class Fes():
    def helloworld():
        print("Hello World")
    def import_data(workingDir, subWorkingDir, fName, nReps, lim=100001):
        reps = np.arange(0, nReps,1)
        nFramesPerRep = lim
        kT = 2.49
        weights = np.zeros((len(reps),nFramesPerRep))
        cv_x = np.zeros((len(reps),nFramesPerRep))
        cv_y = np.zeros((len(reps),nFramesPerRep))
        for r in reps:
            df = np.loadtxt(f"{workingDir}/{subWorkingDir}_{r}/{fName}",skiprows=1, usecols=[3,4,-1])[:nFramesPerRep]
            cv_x[r] = df[:,0]
            cv_y[r] = df[:,1]
            weights[r] = np.exp(df[:,2]/kT) 
        return cv_x, cv_y, weights
    
    def get_histograms(cv_x, cv_y, weights, xmin, xmax, ymin, ymax):
        histograms = [np.histogram2d(cv_x[r], cv_y[r], range=[[xmin, xmax], [ymin, ymax]], bins=[100,100], weights=weights[r]) for r in range(len(cv_x))]
        return histograms
    
    def get_probability(histograms, nReps):
        kT = 2.49
        avg_p = np.copy(histograms[0][0])
        for H in histograms:
            avg_p = np.add(avg_p, H[0])
        avg_p = avg_p/nReps
        avg_g = np.copy(avg_p)
        for i in range(len(avg_p)):
            for j in range(len(avg_p[i])):
                if avg_p[i,j] > 0:
                    avg_g[i,j] = -kT*np.log10(avg_p[i,j])
                else:
                    avg_g[i,j] = 100
        avg_g = avg_g - np.min(avg_g)
        return avg_p, avg_g
        
    def plot_FES(avg_g, histograms, cv1_label, cv2_label):
        extended_cmap = Colors.define_RYGBP_colormap()
        hist = avg_g.T
        binx = histograms[0][1]
        biny = histograms[0][2]
        fig, ax = plt.subplots(figsize=(5,5))
        im = ax.imshow(hist, aspect=1, interpolation='nearest', origin='lower', extent=[binx[0], binx[-1], biny[0], biny[-1]],cmap=extended_cmap, vmin=0,vmax=60)
        ax.set_xlabel(f"{cv1_label}")
        ax.set_ylabel(f"{cv2_label}")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))  # 6 total x-ticks
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6))  # 6 total y-ticks
        cbar_ax = fig.add_axes([0.95, 0.2, 0.05, 0.585]) 
        cbar = plt.colorbar(im, cax=cbar_ax, label = "Free Energy (kJ/mol)")
