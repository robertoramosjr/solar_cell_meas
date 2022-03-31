import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

i_v = pd.read_csv("C:/Users/robee/Desktop/j_v_tests.txt", sep='\t')

v, i = i_v.iloc[:, :1], i_v.iloc[:, 1:]

array_v, array_i = v.transpose().to_numpy(), i.transpose().to_numpy()

short_circuit_current_index = i_v[i_v['Voltage (V)'] == 0.0].index.values
short_circuit_current = i_v.loc[int(short_circuit_current_index), 'j (mA/cm2)']
print(short_circuit_current)

open_circuit_voltage_index = i_v[i_v['j (mA/cm2)'] == i_v['j (mA/cm2)'].abs().min()].index.values

open_circuit_voltage = i_v.loc[int(open_circuit_voltage_index), 'Voltage (V)']
print(open_circuit_voltage)

i_v['Jsc'] = short_circuit_current

plt.plot(array_v[0], array_i[0])
plt.plot(i_v['Voltage (V)'], i_v['cell power mW'], 'r')
plt.scatter(open_circuit_voltage, i_v['j (mA/cm2)'].abs().min())
plt.scatter(0.0, short_circuit_current)
plt.show()
