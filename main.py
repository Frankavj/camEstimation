import csv
from data import *
import os
from estimateCAMs import *

# GENERAL DATA STRUCTURE INFO
FPS = 25

# TRACK DATA (highD recordingMeta.csv)
METAFILE = "_recordingMeta.csv"
ID = 0
NUM_VEHICLES = 10

# VEHICLE DATA (PER TRACK) (highD tracksMeta.csv)
TRACKMETAFILE = "_tracksMeta.csv"
FRAMES = 5
DIRECTION = 7
DISTANCE = 8
AVG_VELOCITY = 11

# FRAME DATA (PER VEHICLE) (highD tracks.csv)
TRACKFILE = "_tracks.csv"
VEHICLE_ID = 1
X_POSITION = 2
Y_POSITION = 3
X_VELOCITY = 6
Y_VELOCITY = 7
X_ACCELERATION = 8
Y_ACCELERATION = 9
DHW = 12  # distance headway
THW = 13  # time headway


# Read all the data about one recording as specified by the path
def read_recording(path):
    vehicle_amount = None
    frame_amounts = []
    position_dict = {}
    velocity_dict = {}
    sniffer = csv.Sniffer()
    cams = 0

    # Get the number of vehicles per recording
    with open(path + METAFILE) as metadata:
        # Remove the header (variable names row) of the metadata of the recording
        has_header = sniffer.has_header(metadata.read(1024))
        metadata.seek(0)

        reader = csv.reader(metadata)
        if has_header:
            next(reader)

        # View that meta data of this recording
        for row in reader:
            print("Recording " + row[ID] + " has " + row[NUM_VEHICLES] + " vehicles.")
            vehicle_amount = int(row[NUM_VEHICLES])

    # Get the number of frames per vehicle
    with open(path + TRACKMETAFILE) as trackmeta:
        # Remove the header (variable names row) of the trackmeta data of the recording
        has_header = sniffer.has_header(trackmeta.read(1024))
        trackmeta.seek(0)

        reader = csv.reader(trackmeta)
        if has_header:
            next(reader)

        # Store the number of frames for each vehicle in the recording
        for row in reader:
            frames = int(row[FRAMES])
            frame_amounts.append(frames)

    # Fill the vehicle dictionaries
    with open(path + TRACKFILE) as trackdata:
        # Remove the header (variable names row) of the trackdata of the recording
        has_header = sniffer.has_header(trackdata.read(2048))
        trackdata.seek(0)

        reader = csv.reader(trackdata)
        if has_header:
            next(reader)

        for row in reader:
            vehicle = int(row[VEHICLE_ID])

            # Fill in the vehicle position dictionary
            position = (float(row[X_POSITION]), float(row[Y_POSITION]))
            if vehicle in position_dict:
                values = position_dict[vehicle]
                values.append(position)
            else:
                values = [position]
            position_dict[vehicle] = values

            # Fill in the vehicle velocity dictionary
            velocity = (float(row[X_VELOCITY]),float(row[Y_VELOCITY]))
            if vehicle in velocity_dict:
                values = velocity_dict[vehicle]
                values.append(velocity)
            else:
                values = [velocity]
            velocity_dict[vehicle] = values

    # Get the CAM prediction per vehicle in the track
    vehicle_id = 1
    while vehicle_id <= vehicle_amount:
        cams += vehicle_cams(FPS, vehicle_id, frame_amounts[vehicle_id - 1], position_dict[vehicle_id], velocity_dict[vehicle_id])
        vehicle_id += 1


# Read each track in the data
if __name__ == "__main__":
    track_num = 1
    path = 'data/01'

    # For testing purposes (only look at recording 1):
    read_recording(path)

    # Read code:

    # while os.path.exists(path + '_tracks.csv'):
    #     read_track(path)
    #     track_num += 1
    #     if track_num < 10:
    #         path = 'data/0' + str(track_num)
    #     else:
    #         path = 'data/' + str(track_num)

