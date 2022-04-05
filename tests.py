import pyvisa as visa
import time

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::10::INSTR')



source.write('*rst')
frequency = (0.2 / 1.2)
source.write('outp on')
source.write('appl:ramp 1, 1.2, -0.1')
time.sleep(30)
