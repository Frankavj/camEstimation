from statistics import mean


def calculate_macroscopic_params(vehicle_amount, duration, headway_dict, avg_speeds):
    flow = vehicle_amount / duration
    speed = mean(avg_speeds)

    headways = []
    for vehicle in headway_dict:
        headways.append(mean(headway_dict[vehicle]))

    density = 1 / mean(headways)

    return flow, density, speed