import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import MaxNLocator

class Colors:
    def define_RYGBP_colormap():
        # Create a custom colormap from blue to red
        colors = [
            (1, 0, 1),
            (0, 0, 1),    # Blue (0, 0, 1)
            (0, 1, 1),    # Cyan (0, 1, 1)
            (0, 1, 0),    # Green (0, 1, 0)
            (1, 1, 0),    # Yellow (1, 1, 0)
            (1, 0.65, 0), # Orange (1, 0.65, 0)
            (1, 0, 0)    # Red (1, 0, 0)
        ]  
        cmap = mcolors.LinearSegmentedColormap.from_list('RYGBP', colors)
        
        
        # Modify the colormap to include white for values above the max value (vmax)
        extended_colors = [cmap(i) for i in range(cmap.N)] + [(1, 1, 1, 1)]  # Add white color
        extended_cmap = mcolors.ListedColormap(extended_colors)
        return extended_cmap

    def define_RYG_colormap():
        
        colors = [
            (0, 1, 0),    # Green (0, 1, 0)
            (1, 1, 0),    # Yellow (1, 1, 0)
            (1, 0, 0)    # Red (1, 0, 0)
        ]  
        cmap = mcolors.LinearSegmentedColormap.from_list('RYG', colors)
        
        
        # Modify the colormap to include white for values above the max value (vmax)
        extended_colors = [(1, 1, 1, 1)] + [cmap(i) for i in range(cmap.N)] + [(1, 1, 1, 1)]  # Add white color
        extended_cmap = mcolors.ListedColormap(extended_colors)
        return extended_cmap