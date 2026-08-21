import numpy as np
import plotly.graph_objects as go
from scipy.optimize import curve_fit 
from pac_analysis.pac_equation import  nf_equation, alpha_is, beta_is
from pac_analysis.process_pac_data import flip_data, normalize_data

#defining the model
def model(L, k,rg):
    """Defines the theoretical model"""
    nf_curve = nf_equation(L, rg)
    return (alpha_is(rg) + (np.pi/(beta_is(rg)*4*np.arctan(L+1/k))) + (1 - alpha_is(rg) - 1/(2*beta_is(rg))) * ((2/np.pi) * np.arctan(L+1/k)) 
            + (nf_curve - 1)/((1+2.47*(rg**0.31)*L*k)*(1+L**(0.006*rg+0.113)*k**(-0.0236*rg + 0.91))))

#using a curve-fit to find k
def find_k(rel_L, rel_I, rg):
    """Uses curve-fit to find k with the relative distance and currents"""

    params, covariance = curve_fit(
        lambda L, k: model(L, k, rg),
        rel_L,
        rel_I,
        p0=[2.0],
        bounds=(1e-6, np.inf)
    )

    return params[0]


#plotting the model against experimental data
def plot_model(rel_L, rel_I, k_value, rg):
    """Uses plotly to plot the experimental data against the model"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=rel_L,
            y=rel_I,
            mode="lines",
            name="Experimental data"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=rel_L,
            y=model(rel_L, k_value, rg),
            mode="lines",
            name="Model"
        )
    )

    fig.update_layout(
        xaxis_title="L",
        yaxis_title="I",
        title="Model",
        template="plotly_white"
    )

    return fig

def find_i_infi(L_data, I_data, touch_point, a, rg):
    """Finds the value of the bulk current 
    that gives a curve-fit with the minimum error"""
    L_data = flip_data(L_data)
    rel_L = (L_data - touch_point) / a
    mask = (rel_L>0)&(rel_L<5)
    rel_L=rel_L[mask]
    i_values = np.linspace(1e-9,1e-8,100)
    error_list=[]

    for i in i_values:
        rel_I = (I_data/i)[mask]
        k = find_k(rel_L, rel_I, rg)
        pred = model(rel_L, k, rg)
        error = rms_error(rel_I,pred)
        error_list.append(error)

    index = np.argmin(error_list)
    i_infi = i_values[index]

    return i_infi


        
def find_k_deluxe(L_data, I_data, rg , a, zero_point):
    """Finds k given the raw L and I data"""
    i_infi = find_i_infi(L_data,I_data,zero_point,a,rg)
    rel_L, rel_I = normalize_data(L_data, I_data, zero_point, a, i_infi)
    k = find_k(rel_L, rel_I,rg)
    
    return k



#finding the rms percentage error between model and data
def rms_error(rel_I, pred):
    """Finds the root-mean-square percentage error between theoretical model
    and experimental data"""

    rmse = np.sqrt(np.mean(((rel_I - pred)/rel_I)**2))
    rmse_percent = 100 * rmse
    return rmse_percent



















