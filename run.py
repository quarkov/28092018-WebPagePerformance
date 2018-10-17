import numpy as np
from matplotlib import pyplot as plt
from core.functions import*
from core.web_page_open import*
from core.classes import*
import os
import csv

latency_time = w_latency_time if os.name == "nt" else l_latency_time

hostname = input_hostname()
filename = store_dir(hostname)

duration, freq = input_params()
tests_number = duration*60//freq + 1

results = open(filename + ".csv", "a")
csv.writer(results).writerows([['time', 'ping', 'load']])

plt.figure(figsize=(10, 0.5*tests_number))
fig, ax = plt.subplots()
ax.set_title(filename, size=10)
ax.set_xlabel('time, ms')
ax.xaxis.grid(True)
ax.invert_yaxis()
ind = np.arange(tests_number)
p = plt.barh(ind, 0, height=0.5, color='blue', label='loading time')
l = plt.barh(ind, 0, height=0.5, color='green', label='ping')
plt.legend((l, p), ('ping', 'loading time'), loc=4)
plt.savefig(filename + ".svg")

web_page_open(filename, freq)

for test in range(tests_number):
    start = time.time()
    lat_thread = ThreadValue(target=latency_time, args=[hostname])
    per_thread = ThreadValue(target=page_loading, args=[hostname])
    sleep_thread = ThreadValue(target=time.sleep, args=[freq])
    lat_thread.start(), per_thread.start(), sleep_thread.start()
    clock, latency, load = now(), lat_thread.join(), per_thread.join()
    print(clock)
    csv.writer(results).writerows([[clock, latency, load]])
    p = plt.barh(clock, load, color='blue', height=0.5)
    l = plt.barh(clock, latency, color='green', height=0.5)
    print(clock)
    fig.canvas.draw()
    plt.savefig(filename + ".svg")
    sleep_thread.join()
    print("ok", time.time() - start)
results.close()
