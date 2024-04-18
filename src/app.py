import pandas as pd
import numpy as np
import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

import vis_1
import visualisation2
import visualisation5
import visualisation6
import dummy
import template
import vis_3

from visualisation_4_a import create_visualisation_4_a
from visualisation_4_b import create_visualisation_4_b

app = dash.Dash(__name__)
app.title = 'Projet Equipe 7 | INF8808'
server = app.server 

oscar = pd.read_csv("./assets/data/the_oscar_award_withID.csv")
globe = pd.read_csv("./assets/data/golden_globe_awards_withID.csv")
meta = pd.read_csv("./assets/data/awards_metadata.csv")

template.create_custom_theme()
template.set_default_theme()

#vis_1
vis1_df = pd.read_feather('./assets/data/vis1_df.feather')
vis1_df1 = pd.read_feather('./assets/data/vis1_df1.feather')
vis1_df2 = pd.read_feather('./assets/data/vis1_df2.feather')
list_cats = vis1_df.category.unique().tolist()
list_cats.sort()
list_cats.insert(0, 'All')

#vis_2
df_preprocessed_2 = pd.read_feather("./assets/data/df_preprocessed_2.feather")

#vis_3 
vis_3_df = pd.read_feather('./assets/data/vis_3_df.feather')
vis_3_df1 = pd.read_feather('./assets/data/vis_3_df1.feather')
vis3_list_cats = vis_3_df.category.unique().tolist()
vis3_list_cats.insert(0, 'All')

#vis_4
df_actors_vis_4 = pd.read_feather("./assets/data/vis_4_df_actors.feather")
df_actresses_vis_4 = pd.read_feather("./assets/data/vis_4_df_actresses.feather")
df_directors_vis_4 = pd.read_feather("./assets/data/vis_4_df_directors.feather")
df_female_directors_vis_4 = pd.read_feather("./assets/data/vis_4_df_female_directors.feather")
df_studio_vis_4 = pd.read_feather("./assets/data/vis_4_df_studio.feather")

#vis_5
vis_5_df = pd.read_feather("./assets/data/df_vis5.feather")

#Figures
fig1 = vis_1.vis1(vis1_df1, vis1_df2)

fig3 = vis_3.vis3(vis_3_df1)

fig4a = create_visualisation_4_a(df_actors_vis_4, df_actresses_vis_4, df_directors_vis_4, df_female_directors_vis_4)
fig4b = create_visualisation_4_b(df_studio_vis_4)

fig5 = go.Figure()
fig5 = visualisation5.heatmap_awards(fig= fig5, all_films= vis_5_df, annot= True, sep= True)

fig6a, fig6b, fig6 = visualisation6.get_viz6(oscar, globe)

