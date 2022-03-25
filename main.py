import pyvisa
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
from tqdm import tqdm


def meas_potentials():
    potentials = np.arange(initial_voltage, (final_voltage + voltage_step), voltage_step)
    return [value for value in reversed(potentials)] if meas_direction == 'r' else potentials


def prepare_meter():
    current_meter.write('*rst; *cls')
    current_meter.write('func "curr:dc"')


def ask_voltage(voltage):
    return float(input(f'Qual a tensão {voltage} da medida em V? \n'))


def ask_scan_direction():
    temp_direction = input('Qual a direção da medida? \n r para reverse \n f para forward \n').lower()
    while temp_direction.lower() != 'f' and temp_direction.lower() != 'r':
        temp_direction = input('Parâmetro inválido, digite novamente: \n r para reverse \n f para forward \n')
        print(temp_direction.lower())
    return temp_direction.lower()


def ask_meas_rate():
    return float(input('Qual a velocidade da medida em V/s? \n'))


def measurement():
    temp_current_values = []
    temp_offset_potential = []

    for n in tqdm(list(range(0, len(meas_potentials())))):
        potential_source.write('volt:offs ' + str((meas_potentials()[n] / 2)))
        time.sleep(step_speed)
        temp_current_values.append(float(current_meter.query('meas:curr:dc?')))
        temp_offset_potential.append((float(potential_source.query('volt:offs?'))))
    return temp_current_values, temp_offset_potential


rm = pyvisa.ResourceManager()
potential_source = rm.open_resource('GPIB::10::INSTR')
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')

initial_voltage = ask_voltage('inicial')

final_voltage = ask_voltage('final')

scan_rate = ask_meas_rate()

meas_direction = ask_scan_direction()

voltage_step = 0.05

points_number = float((final_voltage + abs(initial_voltage) + 1) / voltage_step)

step_speed = voltage_step / scan_rate


potential_source.write('outp on')
prepare_meter()

current_values, offset_potential = measurement()
# current_values = []
# offset_potential = []
#
# for n in tqdm(list(range(0, len(meas_potentials())))):
#     potential_source.write('volt:offs ' + str((meas_potentials()[n] / 2)))
#     time.sleep(step_speed)
#     current_values.append(float(current_meter.query('meas:curr:dc?')))
#     offset_potential.append((float(potential_source.query('volt:offs?'))))

potential_source.write('outp off')

app_potential = [value * 2 for value in offset_potential]

plt.plot(app_potential, current_values, 'o')
plt.show()

output_data = pd.DataFrame([app_potential, current_values])\
    .transpose()\
    .set_axis(['Tensão (V)', 'Corrente (mA)'], axis=1)

output_data.to_csv('C:/Users/robee/Desktop/j_v_tests.txt', sep='\t', index=False)
