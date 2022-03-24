import pyvisa
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np


def meas_potentials():
    return np.arange(initial_voltage, final_voltage + voltage_step, voltage_step)


def ask_voltage(voltage):
    return float(input(f'Qual a tensão {voltage} da medida em V? \n'))


def ask_voltage_step():
    return float(input('Qual o passo de potencial desejado em V/passo? \n'))


def ask_meas_rate():
    return float(input('Qual a velocidade da medida em V/s? \n'))


rm = pyvisa.ResourceManager()
potential_source = rm.open_resource('GPIB::10::INSTR')
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')

initial_voltage = ask_voltage('inicial')
final_voltage = ask_voltage('final')
voltage_step = ask_voltage_step()
scan_rate = ask_meas_rate()
step_speed = voltage_step / scan_rate


potential_source.write('outp on')

current_values = []
app_potential = []

for n in list(range(0, len(meas_potentials()))):
    potential_source.write('volt:offs ' + str(meas_potentials()[n]))
    time.sleep(step_speed)
    current_values.append(float(current_meter.query('meas:curr:dc?')))
    app_potential.append((float(potential_source.query('volt:offs?'))))

potential_source.write('outp off')

plt.plot(app_potential, current_values)
plt.show()

output_data = pd.DataFrame([app_potential, current_values])\
    .transpose()\
    .set_axis(['Tensão (V)', 'Corrente (mA)'], axis=1)

output_data.to_csv('C:/Users/robee/Desktop/j_v_tests.txt', sep='\t', index=False)
