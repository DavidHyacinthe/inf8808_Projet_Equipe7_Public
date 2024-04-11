import tools_viz6.preprocess as preproc
import tools_viz6.heatmap as heatmap
from tools_viz6.heatmap import WHITE, GREEN, PURPLE, GOLD, GREY 
import plotly.graph_objects as go
import copy

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import json

COLUMN_WIDTH = 1
year_to_x = None


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
    hovered_award = pd.read_feather("src/tools_viz6/data_vis6.feather")
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

def get_div_viz6(oscar_data, globe_data):
    figa, figb, fig = get_viz6(oscar_data, globe_data)
    config = dict(
                scrollZoom = False,
                showTips = False,
                showAxisDragHandles = False,
                doubleClick = False,
                displayModeBar = False)
    div = html.Div(
        className = 'vis6',
        children = [
            html.H3("Les deux récompenses au fil des années",
                    className = 'h-with-margins'),

            
            html.P("Dans cette dernière visualisation, nous explorons l'évolution des récompenses à travers les âges, nous permettant alors d'identifier les années durant lesquelles les deux cérémonies étaient en accord. Chaque case représente une récompense dans une catégorie.",
                    className = 'p-with-margins'),


            html.P("Les cases vertes représentent les catégories pour lesquelles les deux cérémonies ont été en accord lors d'une année précise. Par exemple, en 2017, les Oscars ainsi que les Golden Globes ont décidé de récompenser Damien Chazelle avec le prix du meilleur réalisateur de l'année pour le film LA LA LAND. L'intensité de la couleur d'une case est proportionelle au consensus entre les deux cérémonies.",
                    className = 'p-with-margins'),

            dcc.Graph(id="vis6a",
                          className= "waffle",
                          figure=figa,
                          config = config),

            html.P("Les cases violettes et jaunes représentent respectivement les récompenses données aux Oscars et aux Golden Globes, surlignant alors les différentes opinions des deux cérémonies.",
                    className = 'p-with-margins'),

            
            html.P("""Pour chaque année, la visualisation rassemble les films par blocs, séparés par des lignes noires. Les films les plus récompensées sont placés à la base des barres. Cela nous permet ainsi de repérer plusieurs films particulièrement bien récompensés:
                        Récompensé en 2017, La La Land est à ce jour le film ayant reçu le plus grand nombre de Golden Globes (7), dont 4 dans des catégories également récompensées par un Oscar.
                        Le nombre de récompenses données aux Golden Globes étant plus faible qu'aux Oscars, le record de La La Land ne lui permet alors d'égaler celui de Ben Hur, Titanic et Le Retour du Roi, récompensés d'11 Oscars en 1960, 1998 et 2004 respectivement.
                        À ce jour, il demeure le record d'Oscars et de récompenses reçus par un seul film.""",
                    className = 'p-with-margins'),

            dcc.Graph(id="vis6b",
                          className= "waffle",
                          figure=figb,
                          config = config),
            
            html.P("En 1945 et 1983, l’écart entre les deux cérémonies quant à leur choix de films récompensés fût le plus petit, étant réduit à un nombre record de 9 films différents. Cependant, il connut son apogée en 1957, creusant un clivage de 22 films entre les deux prix.",
                    className = 'p-with-margins'),

            html.P("Finalement cette visualisation nous permet de voir qu'en 2013, les deux cérémonies étaient en accord sur une grande majorité des catégories (10 récompenses communes), alors qu'en 1957 les deux cérémonies n'avaient seulement trouvé un terrain d'entente vis-à-vis de la récompense du meilleur film, déscernée au Tour du monde en 80 jours.",
                    className = 'p-with-margins'),

             html.P("C'est maintenant à vous d'explorer la visualisation ! Vous pouvez utiliser la barre glissante située en dessous de la figure pour limiter la visualisation à un nombre plus limité d'années.",
                    className = 'p-with-margins'),

            dcc.Graph(id="vis6",
                          className= "waffle",
                          figure=fig,
                          config = config),

            html.Div(className = "slide-container-vis6",
                     children = [
                        dcc.RangeSlider(
                                            id='vis6-rangeSlider',
                                            min=1944,
                                            max=2017,
                                            step=1,
                                            value=[1944, 2017],
                                            marks={year: str(year) for year in range(1945, 2020, 5)},  # Add marks every 5 years
                                        ),
                     ])
        ]
    )
    
    return div

def rangeslide_callback(value, fig):
    with open("tools_viz6/year_to_x", 'r') as file:
        year_to_x = json.loads(file.read())
    print(year_to_x)
    min_value, max_value = min(value), max(value)
    X_left = min(year_to_x[str(float(min_value))])
    X_right = max(year_to_x[str(float(max_value))])
    fig['layout']['xaxis']['range'] = [X_left - 1, X_right + 1]
    return fig
