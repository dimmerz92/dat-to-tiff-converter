# dat-to-tiff-converter

## Preamble
This program was made to assist a researcher to convert dat image/spectra files generated by Bruker Opus at the Australian Synchtrotron to a more portable and easy to use image format (tif).

Please feel free to pinch this code and rework it to suit your needs. If you need help, I'm happy to assist and answer questions.

## Dependencies
- tkinter: is typicall distributed with Python, however, if you do not have it you can usually download it with apt/homebrew depending on your OS.
- matplotlib: (gridspec, pyplot)
- numpy
- math
- sys
- os
- re

## How it works
1. Tkinter is used to open a file dialogue for ease of directory searching.
  - Select the directory containing your .dat image/spectra files.
  - Click OK/Open, depending on the version and OS you have.
2. This version of the datToTif python file will use regex to determine which files are your spectra.
  - The files will be sorted using this regex based on a specific file naming convention, it is recommended that you either change this section to match your file naming convention, or change your naming convention to suit this regex.
3. A number of output folders will be created to contain the image outputs.
  - Some will have scales and legends and some will just be the image.
4. The images will run through some logic to determine the correct contrast treatments and subsequently saved using matplotlib.
5. Finally, prior to completion, the program will generate a combined figure containing all images generated into one figure.

## Assumptions:
- The .dat file should only contain tab delimited integers or floats of a single channel greyscale nature.

## TLDR (what it does):
Reads the contents of the current working directory, converts all .dat files found to a colorised .tif image.

## How to use:
1. Ensure the python script is in the same directory as all .dat images (you do not need to worry if there are other files in the directory, the script will ignore anything that is not a .dat file)
2. Run the script using ```python3 datToTif.py```
3. A new output directory will have been added to the working directory, all saved images will be in that folder.