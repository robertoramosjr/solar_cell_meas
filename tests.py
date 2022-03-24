import pandas as pd
import matplotlib.pyplot as plt
import pyvisa
import time
import numpy as np

i_v = pd.read_csv("C:/Users/robee/Desktop/j_v_tests.txt", sep='\t')

v, i = i_v.iloc[3:, :1], i_v.iloc[3:, 1:]

array_v, array_i = v.transpose().to_numpy(), i.transpose().to_numpy()

plt.plot(array_v[0], array_i[0], 'or')
plt.show()

rm = pyvisa.ResourceManager()
potential_source = rm.open_resource('GPIB::10::INSTR')
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')


def meas_potentials():
    return np.arange(initial_voltage, final_voltage + step, step)


"""
from here, another way to make the source apply potential. Tests will be done to see how is more reliable
"""
#
final_voltage = 1.2
initial_voltage = - 0.1
step = 0.1

potential_source.write('outp on')

app_potential = []
meas_volt = []
print(type(meas_potentials()))


for n in list(range(0, len(meas_potentials()))):
    potential_source.write('appl:dc def, def, ' + str(meas_potentials()[n] / 2))
    time.sleep(1)
    app_potential.append((float(potential_source.query('volt:offs?'))))
    meas_volt.append(float((current_meter.query('meas:volt:dc?'))))
potential_source.write('outp off')

print(app_potential, meas_volt)
