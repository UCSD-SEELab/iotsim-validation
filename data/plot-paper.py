#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
x = ['RPi0_1\nmeasure\nScene 1', 'RPi0_1\nRelIoT\nScene 1', 'RPi0s\nmeasure\nScene 1', 'RPi0s\nRelIoT\nScene 1', #     'RPi0_1\nmeasure\nScene 2', 'RPi0_1\nRelIoT\nScene 2', 'RPi0_2,3,4\nmeasure\nScene 2', 'RPi0_2,3,4\nRelIoT\nScene 2', \
    'RPi0_1\nmeasure\nScene 3', 'RPi0_1\nRelIoT\nScene 3', 'RPi0s\nmeasure\nScene 3', 'RPi0s\nRelIoT\nScene 3']

scene = []
scene.append([1115.45, 2034.75, 630.48])
scene.append([1115.45, 2034.75, 630.48])
scene.append([994.10, 1865.24, 654.26]) # 3
scene.append([994.10, 1865.24, 654.26]) # 3
#scene.append([1100.06, 2053.04, 652.43])
#scene.append([1100.06, 2053.04, 652.43])
#scene.append([959.72, 1876.21, 605.48]) # 3
#scene.append([959.72, 1876.21, 605.48]) # 3
scene.append([966.69, 1971.95, 632.31])
scene.append([966.69, 1971.95, 632.31])
scene.append([869.42, 1929.87, 602.43]) # 3
scene.append([869.42, 1929.87, 602.43]) # 3
scene = np.array(scene)

avgPower_r = scene[:, 0]
maxPower_r = scene[:, 1]
minPower_r = scene[:, 2]
print(avgPower_r, maxPower_r, minPower_r)

plt.figure()
x_pos = [1, 2, 3, 4, 5, 6, 7, 8]
lavg, = plt.plot(x_pos, avgPower_r, 'bo', markersize=5, label='avg. power')
lmax, = plt.plot(x_pos, maxPower_r, 'b_', markersize=20, label='max power')
lmin, = plt.plot(x_pos, minPower_r, 'g_', markersize=20, label='min power')
# plt.xlabel("Energy Source")
plt.ylabel("Power (mW)")
plt.title("Power measurement and simulation results in Scenario 1 and 3.")
plt.legend()

plt.xticks(x_pos, x)
plt.savefig('./power.png', dpi=300)


# In[23]:


y = ['RPi0_1\nmeasure\nScene 2', 'RPi0_1\nRelIoT\nScene 2', 'RPi0s\nmeasure\nScene 2', 'RPi0s\nRelIoT\nScene 2', #     'RPi0_1\nmeasure\nScene 2', 'RPi0_1\nRelIoT\nScene 2', 'RPi0_2,3,4\nmeasure\nScene 2', 'RPi0_2,3,4\nRelIoT\nScene 2', \
    'RPi0_1\nmeasure\nScene 3', 'RPi0_1\nRelIoT\nScene 3', 'RPi0s\nmeasure\nScene 3', 'RPi0s\nRelIoT\nScene 3']

scene = []
#scene.append([42.46, 44.4, 39.0])
#scene.append([42.46, 44.4, 39.0])
#scene.append([41.26, 42.2, 39.5]) # 3
#scene.append([41.26, 42.2, 39.5]) # 3
scene.append([58.39, 61.6, 54.1])
scene.append([58.39, 61.6, 54.1])
scene.append([39.42, 41.2, 35.8]) # 3
scene.append([39.42, 41.2, 35.8]) # 3
scene.append([59.12, 61.6, 55.1])
scene.append([59.12, 61.6, 55.1])
scene.append([38.79, 40.1, 37.4]) # 3
scene.append([38.79, 40.1, 37.4]) # 3
scene = np.array(scene)

avgTemp_r = scene[:, 0]
maxTemp_r = scene[:, 1]
minTemp_r = scene[:, 2]
print(avgTemp_r, maxTemp_r, minTemp_r)

plt.figure()
y_pos = [1, 2, 3, 4, 5, 6, 7, 8]
lavg, = plt.plot(x_pos, avgTemp_r, 'bo', markersize=5, label='avg. temperature')
lmax, = plt.plot(x_pos, maxTemp_r, 'b_', markersize=20, label='max temperature')
lmin, = plt.plot(x_pos, minTemp_r, 'g_', markersize=20, label='min temperature')
# plt.xlabel("Energy Source")
plt.ylabel("Temperature (°C)")
plt.title("Temperature measurement and simulation results in Scenario 2 and 3.")
plt.legend()

plt.xticks(y_pos, y)
plt.savefig('./temp.png', dpi=300)


# In[ ]:




