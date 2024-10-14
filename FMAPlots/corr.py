import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from FMAPlots.colors import Colors

class Corr: 
    def import_dataset(workingDir, subworkingDir, fName, nAtoms, nModes):
        skipme = np.array([((nAtoms*i + (2*i) + 0),(nAtoms*i + (2*i) + 1)) for i in range(nModes)]).flatten()
        reps = [1,2,3,4,5]
        data = np.array([np.array(pd.read_csv(f"{workingDir}/{subworkingDir}_{i}/{fName}", skiprows=skipme, sep = r"\s+", usecols=[1,2,3], header=None)).reshape(nModes,nAtoms*3) for i in reps])
        return data
    
    def get_modes_from_dataset(dataset, mStart, mEnd):
        s1, s2 = mStart-1,mStart-1
        e1, e2 = mEnd-1,mEnd-1
        nR = len(dataset)
        corr = np.zeros( (nR, nR, e1-s1+1, e2-s2+1) )
        for rep1 in range(nR):
            for rep2 in range(nR):
                for i in range(e1-s1+1):
                    for j in range(e2-s2+1):
                        corr[rep1, rep2, i, j] = np.dot(dataset[rep1, s1+i], dataset[rep2, s2+j])
        return corr
    
    def plot_correlation_from_modes(corr, systemname, nR=5):
        colormapping = Colors.define_RYG_colormap()
        fig, ax = plt.subplots(nR, nR, figsize=(10,10))
        annotme = True
        fig.suptitle(f"Correlation of Modes from {systemname} Replicas", fontsize=20)
        for r1 in range(nR):
            for r2 in range(nR):
                im = ax[r1,r2].imshow(np.abs(corr[r1, r2]), vmin=0.5, vmax=1.01,cmap=colormapping, extent=[6,9,6,9], origin='lower')
                # Loop over data dimensions and create text annotations.
                if annotme == True:
                    for i in range(len(corr[r1,r2])):
                        for j in range(len(corr[r1,r2,0])):
                            text = ax[r1,r2].text(6.5+j, 6.5+i, f"{np.abs(np.round(corr[r1,r2, i, j], 2))}",
                                               ha="center", va="center", color="black", fontsize=12)
                # Define the positions where you want the ticks
                tick_positions = [6.5, 7.5, 8.5]
                
                # Define the custom labels corresponding to the tick positions
                tick_labels = ['7', '8', '9']
                
                # Set the custom ticks and labels for both x and y axes
                ax[r1,r2].set_xticks(tick_positions)
                ax[r1,r2].set_xticklabels(tick_labels)
                
                ax[r1,r2].set_yticks(tick_positions)
                ax[r1,r2].set_yticklabels(tick_labels)
                ax[r1,r2].set_title(f"Replica {r1+1} -> {r2+1}")
                fig.tight_layout()
        
        cbar_ax = fig.add_axes([1, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
        fig.colorbar(im, cax=cbar_ax, label="Correlation")
        plt.tight_layout(rect=[0, 0, 1, 0.98])
        return fig, ax