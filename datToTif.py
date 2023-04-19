import sys
import os
import re
import numpy as np
from PIL import Image, ImageOps

files = os.listdir() # list all files in the current working directory
files = [file for file in files if re.match(".*.dat$", file)] # exclude files that are not .dat files

# make an output folder to store images
output = "tif_outputs"
try:
    os.mkdir(output)
except FileExistsError:
    sys.exit("tif_outputs folder exists")

# generate and colour each image
for file in files:
    with open(file, "r") as f:
        data = f.readlines()
        lines = [line.strip().split("\t") for line in data] # splits on the tab delimiter and strips whitespace
        for i in range(len(lines)):
            lines[i] = [float(line.strip()) for line in lines[i]] # removes whitespace from individual list items
        image = np.array(lines) # convert to array
        image = (image - image.min())/(image.max() - image.min()) * 255# normalise data
        image = ImageOps.colorize(Image.fromarray(image).convert("L"), "yellow", "blue") # colorise on the interval 0 = yellow to 1 = blue
        image.save(f"{output}/{file[:-3]}tif") # save the image to the directory