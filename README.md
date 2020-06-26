# Tool to analyse macroscopic parameters against CAM generations
The tool can be used to convert a set of microscopic traffic parameters into the corresponding macroscopic traffic 
parameters and an estimation of the Cooperative Awareness Message generations.

## Input format
The HighD data set was used in the development of this tool. 
HighD is a large set of vehicle trajectory data from German highways available for non-commercial use at https://www.highd-dataset.com/. 
Each recording in this data set has three csv files, each starting with the recording ID (indicated as XX below). 
- XX_recordingMeta: contains general recording data, such as the total number of vehicles in that recording.
- XX_tracksMeta: contains data per track, a track being the data concerning a particular vehicle within a recording. 
An example of this is the number of frames that a vehicle is in the recording.
- XX_tracks: contains frame-specific data of vehicles, such as their x- and y-velocity.

The input data must be placed in the data folder.

The relevant data for this script is defined as global variables in main.py, which collects this data from the input file,
runs the functions to calculate the macroscopic parameters and CAM generations,
and then writes the results to an output csv file.
These variables may be at a different index when using another input data set (this can easily be changed in main.py),
but this three-file structure must be adhered to in order to run the tool. 

## Running the tool
To use the tool, run main.py. While it is running, the file paths will be printed as it finishes the calculations for each path. 
Once the program is finished running, the results will appear in the same folder as main.py in a file named results.csv. 
This csv file can then be opened in a spreadsheet program of your choice. 
If you run the calculations again, the previous contents of results.csv will be overwritten.
