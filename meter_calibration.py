
import pyvisa
import time
from tqdm import tqdm
from datetime import datetime

rm = pyvisa.ResourceManager()
current_meter = rm.open_resource('USB0::0x0957::0x0618::MY50310013::0::INSTR')
current_meter.write('*rst; *cls')

current_meter.write('cal:sec:stat off,at34405')
current_meter.write('conf:curr:dc')
current_meter.write('cal:val 9.9e+37')
current_meter.write('cal?')
for n in tqdm(range(0,9), desc='Evaluating autozero'):
    time.sleep(5)

print('Connect the 10 mA source to the I/LO terminals of the multimeter.')
time.sleep(10)

current_meter.write('conf:curr:dc 0.01')
current_meter.write('cal:val 0.01')
current_meter.write('cal?')
time.sleep(60)

print('Insert 100 mA source')
time.sleep(30)

current_meter.write('conf:curr:dc 0.1')
current_meter.write('cal:val 0.1')
current_meter.write('cal?')
time.sleep(60)

print('Insert 1 A source')
time.sleep(30)

current_meter.write('conf:curr:dc 1')
current_meter.write('cal:val 1')
current_meter.write('cal?')
time.sleep(60)

current_meter.write('cal:str "Cal Date: "')

current_meter.write('cal:sec:stat on,at34405')

