import csv
from data import *
import os
from estimateCAMs import *
from macroscopicParams import *

# TRACK DATA (highD recordingMeta.csv)
METAFILE = "_recordingMeta.csv"
ID = 0
FRAMERATE = 1
DURATION = 7
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
FRONT_SIGHT_DISTANCE = 10
DHW = 12  # distance headway


# Read all the data about one recording as specified by the path
def read_recording(path):
    # Global data
    vehicle_amount = None
    fps = None
    duration = None
    cams = 0

    # Data per vehicle
    frame_amounts = []
    avg_speeds = []
    headway_dict = {}
    position_dict = {}
    velocity_dict = {}

    sniffer = csv.Sniffer()

    # Get the number of vehicles
    with open(path + METAFILE) as metadata:
        # Remove the header (variable names row) of the metadata of the recording
        has_header = sniffer.has_header(metadata.read(1024))
        metadata.seek(0)

        reader = csv.reader(metadata)
        if has_header:
            next(reader)

        # View that meta data of this recording
        for row in reader:
            vehicle_amount = int(row[NUM_VEHICLES])
            fps = int(row[FRAMERATE])
            duration = float(row[DURATION])

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

            avg_velocity = float(row[AVG_VELOCITY])
            avg_speeds.append(avg_velocity)

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
            position_dict = add_to_dict(position_dict, vehicle, position)

            # Fill in the vehicle velocity dictionary
            velocity = (float(row[X_VELOCITY]), float(row[Y_VELOCITY]))
            velocity_dict = add_to_dict(velocity_dict, vehicle, velocity)

            # Fill in the vehicle distance headway directionary
            # When the headway is 0 (no preceding car), take the front distance
            headway = float(row[DHW])
            if headway == 0:
                headway = float(row[FRONT_SIGHT_DISTANCE])
            headway_dict = add_to_dict(headway_dict, vehicle, headway)

    # Get the CAM prediction per vehicle in the track
    vehicle_id = 1
    while vehicle_id <= vehicle_amount:
        cams += vehicle_cams(fps, vehicle_id, frame_amounts[vehicle_id - 1], position_dict[vehicle_id], velocity_dict[vehicle_id])
        vehicle_id += 1

    # Get the macroscopic parameter values for this recording
    flow, density, speed = calculate_macroscopic_params(vehicle_amount, duration, headway_dict, avg_speeds)

    print("Path: ", path)
    print("     ", flow, " vehicles/s")
    print("     ", density, " vehicles/m")
    print("     ", speed, " m/s")
    print("     ", cams, " cams")
    print(" ")


def add_to_dict(dictionary, key, value):
    if key in dictionary:
        values = dictionary[key]
        values.append(value)
    else:
        values = [value]
    dictionary[key] = values
    return dictionary



# Read each track in the data
if __name__ == "__main__":
    track_num = 1
    path = 'data/01'

    # For testing purposes (only look at recording 1):
    # read_recording(path)

    # Read code:

    while os.path.exists(path + '_tracks.csv'):
        read_recording(path)
        track_num += 1
        if track_num < 10:
            path = 'data/0' + str(track_num)
        else:
            path = 'data/' + str(track_num)