# App Layout
app.layout = html.Div(
    className='content',
    children=[
        html.H1("Lumière sur l'excellence :"),
        html.H2("Une double analyse des lauréats des Oscars et Golden Globes"),
        html.Img(src="https://pngimg.com/d/academy_awards_PNG34.png",
                 id='oscar-img'),
        html.Img(src="https://www.pngall.com/wp-content/uploads/9/Grammy-Awards-Trophy-PNG-HD-Image.png",
                 id='globe-img'),


        html.Main(
            className= "all-viz-and-buttons-container",
            children= [ 
                html.P(["Les Oscars du Cinéma sont la récompense la plus prestigieuse dans le monde du cinéma. Décernés par l’",
                       html.I("Academy of Motion Pictures Arts and Science"),
                        " depuis 1929, ils récompensent l’excellence artistique et technique des films américains et étrangers. Depuis 1944, la cérémonie des Golden Globes remet, elle aussi, des distinctions dans le monde du cinéma, octroyées par l’",
                        html.I("Hollywood Foreign Press Association."),
                        html.Br(),
                        "Au cours de cet article, nous chercherons à explorer 73 ans de Cinéma pour mettre en évidence les différences et points communs entre les cérémonies."],
                       className = 'p-with-margins'),
                html.H3("Les Oscars et Golden Globes récompensent-ils les mêmes types de film ?",
                    className = 'h-with-margins'),
                html.P(["Les deux cérémonies varient dans les prix decernés. Par exemple, les Golden Globes ont tendance à discerner les films dramatiques et les comédies, engendrant alors la création de deux catégories différentes pour meilleur acteur ou meilleur film, parmi d'autres. " + \
                        "Malgré de telles disparités parmi les catégories, on retrouve souvent les mêmes genres et mots-clés parmi les films lauréats.",
                        html.Br(),
                        "Cependant, certaines différences sont indéniables, avec l'exemple du prix de la meilleure actrice. Aux Golden Globes, un mot-clé que l'on trouve " + \
                        "souvent au sein des films dramatiques lauréats est \"woman director\", créant un contraste avec les Oscars, où un mot-clé commun parmi les films lauréats du même prix est \"rape\". " + \
                        "Une telle différence mènerait une personne à se demander si les deux cérémonies cherchent réellement les mêmes critères en dépit d'un consensus vis-à-vis des récompenses dans leur ensemble, et si ces mots-clés sont des coïncidences ou représentent " + \
                        "la place de la femme au cœur de l'industrie cinématographique, si ce n'est dans ces cérémonies spécifiquement. " + \
                        "Nous vous invitons à explorer le graphique ci-dessous et de juger par vous-même en arrivant à votre propre conclusion.",
                       ],
                       className = 'p-with-margins'),
                html.Div(
                        className = 'viz-and-buttons-container',
                        children = [
                                    html.Div(
                                            className = 'viz-container',
                                            children = [
                                                    dcc.Graph(id = "vis1",
                                                              className = "figure",
                                                              figure = fig1,
                                                              config = dict(
                                                                      scrollZoom = False,
                                                                      showTips = False,
                                                                      showAxisDragHandles = False,
                                                                      doubleClick = False,
                                                                      displayModeBar = False)),
                                                    ]),
                                    html.Div(
                                            className = "radio-buttons-container-vis1",
                                            children = [
                                                    dcc.RadioItems(
                                                            id = 'vis1_sorting',
                                                            options = ['Oscars et Golden Globes', 'Oscars', 'Golden Globes'],
                                                            value = 'Oscars et Golden Globes',
                                                            labelStyle = {'whiteSpace': 'nowrap'}
                                                            
                                            ),
                                                    ],
                                            ),
                                    html.Div(
                                            className = "dropdown-container-vis1",
                                            children = [
                                                    dcc.Dropdown(
                                                    id = 'vis1_cats',
                                                    options = list_cats,
                                                    value = 'All'
                                             ),
                                                    ],
                        ),
                                    dcc.Store(id = 'dfs-store', data = {
                                                                        'df1': vis1_df1.to_json(), 
                                                                        'df2': vis1_df2.to_json()})
                        ]),
                
                
                html.H3("Récompenses, box-office, budget : existe-t-il un lien ?",
                    className = 'h-with-margins'),
                
                html.P("Titanic est l’un des films avec le plus gros budget, \
                       et il semble être un bon investissement : l’un des plus \
                       gros succès de tous les temps au box-office mondial et le \
                       film le plus récompensé de l’histoire des cérémonies. Mais \
                       est-il toujours nécessaire d’investir autant pour avoir un tel \
                       box-office et autant de récompenses ? A travers cette visualisation, \
                       nous vous invitons à explorer les liens entre le budget, le box-office \
                       et les récompenses, en tenant compte de l’inflation. Chaque bulle \
                       représente un film ; ainsi, en naviguant avec votre souris, vous \
                       pourrez découvrir différentes informations sur chaque film comme \
                       son nombre d’oscar, sa date de sortie… Cette visualisation vous \
                       permet aussi de voir facilement les films ayant remporté le plus \
                       d’oscars, de globes ou les deux grâce aux boutons situés à droite \
                       de l’image. Bon voyage à travers les récompenses !",
                       id = 'vis2-description',
                       className = 'p-with-margins'),
                
                html.Div(
                         className = 'viz-and-buttons-container',
                         children = [
                                     html.Div(
                                              className ='viz-container',
                                              children = [
                                                          dcc.Loading(dcc.Graph(id="vis2", 
                                                                                config = dict(scrollZoom = False,
                                                                                              showTips = False,
                                                                                              showAxisDragHandles = False,
                                                                                              doubleClick = False,
                                                                                              displayModeBar = False)),
                                                                                type = "cube")]),
                                     html.Div(
                                              className = 'radio-buttons-container',
                                              children = [
                                                          dcc.RadioItems(
                                                                         id='selection2',
                                                                         options=['Oscars et Golden Globes', 'Oscars', 'Golden Globes'],
                                                                         value='Oscars et Golden Globes',
                                                                         labelStyle = {'whiteSpace': 'nowrap'}
                                             )]),
                        ]),
                
                html.H3("Les récompenses dans le monde",
                                className = 'h-with-margins'),
                html.P("Dans cette nouvelle figure, vous pouvez découvrir quels \
                    pays reçoivent le plus de récompenses. \
                    Les Etats Unis d'Amérique reçoivent plus de 80% des prix, \
                    Vous pouvez choisir de les afficher ou non dans la figure.",
                    className = 'p-with-margins'),
                
                html.Div(
                        className = 'viz-and-buttons-container',
                        children = [
                                    html.Div(
                                            className = 'viz-container',
                                            children = [
                                                    dcc.Graph(id = "vis3",
                                                              className = "figure",
                                                              figure = fig3,
                                                              config = dict(
                                                                      scrollZoom = False,
                                                                      showTips = False,
                                                                      showAxisDragHandles = False,
                                                                      doubleClick = False,
                                                                      displayModeBar = False)
                                           )]),
                                    html.Div(
                                             className = "buttons-and-menus-container",
                                             children = [
                                                 html.Div(
                                                          className = "radio-buttons-container",
                                                          children = [
                                                              dcc.RadioItems(
                                                                  id = 'vis3_sorting',
                                                                  options = ['Oscar et Golden Globe', 'Oscar', 'Golden Globe'],
                                                                  value = 'Oscar et Golden Globe',
                                                                  labelStyle = {'whiteSpace': 'nowrap'}
                                                            
                                                 )]),
                                                 html.Div( 
                                                          className = "dropdown-container-vis3",
                                                          children = [
                                                              dcc.Dropdown(
                                                                  id = 'vis3_cats',
                                                                  options = vis3_list_cats,
                                                                  value = 'All'
                                                 )]),
                                                 html.Div(
                                                          className="radio-buttons-container-vis3-usa",
                                                          children=[
                                                              dcc.RadioItems(
                                                                  id='include_usa',
                                                                  options=[
                                                                      {'label': 'Exclude USA', 'value': 1},
                                                                      {'label': 'Include USA', 'value': 0}
                                                                      ],
                                                                  value=1,  # Default value to exclude USA
                                                                  labelStyle={'whiteSpace': 'nowrap'}
                                                  )]),
                                                 dcc.Store(id='intermediate-value')
                                    ]),
                        ]),
                
                html.H3("Qui gagne les récompenses ?",
                                className = 'h-with-margins'),
                
                html.P("Les figures suivantes montrent les récompenses obtenues par \
                    les personnalités les plus récompensées. \
                    Chaque case représente une récompense obtenue, \
                    la couleur correspond à la catégorie. \
                    Toutes les récompenses sont dans l'ordre chronologique.",
                    className = 'p-with-margins'),
                        
                html.P("Vous pouvez observer que les acteurs et actrices reçoivent\
                    beaucoup plus de Globes que d'Oscars, parce que les Globes de \
                    meilleur acting sont divisés en quatre sous catégories chaque année : \
                    Meilleure Actrice dans un Drame, Meilleur Acteur dans un Drame, \
                    Meilleure Actrice dans une Comédie, Meilleur Acteur dans une comédie.",
                        className = 'p-with-margins'),
                html.P("Vous pouvez aussi remarquer que les femmes reçoivent très peu \
                    souvent de prix pour la Meilleure Réalisation. \
                    Seulement deux femmes ont reçu ce prix dans l'histoire : \
                        Kathryn Bigelow et Barbra Streisand.",
                        className = 'p-with-margins'),
                
                dcc.Graph(id="vis4a",
                          className= "waffle",
                          config = dict(scrollZoom = False,
                                        showTips = False,
                                        showAxisDragHandles = False,
                                        doubleClick = False,
                                        displayModeBar = False),
                          figure=fig4a),
                
                html.P("Sur la figure suivante, vous pouvez observer les \
                    compagnies qui ont reçu le plus de récompenses.",
                        className = 'p-with-margins'),
                
                dcc.Graph(id="vis4b",
                          className= "waffle",
                          config = dict(scrollZoom = False,
                                        showTips = False,
                                        showAxisDragHandles = False,
                                        doubleClick = False,
                                        displayModeBar = False),
                          figure=fig4b),
                
                html.H3("Quelles sont les relations entre récompenses ?",
                    className = 'h-with-margins'),
                                
                html.P("La visualisation suivante permet d'identifier les récompenses \
                       qui sont souvent obtenues par un même film, ou à l'inverse  \
                           qui sont rarement obtenues par un même film.",
                           className = 'p-with-margins'),
                html.P("Par exemple, les récompenses Oscar du Meilleur Film et \
                    Oscar du Meilleur réalisateur sont souvent obtenues ensemble. \
                        A l'inverse, Les films qui remportent le Globe du Meilleur Film (Comedie) \
                            ne remportent que rarement l'Oscar du Meilleur scénario original.",
                            className = 'p-with-margins'),
                html.P("Les données affichées dans la figure sont des probabilités conditionnelles, \
                    c'est à dire la probabilité qu'un film obtienne une récompense sachant \
                        qu'il en a reçu une autre.",
                        className = 'p-with-margins'),
                
                dcc.Graph(id="vis5",
                          className= "heatmap",
                          figure=fig5),

                
                html.H3("Les deux récompenses au fil des années",
                        className = 'h-with-margins'),

                
                html.P("Dans cette dernière visualisation, nous explorons l'évolution des récompenses à travers les âges, nous permettant alors d'identifier les années durant lesquelles les deux cérémonies étaient en accord. Chaque case représente une récompense dans une catégorie.",
                        className = 'p-with-margins'),


                html.P("Les cases vertes représentent les catégories pour lesquelles les deux cérémonies ont été en accord lors d'une année précise. Par exemple, en 2017, les Oscars ainsi que les Golden Globes ont décidé de récompenser Damien Chazelle avec le prix du meilleur réalisateur de l'année pour le film LA LA LAND. Plus une colonne contient de vert, plus les deux cérémonies ont trouvé un consensus cette année.",
                        className = 'p-with-margins'),

                dcc.Graph(id="vis6a",
                            className= "waffle",
                            figure=fig6a,
                            config = visualisation6.config),

                html.P("Les cases violettes et jaunes représentent respectivement les récompenses données aux Oscars et aux Golden Globes, surlignant alors les différentes opinions des deux cérémonies.",
                        className = 'p-with-margins'),

                
                html.P("""Pour chaque année, la visualisation rassemble les films par blocs, séparés par des lignes noires. Les films les plus récompensées sont placés à la base des barres. Cela nous permet ainsi de repérer plusieurs films particulièrement bien récompensés:
                            Récompensé en 2017, La La Land est à ce jour le film ayant reçu le plus grand nombre de Golden Globes (7), dont 4 dans des catégories également récompensées par un Oscar.
                            Le nombre de récompenses données aux Golden Globes étant plus faible qu'aux Oscars, le record de La La Land ne lui permet alors d'égaler celui de Ben Hur, Titanic et Le Retour du Roi, récompensés d'11 Oscars en 1960, 1998 et 2004 respectivement.
                            À ce jour, il demeure le record d'Oscars et de récompenses reçus par un seul film.""",
                        className = 'p-with-margins'),

                dcc.Graph(id="vis6b",
                            className= "waffle",
                            figure=fig6b,
                            config = visualisation6.config),
                
                html.P("En 1945 et 1983, l’écart entre les deux cérémonies quant à leur choix de films récompensés fût le plus petit, étant réduit à un nombre record de 9 films différents. Cependant, il connut son apogée en 1957, creusant un clivage de 22 films entre les deux prix.",
                        className = 'p-with-margins'),

                html.P("Finalement cette visualisation nous permet de voir qu'en 2013, les deux cérémonies étaient en accord sur une grande majorité des catégories (10 récompenses communes), alors qu'en 1957 les deux cérémonies n'avaient seulement trouvé un terrain d'entente vis-à-vis de la récompense du meilleur film, décernée au Tour du monde en 80 jours.",
                        className = 'p-with-margins'),

                html.P("C'est maintenant à vous d'explorer la visualisation !",
                        className = 'p-with-margins'),

                dcc.Graph(id="vis6",
                            className= "waffle",
                            figure=fig6,
                            config = visualisation6.config),

                html.H3("Sources et Méthodologie",
                        className = 'h-with-margins'),

                html.P("Les données des récompenses présentées dans cet article sont tirées de bases de données mises à disposition sur Kaggle:",
                       className = 'p-with-margins'),

                html.Ul([
                    html.Li([
                        html.A("Ensemble de données sur les Oscars de 1927 à 2024", href = "https://www.kaggle.com/datasets/unanimad/the-oscar-award"),
                        " (depuis mis à jour pour intégrer les données les plus récentes)",
                    ]),
                    html.Li(html.A("Ensemble de données sur les Golden Globes de 1944 à 2020", href = "https://www.kaggle.com/datasets/unanimad/golden-globe-awards"))
                ],
                    className = 'p-with-margins'),

                html.P([
                    "Les informations complémentaires sur les films, tels que leur box office, genre ou mots clés, sont tirés de la base de données Publiques ",
                    html.A("The Movie Database", href = "https://www.themoviedb.org"),
                    "."
                    ],
                    className = 'p-with-margins'),

                html.P("Lors de la définition de notre sujet nous pensions utiliser un autre ensemble de données d'informations sur les films qui allait jusqu'à 2017. Cela nous a amené à fixer un cadre temporel pour les cérémonies de 1944 à 2017.",
                       className = 'p-with-margins'),

                html.P("Les noms des récompenses ayant pu évoluer au cours des années, nous avons adapté les anciennes récompenses pour coller aux récompenses données actuellement et avoir ainsi un cadre commun pour l'ensemble des années.",
                       className = 'p-with-margins'),
                html.Div(children= [html.P("La La Land should have won best picture")], id="bottom")
            ]),
        
    ])
 


