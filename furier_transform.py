import os
import pandas as pd
from io import StringIO
from scipy.fft import rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cmath

with open('01_S_01_vzduch.lvm', 'r') as file:
    data = file.readlines()

for num, i in enumerate(data):
    if i[0] == '0':
        data = data[num:len(data)]
        break

num_columns = data[0].count('\t')
data = ' '.join(data)

if num_columns == 1:
    headers = ['time', 'sensor1']
else:
    headers = ['time', 'sensor1', 'sensor2', 'sensor3']
df = pd.read_csv(StringIO(data), sep="\t", names=headers, engine='python')
print(df)
n = 200000
freq = n/df['time'].iloc[len(df)-1]
xf = rfftfreq(n, 1/freq)
yf1 = rfft(np.array(df['sensor1']))
yf2 = rfft(np.array(df['sensor2']))
yf3 = rfft(np.array(df['sensor3']))
yf = [yf1, yf2, yf3]

print('frequency [Hz]:', '        ', 'amplitude [Hz]:', '         ', 'phase [deg]:')
for count, i in enumerate(yf):
    print(f'sensor{count+1}:')
    for num in range(1, 4):
        peaks, properties = find_peaks(np.abs(i), height=10000)
        xx = i[peaks][num]
        print(xf[peaks][num], '\t', properties['peak_heights'][num], '\t', np.degrees(cmath.phase(xx)))
    print('')

fig, ax = plt.subplots()
ax.plot(xf, np.abs(yf1), color='purple')
# ax.plot(xf, np.abs(yf2), color='red')
# ax.plot(xf, np.abs(yf3), color='orange')
ax.plot(xf[peaks], properties['peak_heights'], 'x')  # mark peaks in graph
ax.set(xlim=(10, 1000))
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel('amplitude [Hz]')
plt.show()

