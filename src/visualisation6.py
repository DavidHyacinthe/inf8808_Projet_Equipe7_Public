import tools_viz6.preprocess as preproc
import tools_viz6.heatmap as heatmap
import plotly.graph_objects as go
import copy

import dash
import dash_html_components as html
from dash import dcc
import pandas as pd
import json
from template import COLORS, THEME, create_custom_theme

COLUMN_WIDTH = 1
year_to_x = None

config = dict(
            scrollZoom = False,
            showTips = False,
            showAxisDragHandles = False,
            doubleClick = False,
            displayModeBar = False)

def hex_to_rgb(hexcode):
    # Remove '#' if it exists in the beginning of the hexcode
    if hexcode.startswith('#'):
        hexcode = hexcode[1:]

    # Convert hex to RGB
    r = int(hexcode[0:2], 16)
    g = int(hexcode[2:4], 16)
    b = int(hexcode[4:6], 16)

    return f'rgb({r},{g},{b})'

WHITE = hex_to_rgb(THEME['background_color'])
GREEN = hex_to_rgb(COLORS['both_base'])
PURPLE = hex_to_rgb(COLORS['oscar_base'])
GOLD = hex_to_rgb(COLORS['globe_base'])
GREY = hex_to_rgb(COLORS['unimportant'])



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
    create_custom_theme()
    fig = go.Figure()
    fig = heatmap.get_figure(hovered_award, COLUMN_WIDTH)
    fig = heatmap.add_lines(hovered_award, fig)
    fig.update_layout(template='custom_theme')
    fig.update_layout(
        dragmode=False,
        width=1300,
        height=650,
        xaxis=dict(zeroline=False, showgrid=False, linecolor = THEME['axis']), 
        yaxis=dict(zeroline=False, showgrid=False, showticklabels=False, showline=False, tickvals=[]),
    )
    figa = copy.deepcopy(fig) # GREEN ONLY
    figa.update_traces(colorscale=[
                                [0/13, WHITE], # base
                                [1/13, GREEN], 
                                [2/13, GREY], 
                                [3/13, GREY],
                                [10/13, WHITE], # 11 oscars
                                [11/13, GREEN], 
                                [12/13, GREY], 
                                [13/13, GREY],
                                ])
    
    figb = copy.deepcopy(fig) # MOVIES
    figb.update_traces(colorscale=[
                                [0/13, WHITE], # base
                                [1/13, GREY], 
                                [2/13, GREY], 
                                [3/13, GREY],
                                [10/13, WHITE], # 11 oscars
                                [11/13, GREEN], 
                                [12/13, PURPLE], 
                                [13/13, GOLD],
                                ])
    
    fig.update_traces(colorscale=[
                                [0/13, WHITE], # base
                                [1/13, GREEN], 
                                [2/13, PURPLE], 
                                [3/13, GOLD],
                                [10/13, WHITE], # 11 oscars
                                [11/13, GREEN], 
                                [12/13, PURPLE], 
                                [13/13, GOLD],
                                ])
    return figa, figb, fig


