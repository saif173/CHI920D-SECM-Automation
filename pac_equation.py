import numpy as np
import matplotlib.pyplot as plt

L_test_data = np.linspace(0, 3, 200)
rg = 10
k = 1.09175558e-11

def alpha_is(rg):
    alpha = np.log(2) + np.log(2)*(1 - (2/np.pi * np.arccos(1/rg))) 
    - np.log(2)*(1 - (2/np.pi * np.arccos(1/rg))**2)
    return alpha

def beta_is(rg):
    beta = ( 1 + 0.639 * (1 - (2/np.pi) * np.arccos(1/rg)) 
                   - 0.186 * (1 - ((2/np.pi) * np.arccos(1/rg))**2) )
    return beta

alpha = alpha_is(rg)
beta =beta_is(rg)
print("beta is", beta)

#positive feedback
def pf_equation(L, alpha, beta):
    return alpha + (np.pi/(beta*4*np.arctan(L))) + (1 - alpha - 1/(2*beta)) * ((2/np.pi) * np.arctan(L))

print(pf_equation(7, alpha, beta))
pf_curve = pf_equation(L_test_data, alpha, beta)

#negative feedback
def nf_equation(L, rg):
    return ((2.08/rg**0.358)*(L-0.145/rg) + 1.585)*((2.08/rg**0.358)*(L+0.0023*rg) + 1.57 + (np.log(rg)/L)+((2/(np.pi*rg))*np.log(1 + (np.pi*rg)/(2*L))))**-1

nf_curve = nf_equation(L_test_data, rg)

#combined positive and negative feedback

def pac_total(pf,nf,k, L, rg):
    return (pf + (nf - 1)/((1+2.47*(rg**0.31)*L*k)*(1+L**(0.006*rg+0.113)*k**(-0.0236*rg + 0.91))))

pf_curve_special = pf_equation(L_test_data + 1/k, alpha, beta)

total_pac_curve = pac_total(pf_curve_special,nf_curve, k, L_test_data, rg)

#plotting curves
"""plt.plot(L_test_data, pf_curve)
plt.xlabel("L")
plt.ylabel("I")
plt.title("PAC Curve from Equation (Positive feedback)")
plt.grid(True)
plt.show()

plt.plot(L_test_data, nf_curve)
plt.xlabel("L")
plt.ylabel("I")
plt.title("PAC Curve from Equation (Negative feedback)")
plt.grid(True)
plt.show()

plt.plot(L_test_data, total_pac_curve)
plt.xlabel("L")
plt.ylabel("I")
plt.title("total PAC Curve from Equation (mixed)")
plt.grid(True)
plt.show()
"""