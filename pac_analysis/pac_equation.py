import numpy as np


def alpha_is(rg):
    alpha = np.log(2) + np.log(2)*(1 - (2/np.pi * np.arccos(1/rg))) 
    - np.log(2)*(1 - (2/np.pi * np.arccos(1/rg))**2)
    return alpha

def beta_is(rg):
    beta = ( 1 + 0.639 * (1 - (2/np.pi) * np.arccos(1/rg)) 
                   - 0.186 * (1 - ((2/np.pi) * np.arccos(1/rg))**2) )
    return beta



#positive feedback
def pf_equation(L, alpha, beta):
    return alpha + (np.pi/(beta*4*np.arctan(L))) + (1 - alpha - 1/(2*beta)) * ((2/np.pi) * np.arctan(L))

#negative feedback
def nf_equation(L, rg):
    return ((2.08/rg**0.358)*(L-0.145/rg) + 1.585)*((2.08/rg**0.358)*(L+0.0023*rg) + 1.57 + (np.log(rg)/L)+((2/(np.pi*rg))*np.log(1 + (np.pi*rg)/(2*L))))**-1



#combined positive and negative feedback

def pac_total(pf,nf,k, L, rg):
    return (pf + (nf - 1)/((1+2.47*(rg**0.31)*L*k)*(1+L**(0.006*rg+0.113)*k**(-0.0236*rg + 0.91))))