# Callback functions
@app.callback(
    [Output('vis1', 'figure'),
     Output('dfs-store', 'data')],
    [Input('vis1_sorting', 'value'),
     Input('vis1_cats', 'value')],
    [State('vis1', 'figure'),
     State('dfs-store', 'data')]
)
def update_vis1(sorting_option, cat_option, fig, stored_data):
    ctx = dash.callback_context
    
    if not ctx.triggered: raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input == 'vis1_cats':
        if cat_option is None: raise dash.exceptions.PreventUpdate
        fig, df1, df2 = vis_1.update_category(cat_option, fig, vis1_df)
    else:
        df1 = pd.read_json(stored_data.get('df1'))
        df2 = pd.read_json(stored_data.get('df2'))
    
    if sorting_option is None: raise dash.exceptions.PreventUpdate
    if sorting_option == "Oscars et Golden Globes":
        if triggered_input == 'vis1_cats':
            return [fig, {'df1': df1.to_json(), 'df2': df2.to_json()}]
        else: sorting_option = 'Total'
    fig = vis_1.update_sorting(sorting_option, fig, df1, df2)

    return [fig, {'df1': df1.to_json(), 'df2': df2.to_json()}]

@app.callback(
    Output("vis2", "figure"), 
    Input("selection2", "value")
)
def callback(selection):
    return(visualisation2.display_animated_graph(selection, df_preprocessed_2))

@app.callback(
    Output('intermediate-value', 'data'),
    [Input('vis3_sorting', 'value'),
     Input('vis3_cats', 'value'),
     Input('include_usa', 'value')]
)
def update_intermediate(sorting_option, cat_option, usa_option):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    if sorting_option == "Oscar et Golden Globe":
            sorting_option = 'Total'
    filtered_df = vis_3.update_dataframe(sorting_option,cat_option, vis_3_df, usa_option)
    return filtered_df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('vis3', 'figure'),
    Input('intermediate-value', 'data'),
    [State('vis3', 'figure'),]
)
def update_vis3(json_filtered_data, fig):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    dff = pd.read_json(json_filtered_data, orient='split')
    fig = vis_3.update_figure(fig,dff)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)