import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re

files = os.listdir() # list all files in the current working directory
files = [file for file in files if re.match(".*.dat$", file)] # exclude files that are not .dat files

# make an output folder to store images
try:
       os.makedirs("Processed", exist_ok = True)
except Exception as e:
       sys.exit(e)

# generate and colour each image
for file in files:
    with open(file, "r") as f:
        img = np.loadtxt(f)
    # Determine the contrast min and max based on file name
        if '_1705-1760' in file:
                contrast_min, contrast_max = 0.05, 0.5
        elif '_1480-1590' in file:
                contrast_min, contrast_max = 0, 2.5
        elif '_1725-1760' in file:
                contrast_min, contrast_max = 0, 0.3
        elif '_2907-2944' in file:
                contrast_min, contrast_max = 0.05, 0.225
        elif '_2946-2880' in file:
                contrast_min, contrast_max = 0, 0.225    
        elif any(substr in file for substr in ["_2946-2980", "_2865-2885", "_3000-3020"]):
               contrast_min, contrast_max = 0, 0.2
        elif "VN_1480-1590_1725-1770" not in file and any(substr in file for substr in ["_2840-2865", "_1725-1770"]):
               contrast_min, contrast_max = 0, 0.08
        else:
               contrast_min, contrast_max = 0, 0.15

        # Save figure as is
        fig, ax = plt.subplots()
        image = ax.imshow(img, interpolation="bilinear", cmap="jet", vmin=contrast_min, vmax=contrast_max)
        plt.colorbar(image, ax=ax)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(f"Processed{os.sep}{file[:-4]}.tiff_vmin={contrast_min}_vmax={contrast_max}_jet.tiff", dpi=300)

        print(f"Processed file: {file}")