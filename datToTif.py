import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os
import re

files = os.listdir() # list all files in the current working directory
files = [file for file in files if re.match(".*.dat$", file)] # exclude files that are not .dat files
titles = [re.search("((?=[A-Za-z])(?:(?!_SM|_CELL).)*)", title).group(1) for title in files] # extract titles from filenames
fig_title = [*set([re.search("((?=CELL)(?:(?!_[A-Z]).)*)", title).group(1) for title in files])][0].replace("_", " ")

# sort in desired lexicographic order
titles = sorted(titles, key=lambda x:(1,x) if ":" in x else (0,x.upper()))
order={v:i for i, v in enumerate(titles)}
files = sorted(files, key=lambda x:order[re.search("((?=[A-Za-z])(?:(?!_SM|_CELL).)*)", x).group(1)])

# make an output folder to store images
try:
       os.makedirs("Processed", exist_ok = True)
except Exception as e:
       sys.exit(e)

images = []

# generate and colour each image
for i, file in enumerate(files):
        with open(file, "r") as f:
                img = np.loadtxt(f)
                images.append(img)
    # Determine the contrast min and max based on file name
        if '1705-1760' in file:
                contrast_min, contrast_max = 0.05, 0.5
        elif '1480-1590' in file:
                contrast_min, contrast_max = 0, 2.5
        elif '1725-1760' in file:
                contrast_min, contrast_max = 0, 0.3
        elif '2907-2944' in file:
                contrast_min, contrast_max = 0.05, 0.225
        elif '2946-2880' in file:
                contrast_min, contrast_max = 0, 0.225    
        elif any(substr in file for substr in ["2946-2980", "2865-2885", "3000-3020"]):
                contrast_min, contrast_max = 0, 0.2
        elif "VN_1480-1590_1725-1770" not in file and any(substr in file for substr in ["2840-2865", "1725-1770"]):
                contrast_min, contrast_max = 0, 0.08
        else:
                contrast_min, contrast_max = 0, 0.15

        # Save individual figure
        fig, ax = plt.subplots()
        image = ax.imshow(img, interpolation="bilinear", cmap="jet", vmin=contrast_min, vmax=contrast_max)
        plt.colorbar(image, ax=ax)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(f"processed{os.sep}{file[:-4]}.tiff_vmin={contrast_min}_vmax={contrast_max}_jet.tiff", dpi=300)
        plt.close(fig)

        print(f"Processed file: {file}")


# build the combined figure
ncols = 6
nrows = math.ceil(len(files) / ncols)


fig = plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(nrows=nrows+1, ncols=ncols, height_ratios=[0.02] + [1]*(nrows))

# Add column titles
col_titles = np.tile(["Area Under Curve", "Normalised"], ncols//2)
for i, title in enumerate(col_titles):
        ax = plt.subplot(gs[i])
        ax.axis("off")
        ax.set_title(title, fontweight="bold")

for i, img in enumerate(images):
        ax = plt.subplot(gs[i + ncols])
        ax.imshow(img, interpolation="bilinear", cmap="jet", vmin=contrast_min, vmax=contrast_max)
        ax.set_title(titles[i])
        ax.set_axis_off()

plt.suptitle(fig_title, fontweight="bold", fontsize="x-large")
plt.tight_layout()
fig.savefig(f"{fig_title}.tiff")