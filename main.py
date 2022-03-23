import pyvisa
import matplotlib.pyplot as plt
import pandas as pd
import time

rm = pyvisa.ResourceManager()
potential_source = rm.open_resource('GPIB::10::INSTR')
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')
stabilization = 1
final_voltage = 1
initial_voltage = 0
step = 0.01
points_number = int(final_voltage / step)

potential_source.write('volt 1, min')
print(potential_source.query('volt? min'))
#
# potential_source.write('OUTP ON')
# # potential_source.write('APPL 2')
# current_meter.query('MEAS:CURR:DC?')
#
# potential_source.write('VOLT:STEP ' + str(step))
#
# potential_source.write('APPL 0')
# time.sleep(0.5)
# current_values = [float(current_meter.query('MEAS:CURR:DC?'))]
#
# for n in list(range(0, points_number)):
#     potential_source.write("VOLT UP")
#     time.sleep(0.5)
#     current = current_meter.query('MEAS:CURR:DC?')
#     current_values.append(float(current))
#
# potential_source.write('OUTP OFF')
#
# app_potential = [value * step for value in list(range(0, (points_number + 1)))]
#
# output_data = pd.DataFrame([app_potential, current_values])\
#     .transpose()\
#     .set_axis(['Tensão (V)', 'Corrente (mA)'], axis=1)
#
# output_data.to_csv('C:/Users/robee/Desktop/j_v_tests.txt', sep='\t', index=False)
#
# plt.plot(app_potential, current_values)
# plt.show()
