import process_pac_data
import plotly.graph_objects as go
import numpy as np

#negative feedback
coeffs_negative = {
    1002: (0.13219, 3.37167, 0.8218, -2.34719),
    100: (0.27997, 3.05419, 0.68612, -2.7596),
    50.9: (0.30512, 2.6208, 0.66724, -2.6698),
    20.1: (0.35541, 2.0259, 0.62832, -2.55622),
    15.2: (0.37377, 1.85113, 0.61385, -2.49554),
    10.2: (0.40472, 1.60185, 0.58819, -2.37294),
    8.13: (0.42676, 1.46081, 0.56874, -2.28548),
    5.09: (0.48678, 1.17706, 0.51241, -2.07873),
    3.04: (0.60478, 0.86083, 0.39569, -1.89455),
    2.03: (0.76179, 0.60983, 0.23866, -2.03267),
    1.51: (0.90404, 0.42761, 0.09743, -3.23064),
    1.11: (-1.46539, 0.27293, 2.45648, 8.995e-7),
    10: (0.292, 1.151, 0.6553, -2.4035),
}


#positive feedback
coeffs_positive = {
    1002: (0.7314, 0.77957, 0.26298, -1.29077),
    10.2: (0.72627, 0.76651, 0.26015, -1.41332),
    5.1: (0.72035, 0.75128, 0.26651, -1.62091),
    1.51: (0.63349, 0.67476, 0.36509, -1.42897),
    10: (0.68, 0.78377, 0.3315, -1.0672),
}


L_values = np.linspace(0.1, 10, 100)

def positive_PAC_curve(A, B, C, D):
    return A + (B / L_values) + C * np.exp(D / L_values)

def negative_PAC_curve(A, B, C, D):
    return 1/(A + (B / L_values) + C * np.exp(D / L_values))


positive_PAC_curves = {}
for Rglass, coeffs in coeffs_positive.items():
    positive_PAC_curves[Rglass] = positive_PAC_curve(*coeffs)

negative_PAC_curves = {}
for Rglass, coeffs in coeffs_negative.items():
    negative_PAC_curves[Rglass] = negative_PAC_curve(*coeffs)


def plot(x, y, axis1, axis2, title):

    fig = go.Figure()
    fig.add_trace(
    go.Scatter(
    x=x,
    y=y,
    mode="lines+markers",
    marker=dict(size=5),
    ))

    fig.update_layout(
        xaxis_title=axis1,
        yaxis_title=axis2,
        title=title,
        template="plotly_white"
    )

    fig.update_xaxes(range=[min(x), max(x)])
    fig.update_yaxes(range=[min(y), max(y)])

    return fig








