import tkinter as tk
from tkinter import filedialog
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math
import sys
import os
import re

# set the subset of files required
FILE_SUBSET = "01" # ENTER THE IDENTIFIER HERE
FIG_TITLE = "Test Fig" # ENTER TITLE FOR AGGREGATE FIGURE

# select directory
root = tk.Tk()
root.withdraw()
try:
    path = filedialog.askdirectory()
    if not path:
            sys.exit("\n\nUser cancelled operation\n")
    os.chdir(path)
except Exception as e:
    sys.exit(e)

# get file names and figure titles
files = os.listdir() # list all files in the current working directory
files = [file for file in files if re.match(f"\d{{3}}\_{FILE_SUBSET}\_\d{{1}}\-\w+\.tiff$", file)] # exclude files that are not .tiff files
files.sort() # sorts files in lexicographical order
titles = [re.search("(?<=\-)\w+", title).group(0) for title in files] # extract titles from filenames

# make an output folder to store images
try:
    os.makedirs("processed", exist_ok = True)
    os.makedirs("scale", exist_ok = True)
    os.makedirs("axis_scale", exist_ok = True)
except Exception as e:
       sys.exit(e)

# apply colourmap to each image
images = []
contrasts = []
for i, file in enumerate(files):
    img = Image.open(file)
    img = np.array(img)
    images.append(img)
        
    # Determine the contrast min and max based on file name
    if 'Al' in file:
        contrast_min, contrast_max = 0, 6
    elif 'Ar' in file:
        contrast_min, contrast_max = 0, 5.5
    elif 'Ca' in file:
        contrast_min, contrast_max = 0, 0.03
    elif 'CeL' in file:
        contrast_min, contrast_max = 0.01, 0.05
    elif 'Cl' in file:
        contrast_min, contrast_max = 0, 0.2
    elif 'Co' in file:
        contrast_min, contrast_max = 0.05, 0.6
    elif 'Cr' in file:
        contrast_min, contrast_max = 0, 0.04
    elif 'Cu' in file:
        contrast_min, contrast_max = 0, 0.1
    elif 'Fe' in file:
        contrast_min, contrast_max = 0, 0.01
    elif 'K' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'Mn' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'Ni' in file:
        contrast_min, contrast_max = 0, 0.15  
    elif 'P' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'S' in file:
        contrast_min, contrast_max = 0, 0.15  
    elif 'Se' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'Si' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'Ti' in file:
        contrast_min, contrast_max = 0, 0.15
    elif 'Zn' in file:
        contrast_min, contrast_max = 3, 40
    elif 'Back' in file:
        contrast_min, contrast_max = 0, 0.15  
    elif 'Compton' in file:
        contrast_min, contrast_max = 0, 0.15 
    elif 'elastic' in file:
        contrast_min, contrast_max = 0, 0.15 
    elif 'Flux0' in file:
        contrast_min, contrast_max = 0, 0.15 
    elif 'Flux1' in file:
        contrast_min, contrast_max = 0, 0.15                 
    else:
        contrast_min, contrast_max = 0, 0.15

    # save contrasts
    contrasts.append([contrast_min, contrast_max])

    # Save individual figure
    fig, ax = plt.subplots()
    image = ax.imshow(img, interpolation="bilinear", cmap="jet", vmin=contrast_min, vmax=contrast_max)
    plt.axis("off")
    plt.gca().invert_yaxis()
    plt.savefig(f"processed{os.sep}{file[:-4]}_vmin={contrast_min}_vmax={contrast_max}_jet.tiff", dpi=300)
    plt.colorbar(image, ax=ax)
    plt.savefig(f"scale{os.sep}{file[:-4]}_vmin={contrast_min}_vmax={contrast_max}_jet.tiff", dpi=300)
    plt.axis("on")
    plt.savefig(f"axis_scale{os.sep}{file[:-4]}_vmin={contrast_min}_vmax={contrast_max}_jet.tiff", dpi=300)
    plt.close(fig)

    print(f"Processed file: {file}")

# build the combined figure
ncols = 6
nrows = math.ceil(len(files) / ncols)

fig = plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(nrows=nrows, ncols=ncols)

for i, img in enumerate(images):
    ax = plt.subplot(gs[i])
    ax.imshow(img, interpolation="bilinear", cmap="jet", vmin=contrasts[i][0], vmax=contrasts[i][1])
    ax.set_title(titles[i])
    ax.set_axis_off()

plt.suptitle(FIG_TITLE, fontweight="bold", fontsize="x-large")
plt.tight_layout()
fig.savefig(f"{FIG_TITLE}.tiff")