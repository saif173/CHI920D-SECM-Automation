import plotly.graph_objects as go




def plot(x, y, axis1, axis2, title):
    """Simplified plotting function"""

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








