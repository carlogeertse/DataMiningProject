import operator

import numpy as np


def Secoda(data):
    i = 0  # iteration number
    b = 2  # amount of bins for discretisation
    s = 1  # stopping criterion
    average_anomaly_score, pruned_anomaly_scores = {}, {}
    data_list = [data]
    cont = True  # Helper variable due to do while not existing in python
    while cont:
        data = data_list[i]
        i = i + 1
        disc_data = discretize_continuous(np.copy(data), b)
        constellation_frequencies = calculate_constellation_frequencies(disc_data)
        if i > 1:  # If not on first loop
            average_anomaly_score = dict(enumerate(
                (np.fromiter(average_anomaly_score.values(), dtype=float) + np.array(constellation_frequencies)) / 2,
                0))
        else:
            average_anomaly_score = dict(enumerate(constellation_frequencies, 0))
        if i <= 10:  # Smaller steps for early iterations
            s = s + 0.1
            b = b + 1
            data_list.append(data)
        else:
            s = s + 1
            b = b + (s - 2)
            # Start pruning cases that are very likely to be 'normal'
            quantile_95 = np.quantile(np.fromiter(average_anomaly_score.values(), dtype=float), 0.95)
            to_be_pruned = {key: value for key, value in average_anomaly_score.items() if value >= quantile_95}
            pruned_anomaly_scores = {**pruned_anomaly_scores, **to_be_pruned}
            data_list.append(np.delete(data, np.fromiter(to_be_pruned.keys(), dtype=int), 0))
        anomaly_keys = [key for key, value in average_anomaly_score.items() if value <= s]
        anomalies = data[anomaly_keys]
        if len(anomalies) / len(data) > 0.003:
            cont = False
    average_anomaly_score = {**average_anomaly_score, **pruned_anomaly_scores}
    return sorted(average_anomaly_score.items(),
                  key=operator.itemgetter(1))  # Sort by anomaly score and return as tuples


def discretize_continuous(data, b):
    dtypes = data.dtype
    for name in dtypes.names:
        if np.issubdtype(dtypes[name], np.number):  # Only discretize numbers
            attribute = data[name]
            bin_edges = np.histogram_bin_edges(attribute, b)
            data[name] = np.digitize(data[name],
                                     bin_edges[:-1])  # digitize needs to be open ended on either the left or the right
    return data


def calculate_constellation_frequencies(data):
    # First we create the constellations
    constellations = {}
    constellation_data = []
    for row in data:
        constellation = ''
        for attribute in row:
            constellation = constellation + '{0}-'.format(attribute)
        constellation_data.append(constellation)
        if constellation not in constellations:
            constellations[constellation] = 0
        constellations[constellation] = constellations[constellation] + 1
    constellation_frequencies = []
    for i in range(0, len(data)):
        constellation_frequencies.append(constellations[constellation_data[i]])
    return constellation_frequencies
