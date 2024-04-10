'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.graph_objects as go
from tqdm import tqdm

WHITE = 'rgb(255, 255, 255)'
GREEN = 'rgb(68, 237, 27)'
PURPLE = 'rgb(213, 69, 244)'
GOLD = 'rgb(245, 193, 54)'
GREY = 'rgb(112, 106, 105)'

def get_figure(data, column_width):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick. The x and y axes should
        be titled "Year" and "Neighborhood". 

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''

    # Create the heatmap
    fig = go.Figure()    
    fig.add_trace(go.Heatmap(
                            x=data['X'], 
                            y = data['Y'], 
                            z=data['color'], 
                            colorscale=[
                                [0/73, WHITE], # base
                                [1/73, GREEN], 
                                [2/73, PURPLE], 
                                [3/73, GOLD],
                                [10/73, WHITE], # 11 oscars
                                [11/73, GREEN], 
                                [12/73, PURPLE], 
                                [13/73, GOLD],
                                [20/73, WHITE], # 7 GG
                                [21/73, GREEN], 
                                [22/73, PURPLE], 
                                [23/73, GOLD],
                                [30/73, WHITE], # 2013
                                [31/73, GREEN], 
                                [32/73, PURPLE], 
                                [33/73, GOLD],
                                [40/73, WHITE], # 1957
                                [41/73, GREEN], 
                                [42/73, PURPLE], 
                                [43/73, GOLD],
                                [50/73, WHITE], # 1945
                                [51/73, GREEN], 
                                [52/73, PURPLE], 
                                [53/73, GOLD],
                                [60/73, WHITE], # 1948
                                [61/73, GREEN], 
                                [62/73, PURPLE], 
                                [63/73, GOLD],
                                [70/73, WHITE], #1983
                                [71/73, GREEN],
                                [72/73, PURPLE],
                                [73/73, GOLD]
                                ], 
                            showscale=False, 
                            zmin= 0,
                            hovertext= data['hover'],
                            hoverinfo="text",
                            hoverongaps=False))
    
    year_range = range(int(min(data['year_ceremony'])), int(max(data['year_ceremony'])) + 1)
    year_labels = [['' for col in range(column_width + 1)] for year in year_range]
    for i in range(len(year_range)):
        year_labels[i][column_width // 2] = str(year_range[i])

    year_labels = [item for row in year_labels for item in row]
    year_mapping = {i: year_labels[i] for i in range(max(data['X']) + 1)}
    year_labels[:-1]
    fig.update_layout(
        dragmode=False,
        xaxis=dict(tickmode='array',
                   tickvals=data['X'],
                   ticktext=[year_mapping[x] for x in data['X']]),
        yaxis = dict(showticklabels=False,),
    )

    fig['layout'].update(plot_bgcolor='white')


    # fig.update_coloraxes(colorbar=dict(len=0))

    # Add hovertemplate
    # fig.update_traces(
    #     hovertemplate = hover_template.get_heatmap_hover_template()
    # )
    return fig

def add_lines(data, figure):
    data = data[data['color'] != 0]
    shapes = []
    for x in tqdm(range(max(data['X']) + 1)):
        for y in range(max(data['Y'])):
            data_reference = data[(data['X'] == x) & (data['Y'] == y)]
            if len(data_reference) == 0:
                continue
            data_reference = data_reference.iloc[0]
            data_X1 = data[(data['X'] == x + 1) & (data['Y'] == y)]
            data_Y1 = data[(data['X'] == x) & (data['Y'] == y + 1)]
            if len(data_X1) > 0:
                data_X1 = data_X1.iloc[0]
                same = data_X1['tmdb_id'] == data_reference['tmdb_id']
                color = 'white' if same else 'black'
                width = 0.3 if same else 0.7
                shapes.append(go.layout.Shape(
                    type='line',
                    x0=x + 0.5,
                    x1=x + 0.5,
                    y0 = y - 0.5,
                    y1 = y + 0.5,
                    line = dict(color=color, width = width),
                    xref='x',
                    yref='y'
                ))
            if len(data_Y1) > 0:
                data_Y1 = data_Y1.iloc[0]
                same = data_Y1['tmdb_id'] == data_reference['tmdb_id']
                color = 'white' if same else 'black'
                width = 1 if same else 3
                shapes.append(go.layout.Shape(
                    type='line',
                    x0=x - 0.5,
                    x1=x + 0.5,
                    y0 = y + 0.5,
                    y1 = y + 0.5,
                    line = dict(color=color, width = width),
                    xref='x',
                    yref='y'
                ))
    figure.update_layout(shapes = shapes)
    return figure