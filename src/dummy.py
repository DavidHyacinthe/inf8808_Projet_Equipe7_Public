import numpy as np
import plotly.graph_objects as go

# THIS FILE IS JUST A DUMMY TO FILL THE BLANKS IN THE APPLICATION 
# DELETE THIS BEFORE 


def dummy_line(fig) :
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='sin(x)'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='cos(x)'))
    
    fig.update_layout(
        title='Dummy Line chart',
        xaxis_title='x',
        yaxis_title='y'
    )
    
    return fig
    