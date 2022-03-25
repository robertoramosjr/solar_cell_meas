import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

i_v = pd.read_csv("C:/Users/robee/Desktop/j_v_tests.txt", sep='\t')

v, i = i_v.iloc[3:, :1], i_v.iloc[3:, 1:]

array_v, array_i = v.transpose().to_numpy(), i.transpose().to_numpy()

plt.plot(array_v[0], array_i[0], 'or')
plt.show()

