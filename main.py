import csv
from data import *
import os

# TRACK DATA INDEXES
ID = 0
NUM_VEHICLES = 10

# VEHICLE DATA INDEXES (PER TRACK)
DIRECTION = 7
DISTANCE = 8
AVG_VELOCITY = 11

# FRAME DATA INDEXES (PER VEHICLE)
VEHICLE_ID = 1
X_POSITION = 2
Y_POSITION = 3
X_VELOCITY = 6
Y_VELOCITY = 7
X_ACCELERATION = 8
Y_ACCELERATION = 9
DHW = 12  # distance headway
THW = 13  # time headway


# Read data about one track as specified by the path
def read_track(path):
    with open(path + '_recordingMeta.csv') as metadata:
        has_header = csv.Sniffer().has_header(metadata.read(1024))
        metadata.seek(0)

        metaReader = csv.reader(metadata)
        if has_header:
            next(metaReader)  # Don't need the rows with the variables names

        for row in metaReader:
            print("Recording " + row[ID] + " has " + row[NUM_VEHICLES] + " vehicles.")
            # Get the CAM prediction per vehicle in the track
            # for vehicle_id in row[NUM_VEHICLES]:
            #     #read_


# Read each track in the data
if __name__ == "__main__":
    track_num = 1
    path = 'data/01'

    while os.path.exists(path + '_tracks.csv'):
        read_track(path)
        track_num += 1
        if track_num < 10:
            path = 'data/0' + str(track_num)
        else:
            path = 'data/' + str(track_num)
