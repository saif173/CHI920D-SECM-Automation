import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.optimize import curve_fit, brentq
from pac_analysis.pac_equation import alpha,beta, rg, nf_equation, alpha_is, beta_is
from pac_analysis.process_pac_data import flip_data, normalize_data
"""from process_pac_data import rel_I, rel_L, pure_L,pure_I

#removes negative values from rel_L and scales size of rel_I

mask = (rel_L >0) & (rel_L<3) #avoid L=0 because numerical instability
rel_L = rel_L[mask]
rel_I = rel_I[mask]

mask2 = (pure_L>=0.1)&(pure_L<=2.9)
pure_L=pure_L[mask2]
pure_I=pure_I[mask2]"""

#defining the model
def model(L, k,rg):
    """Defines the theoretical model"""
    nf_curve = nf_equation(L, rg)
    return (alpha_is(rg) + (np.pi/(beta_is(rg)*4*np.arctan(L+1/k))) + (1 - alpha_is(rg) - 1/(2*beta_is(rg))) * ((2/np.pi) * np.arctan(L+1/k)) 
            + (nf_curve - 1)/((1+2.47*(rg**0.31)*L*k)*(1+L**(0.006*rg+0.113)*k**(-0.0236*rg + 0.91))))

def shifted_model(L, k, rg, shift):
    """Horizontally shifts the model so that L=0 corresponds to the
    specified y-value."""

    # Calculate model over a range of L values
    x_values = np.linspace(0.001, 100, 10000)
    y_values = model(x_values, k, rg)

    # Find the x value where the model is closest to the desired shift
    index = np.argmin(np.abs(y_values - shift))
    L_shift = x_values[index]

    # Shift the model horizontally
    return model(L + L_shift, k, rg)
#using a curve-fit to find k
def find_k(rel_L, rel_I, rg):

    params, covariance = curve_fit(
        lambda L, k: model(L, k, rg),
        rel_L,
        rel_I,
        p0=[2.0],
        bounds=(1e-6, np.inf)
    )

    return params[0]

def find_k_shift(rel_L, rel_I, rg, shift):
    params, covariance = curve_fit(
        lambda L, k: shifted_model(L, k, rg, shift),
        rel_L,
        rel_I,
        p0=[2.0],
        bounds=(0.001, 100)
    )

    return params[0]

"""k= find_k(rel_L,rel_I,rg)
k2= find_k(pure_L,pure_I,rg)
print("k for experiment is", k)
print("k for theory is", k2)"""

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

def find_i_infi_shift(L_data, I_data, touch_point, a, rg,shift):
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
        k = find_k_shift(rel_L, rel_I, rg, shift)
        pred = shifted_model(rel_L, k, rg, shift)
        error = rms_error(rel_I,pred)
        error_list.append(error)

    index = np.argmin(error_list)
    i_infi = i_values[index]

    return i_infi
        
def find_k_deluxe(L_data, I_data, rg , a, zero_point):
    i_infi = find_i_infi(L_data,I_data,zero_point,a,rg)
    rel_L, rel_I = normalize_data(L_data, I_data, zero_point, a, i_infi)
    k = find_k(rel_L, rel_I,rg)
    
    return k

def find_k_deluxe_shift(L_data, I_data, rg , a, zero_point, shift):
    i_infi = find_i_infi_shift(L_data,I_data,zero_point,a,rg, shift)
    rel_L, rel_I = normalize_data(L_data, I_data, zero_point, a, i_infi)
    k = find_k_shift(rel_L, rel_I,rg, shift)
    
    return k



"""pred = model(rel_L, k,rg)
pred2 = model(pure_L, k2,rg)"""

#finding the rms percentage error between model and data
def rms_error(rel_I, pred):
    """Finds the root-mean-square percentage error between theoretical model
    and experimental data"""

    rmse = np.sqrt(np.mean(((rel_I - pred)/rel_I)**2))
    rmse_percent = 100 * rmse
    return rmse_percent

"""print("rms error for experimental is", rms_error(rel_I, pred),"%")
print("rms error for theoretical is", rms_error(pure_I,pred2),"%" )

plt.plot(rel_L, pred, label = "model")
plt.plot(pure_L,pure_I, label = "pure")
plt.plot(pure_L,pred2, label="pure fit")
plt.plot(rel_L, rel_I, label = "experimental data")
plt.plot(rel_L, model(rel_L,2.5,rg), label = "k=2.5")
plt.plot(rel_L, model(rel_L,4,rg), label = "k=4")
plt.plot(rel_L, model(rel_L,3,rg), label = "k=3")
plt.plot(rel_L, model(rel_L,0.01,rg), label = "k=0.01")
plt.plot(rel_L, model(rel_L,0.1,rg), label = "k=0.1")
plt.plot(rel_L, model(rel_L,1,rg), label = "k=1")
plt.plot(rel_L, model(rel_L,10,rg), label = "k=10")
#plt.plot(rel_L, model(rel_L,100,rg), label = "k=100")
plt.xlabel("L")
plt.ylabel("I")
plt.legend()
plt.ylabel("model")
plt.title("model")
plt.grid(True)
plt.show()


residuals = rel_I - pred

plt.figure()
plt.plot(rel_L, residuals, '.')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel("Relative L")
plt.ylabel("Residual")
plt.title("Residual Plot")
plt.show()"""



















