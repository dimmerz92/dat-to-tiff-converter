# dat-to-tiff-converter

Takes a tab delimited .dat file and converts it to a colorised .tif image.

Assumptions:
the .dat file should only contain tab delimited integers or floats of a single channel greyscale nature.

What it does:
Reads the contents of the current working directory, converts all .dat files found to a colorised .tif image.

How to use:
1. Ensure the python script is in the same directory as all .dat images (you do not need to worry if there are other files in the directory, the script will ignore anything that is not a .dat file)
2. Run the script using ```python3 datToTif.py```
3. A new output directory will have been added to the working directory, all saved images will be in that folder.