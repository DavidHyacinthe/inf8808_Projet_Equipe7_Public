import tools_viz6.preprocess as preproc
import tools_viz6.heatmap as heatmap
from tools_viz6.heatmap import WHITE, GREEN, PURPLE, GOLD, GREY 
import plotly.graph_objects as go
import copy

import dash
import dash_html_components as html
from dash import dcc
import pandas as pd
import json

COLUMN_WIDTH = 1
year_to_x = None

config = dict(
            scrollZoom = False,
            showTips = False,
            showAxisDragHandles = False,
            doubleClick = False,
            displayModeBar = False)


def get_viz6(oscar_data, globe_data):
#     oscar_data, globe_data = preproc.prepare_data(oscar_data, globe_data)
#     all_award = preproc.combine_awards(oscar_data, globe_data)
#     ranked_award = preproc.ranking(all_award)
#     del all_award
#     clustered_award, year_to_x = preproc.clustering(ranked_award, COLUMN_WIDTH)
#     del ranked_award
#     colored_award = preproc.colors(clustered_award)
#     del clustered_award
#     special_award = preproc.special_colors(colored_award)
#     del colored_award
#     spaced_award = preproc.space_awards(special_award, COLUMN_WIDTH)
#     del special_award
#     hovered_award = preproc.add_hover(spaced_award)
#     del spaced_award
#     hovered_award = hovered_award.reset_index()
#     hovered_award = hovered_award.to_feather("tools_viz6/data_vis6.feather")
    hovered_award = pd.read_feather("tools_viz6/data_vis6.feather")
#     with open("tools_viz6/year_to_x", 'w') as file:
#         json.dump(year_to_x, file)

    fig = go.Figure()

    fig = heatmap.get_figure(hovered_award, COLUMN_WIDTH)
    fig = heatmap.add_lines(hovered_award, fig)
    fig.update_layout(
        width=1300,
        height=650
    )
    figa = copy.deepcopy(fig) # GREEN ONLY
    figa.update_traces(colorscale=[
                                [0/73, WHITE], # base
                                [1/73, GREEN], 
                                [2/73, GREY], 
                                [3/73, GREY],
                                [10/73, WHITE], # 11 oscars
                                [11/73, GREEN], 
                                [12/73, GREY], 
                                [13/73, GREY],
                                [20/73, WHITE], # 7 GG
                                [21/73, GREEN], 
                                [22/73, GREY], 
                                [23/73, GREY],
                                [30/73, WHITE], # 2013
                                [31/73, GREEN], 
                                [32/73, GREY], 
                                [33/73, GREY],
                                [40/73, WHITE], # 1957
                                [41/73, GREEN], 
                                [42/73, GREY], 
                                [43/73, GREY],
                                [50/73, WHITE], # 1945
                                [51/73, GREEN], 
                                [52/73, GREY], 
                                [53/73, GREY],
                                [60/73, WHITE], # 1948
                                [61/73, GREEN], 
                                [62/73, GREY], 
                                [63/73, GREY],
                                [70/73, WHITE], #1983
                                [71/73, GREEN],
                                [72/73, GREY],
                                [73/73, GREY]
                                ])
    
    figb = copy.deepcopy(fig) # MOVIES
    figb.update_traces(colorscale=[
                                [0/73, WHITE], # base
                                [1/73, GREY], 
                                [2/73, GREY], 
                                [3/73, GREY],
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
                                ])
    

    return figa, figb, fig


def rangeslide_callback(value, fig):
    with open("tools_viz6/year_to_x", 'r') as file:
        year_to_x = json.loads(file.read())
    print(year_to_x)
    min_value, max_value = min(value), max(value)
    X_left = min(year_to_x[str(float(min_value))])
    X_right = max(year_to_x[str(float(max_value))])
    fig['layout']['xaxis']['range'] = [X_left - 1, X_right + 1]
    return fig
