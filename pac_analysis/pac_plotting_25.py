import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


folder = Path(__file__).parent

L_data, I_data = np.loadtxt(folder / "pacs_gold_1.txt", unpack=True)

a=5

initial_current = I_data[-1]
index = np.argmin((np.abs(I_data - initial_current) / initial_current) - 0.25)
zero_point = L_data[index]
print(zero_point)
print(initial_current)
print(I_data[index])


#normalizing L and I data
rel_L = L_data / a
rel_I = I_data / initial_current


plt.plot(L_data, I_data, label='PAC curve')
plt.xlabel("L")
plt.ylabel("I")
plt.title("PAC Curve")
plt.grid(True)
plt.show()

plt.plot(rel_L, rel_I)
plt.xlabel("normalized L")
plt.ylabel("normalized I")
plt.title("Normalized PAC Curve")
plt.grid(True)
plt.show()
