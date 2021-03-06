
import pyvisa as visa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import time
import numpy as np
from tqdm import tqdm


def meas_potentials():
    potentials = np.arange(initial_voltage, (final_voltage + voltage_step), voltage_step)
    return [value for value in reversed(potentials)] if meas_direction == 'r' else potentials


def prepare_meter():
    current_meter.write('*rst; *cls')
    current_meter.write('conf:curr:dc 10mA, 0.01mA')
    current_meter.write('func "curr:dc"')
    current_meter.write('disp:state off')
    current_meter.write('syst:beep:state off')


def ask_voltage(voltage):
    return float(input(f'Qual a tensão {voltage} da medida em V? \n'))


def ask_scan_direction():
    temp_direction = input('Qual a direção da medida? \n r para reverse \n f para forward \n').lower()
    while temp_direction.lower() != 'f' and temp_direction.lower() != 'r':
        temp_direction = input('Parâmetro inválido, digite novamente: \n r para reverse \n f para forward \n')
        print(temp_direction.lower())
    return temp_direction.lower()


def ask_device_area():
    return float(input('Qual a área do dispositivo em cm^2 ? \n'))


def ask_meas_rate():
    return float(input('Qual a velocidade da medida em V/s? \n'))


def measurement():
    temp_current_values = []
    temp_offset_potential = []
    temp_cell_power = []

    for n in tqdm(list(range(0, len(meas_potentials())))):
        potential_source.write('volt:offs ' + str((meas_potentials()[n] / 2)))
        time.sleep(0.05)
        temp_current_values.append(float(current_meter.query('meas:curr:dc? 10mA, 0.01mA')))
        temp_offset_potential.append((float(potential_source.query('volt:offs?'))))
        temp_cell_power.append(
                float(current_meter.query('meas:curr:dc? 10mA, 0.01mA')) *
                float(potential_source.query('volt:offs?'))
            )
    return temp_current_values, temp_offset_potential, temp_cell_power


def ask_file_name():
    return input('Insira o caminho para salvar o arquivo e o nome do arquivo.')


def find_open_circuit_voltage():
    if len(open_circuit_voltage_index) == 1:
        value = output_data.loc[int(open_circuit_voltage_index), 'Voltage (V)']
    else:
        value = output_data.loc[int(open_circuit_voltage_index), 'Voltage (V)'].mean()
    return value


rm = visa.ResourceManager()
potential_source = rm.open_resource('GPIB0::10::INSTR')
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')

initial_voltage = ask_voltage('inicial')

final_voltage = ask_voltage('final')

scan_rate = ask_meas_rate()

device_area = ask_device_area()

meas_direction = ask_scan_direction()

incident_power = 100

voltage_step = 0.01

points_number = float((final_voltage + abs(initial_voltage) + 1) / voltage_step)

step_speed = voltage_step / scan_rate


potential_source.write('outp on; disp off')
prepare_meter()

current_values, offset_potential, cell_power = measurement()

potential_source.write('outp off')

# ani = FuncAnimation(plt.gcf(), measurement, (int(step_speed*1000)))
current_values_table = pd.Series(current_values).transpose()

app_potential = [value * 2 for value in offset_potential]

current_density = [-1 * value * pow(base=10, exp=3) / device_area for value in current_values]

cell_power = [-1 * value * pow(base=10, exp=3) / device_area for value in cell_power]

output_data = pd.DataFrame([app_potential, current_density, cell_power])\
    .transpose()\
    .set_axis(['Voltage (V)', 'j (mA/cm2)', 'Cell Power (mW/cm2)'], axis=1)

maximum_power_point = output_data['Cell Power (mW/cm2)'].max()

short_circuit_current_index = output_data[output_data['Voltage (V)'] == 0.0].index.values
short_circuit_current = output_data.loc[int(short_circuit_current_index), 'j (mA/cm2)']

open_circuit_voltage_index = output_data[
        output_data['j (mA/cm2)'].abs() ==
        output_data['j (mA/cm2)'].abs().min()
    ]\
    .index.values

open_circuit_voltage = find_open_circuit_voltage()

fill_factor = (maximum_power_point * 100) / (open_circuit_voltage * short_circuit_current)

power_conversion_efficiency = (fill_factor * open_circuit_voltage * short_circuit_current) / incident_power
cell_params = pd.DataFrame(
    [
        short_circuit_current,
        open_circuit_voltage,
        fill_factor,
        power_conversion_efficiency
    ],
    index=[
        'Jsc (mA/cm2)', 'Voc (V)', 'FF (%)', 'PCE (%)'
    ],
    columns=['Cell Parameters']
    )
output_data = cell_params.append(output_data, sort=True)

plt.plot(output_data['Voltage (V)'], output_data['j (mA/cm2)'])
plt.plot(output_data['Voltage (V)'], output_data['Cell Power (mW/cm2)'], 'r')
plt.scatter(open_circuit_voltage, output_data.loc['j (mA/cm2)', 'Cell Parameters'].abs().min())
plt.scatter(0.0, short_circuit_current)
plt.show()

output_data = cell_params.append(output_data, sort=True)
output_data.to_csv(ask_file_name(), sep='\t')
