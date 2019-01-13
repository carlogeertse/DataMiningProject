import scipy as sp
from scipy.io.arff import loadarff
from secoda import Secoda
import time

print("\nHelix:")
helix = loadarff("data\\Helix.arff")
helix_data = helix[0]
helix_data = helix_data.astype([('x1', '<f8'), ('x2', '<f8'), ('x3', '<f8'), ('color', 'U6')])
i = 0
for color in helix_data['color']:
    helix_data['color'][i] = helix_data['color'][i][1:-1]
    i = i + 1
helix_anomalies = Secoda(helix_data)
print(helix_data[[i[0] for i in helix_anomalies[0:5]]])

print("\nMountain:")
mountain = loadarff("data\\mountain.arff")
mountain_data = mountain[0]
mountain_data = mountain_data.astype([('x1', '<f8'), ('x2', '<f8'), ('x3', '<f8')])
mountain_anomalies = Secoda(mountain_data)
print(mountain_data[[i[0] for i in mountain_anomalies[0:5]]])

print("\nNoisyMix:")
NoisyMix = loadarff("data\\NoisyMix.arff")
NoisyMix_data = NoisyMix[0]
NoisyMix_data = NoisyMix_data.astype(
    [('x', '<f8'), ('y', '<f8'), ('z', '<f8'), ('CodeColor', 'U11'), ('CodeType', 'U7')])
i = 0
for color in NoisyMix_data['CodeColor']:
    NoisyMix_data['CodeColor'][i] = NoisyMix_data['CodeColor'][i][1:-1]
    i = i + 1
i = 0
for color in NoisyMix_data['CodeType']:
    NoisyMix_data['CodeType'][i] = NoisyMix_data['CodeType'][i][1:-1]
    i = i + 1
NoisyMix_anomalies = Secoda(NoisyMix_data)
print(NoisyMix_data[[i[0] for i in NoisyMix_anomalies[0:5]]])

print("\nTimeSeries:")
TimeSeries = loadarff("data\\TimeSeries.arff")
TimeSeries_data = TimeSeries[0]
TimeSeries_data = TimeSeries_data.astype([('Time', '<f8'), ('AverageWage', '<f8')])
TimeSeries_anomalies = Secoda(TimeSeries_data)
print(TimeSeries_data[[i[0] for i in TimeSeries_anomalies[0:5]]])

run_time = {1: 0, 10: 0, 100: 0, 1000: 0, 3500: 0}
for key in run_time.keys():
    start = time.perf_counter()
    Secoda(NoisyMix_data[0:key])
    end = time.perf_counter()
    run_time[key] = end - start
print('\n',run_time)