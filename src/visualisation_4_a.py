import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from template import COLORS, create_custom_theme

create_custom_theme()

n = 6 # nombre de prix
colorscale =    [[0, '#2a2b2e'], #Rien
                [1/n, COLORS['oscar_dark']], # Oscar meilleur réalisation
                [2/n, COLORS['oscar_base']], # Oscar meilleur acteur/actrice
                [3/n, COLORS['oscar_light']], # Oscar meilleur role secondaire
                [4/n, COLORS['globe_dark']], # Golden Globe meilleur réalisation
                [5/n, COLORS['globe_base']], # Golden Globe meilleur acteur/actrice
                [6/n, COLORS['globe_light']]] # Golden Globe meilleur role secondaire

convert = {'Oscar': {'DIRECTING': 1, 'ACTOR': 2, 'ACTOR IN A SUPPORTING ROLE': 3, 'ACTRESS': 2, 'ACTRESS IN A SUPPORTING ROLE': 3}, 'Golden Globe': {'DIRECTING': 4, 'ACTOR': 5, 'ACTOR IN A SUPPORTING ROLE': 6, 'ACTRESS': 5, 'ACTRESS IN A SUPPORTING ROLE': 6}}


def create_heatmap_actors(df_actors):
    top_actors = df_actors['name'].value_counts().head(5)
    
    actors_list = list(top_actors.index[:5])
    actors_list = actors_list[::-1]

    z_actors = np.zeros((5,10),dtype=int)
    z_actors_hover = []

    #Attribution de la couleur et du hover
    actor = 0
    for single_actor in actors_list:
        hover = []
        df_single_actor = df_actors[df_actors['name'] == single_actor].sort_values(by='year_ceremony')
        column = 0
        for index, row in df_single_actor.iterrows():
            z_actors[actor][column] = convert[row['ceremony']][row['category']]
            hover.append(f"Année de la cérémonie : {row['year_ceremony']}<br>Nom du film : {row['film']}<br>Année de sortie : {row['year_film']}")
            column += 1
        z_actors_hover.append(hover)
        actor += 1
    z_actors = z_actors/n

    #Remplissage du reste du hover
    for missing_line in range(5-len(actors_list)):
        z_actors_hover.append([])
    for hoverline in z_actors_hover:
        for missing_column in range(10-len(hoverline)):
            hoverline.append("")
            
    # Convertis tout les 0 de z_actors en None pour ne pas les afficher
    for i in range(len(z_actors)):
        for j in range(len(z_actors[i])):
            if z_actors[i][j] == 0:
                z_actors[i][j] = None

    heatmap_actor = go.Heatmap(
        y=actors_list, z=z_actors,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = z_actors_hover,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    
    return heatmap_actor

def create_heatmap_actresses(df_actresses):
    top_actresses = df_actresses['name'].value_counts().head(5)
    
    # On fait la même chose pour les actrices
    actresses_list = list(top_actresses.index)
    actresses_list = actresses_list[::-1]

    z_actresses = np.zeros((5,10),dtype=int)
    z_actresses_hover = []

    actress = 0
    for single_actress in actresses_list:
        hover = []
        df_single_actress = df_actresses[df_actresses['name'] == single_actress].sort_values(by='year_ceremony')
        column = 0
        for index, row in df_single_actress.iterrows():
            z_actresses[actress][column] = convert[row['ceremony']][row['category']]
            hover.append(f"Année de la cérémonie : {row['year_ceremony']}<br>Nom du film : {row['film']}<br>Année de sortie : {row['year_film']}")
            column += 1
        z_actresses_hover.append(hover)
        actress += 1
        
    z_actresses = z_actresses/n

    # Remplissage du reste du hover
    for missing_line in range(5-len(actresses_list)):
        z_actresses_hover.append([])
    for hoverline in z_actresses_hover:
        for missing_column in range(10-len(hoverline)):
            hoverline.append("")
            
    # Convertis tout les 0 de z_actresses en None pour ne pas les afficher
    for i in range(len(z_actresses)):
        for j in range(len(z_actresses[i])):
            if z_actresses[i][j] == 0:
                z_actresses[i][j] = None

    heatmap_actresses = go.Heatmap(
        y=actresses_list, z=z_actresses,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = z_actresses_hover,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )    

    return heatmap_actresses

def create_heatmap_directors(df_directors):
    top_directors = df_directors['name'].value_counts().head(5)
    
    # On fait la même chose pour les réalisateurs
    directors_list = list(top_directors.index)
    directors_list = directors_list[::-1]

    z_directors = np.zeros((5,10),dtype=int)
    z_directors_hover = []

    director = 0
    for single_director in directors_list:
        hover = []
        df_single_director = df_directors[df_directors['name'] == single_director].sort_values(by='year_ceremony')
        column = 0
        for index, row in df_single_director.iterrows():
            z_directors[director][column] = convert[row['ceremony']][row['category']]
            hover.append(f"Année de la cérémonie : {row['year_ceremony']}<br>Nom du film : {row['film']}<br>Année de sortie : {row['year_film']}")
            column += 1
        z_directors_hover.append(hover)
        director += 1

    z_directors = z_directors/n

    # Remplissage du reste du hover
    for missing_line in range(5-len(directors_list)):
        z_directors_hover.append([])
    for hoverline in z_directors_hover:
        for missing_column in range(10-len(hoverline)):
            hoverline.append("")
            
    # Convertis tout les 0 de z_directors en None pour ne pas les afficher
    for i in range(len(z_directors)):
        for j in range(len(z_directors[i])):
            if z_directors[i][j] == 0:
                z_directors[i][j] = None

    heatmap_director = go.Heatmap(
        y=directors_list, z=z_directors,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = z_directors_hover,
        showscale=False,
        zmax=1,
        zmin=0,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    
    return heatmap_director

def create_heatmap_female_directors(df_female_directors):
    top_female_directors = df_female_directors['name'].value_counts().head(5)
    
    # On fait la même chose pour les réalisatrices
    female_directors_list = list(top_female_directors.index)
    female_directors_list = female_directors_list[::-1]

    z_female_directors = np.zeros((5,10),dtype=int)
    z_female_directors_hover = []

    female_director = 0
    for single_female_director in female_directors_list:
        hover = []
        df_single_female_director = df_female_directors[df_female_directors['name'] == single_female_director]
        column = 0
        for index, row in df_single_female_director.iterrows():
            z_female_directors[female_director][column] = convert[row['ceremony']][row['category']]
            hover.append(f"Année de la cérémonie : {row['year_ceremony']}<br>Nom du film : {row['film']}<br>Année de sortie : {row['year_film']}")
            column += 1
        z_female_directors_hover.append(hover)
        female_director += 1
    z_female_directors = z_female_directors/n

    # Remplissage du reste du hover
    for missing_line in range(5-len(female_directors_list)):
        z_female_directors_hover.append([])
    for hoverline in z_female_directors_hover:
        for missing_column in range(10-len(hoverline)):
            hoverline.append("")
            
    # Convertis tout les 0 en None pour ne pas les afficher
    for i in range(len(z_female_directors)):
        for j in range(len(z_female_directors[i])):
            if z_female_directors[i][j] == 0:
                z_female_directors[i][j] = None

    # Remplissage du reste des noms
    female_directors_list.append(" ")
    female_directors_list.append("  ")
    female_directors_list.append("   ")

    # inversion des noms, des hover et des z
    z_female_directors = z_female_directors[::-1]
    z_female_directors_hover = z_female_directors_hover[::-1]
    female_directors_list = female_directors_list[::-1]

    heatmap_female_director = go.Heatmap(
        y=female_directors_list, z=z_female_directors,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = z_female_directors_hover,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )

    return heatmap_female_director

def create_visualisation_4_a(df_actors, df_actresses, df_directors, df_female_directors):
    heatmap_actors = create_heatmap_actors(df_actors)
    heatmap_actresses = create_heatmap_actresses(df_actresses)
    heatmap_directors = create_heatmap_directors(df_directors)
    heatmap_female_directors = create_heatmap_female_directors(df_female_directors)
    
    fig_visualisation_4_a = make_subplots(rows=4, cols=1, 
                                      subplot_titles=("Acteurs", "Actrices", "Réalisateurs", "Réalisatrices"),
                                      vertical_spacing = 0.05)

    fig_visualisation_4_a.add_trace(heatmap_actors, row=1, col=1)
    fig_visualisation_4_a.add_trace(heatmap_actresses, row=2, col=1)
    fig_visualisation_4_a.add_trace(heatmap_directors, row=3, col=1)
    fig_visualisation_4_a.add_trace(heatmap_female_directors, row=4, col=1)

    fig_visualisation_4_a.update_layout(height=1500, width=1000, #à ajuster en fonction des besoins
                    title_text="Personnes ayant gagnés le plus de prix")

    # Légende
    categories = ['Oscar: Meilleur réalisation', 'Oscar: Meilleur acting', 'Oscar: Meilleur second rôle',
                'Golden Globe: Meilleur réalisation', 'Golden Globe: Meilleur acting', 'Golden Globe: Meilleur second rôle']
    colors = [COLORS['oscar_dark'], COLORS['oscar_base'], COLORS['oscar_light'], COLORS['globe_dark'], COLORS['globe_base'], COLORS['globe_light']]

    fig_visualisation_4_a.update_layout(xaxis=dict(zeroline=False, showgrid=False),
                        yaxis=dict(zeroline=False, showgrid=False))
    for cat, color in zip(categories, colors):
        fig_visualisation_4_a.add_trace(go.Scatter
                                (x=[None], y=[None], mode='markers',
                                    marker=dict(size=10, color=color, symbol='square'),
                                    legendgroup=cat, showlegend=True, name=cat))

    # Pour avoir la légende à droite
    # fig_visualisation_4_a.update_layout(
    #     legend_title_text='Catégorie',
    #     legend=dict(
    #         orientation='v', # Utiliser l'orientation verticale
    #         xanchor='left',  # Ancrer la légende à gauche de la position x spécifiée
    #         x=1.05,          # Déplacer légèrement la légende à droite du graphique
    #         yanchor='middle',# Ancrer la légende au milieu de la position y spécifiée
    #         y=0.5            # Centrer la légende verticalement par rapport au graphique
    #     )
    # )

    # Pour avoir la légende en bas
    fig_visualisation_4_a.update_layout(
        legend_title_text='Catégorie',
        dragmode = False,
        legend=dict(
            traceorder='normal',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    fig_visualisation_4_a.update_layout(
        legend=dict(
            y=-0.1, # à ajuster
            x=0.5, # pour centre la légende horizontalement
            xanchor='center'
        )
    )
    
    for i in range(1, 5): # Mise à jour pour 4 subplots
        fig_visualisation_4_a.update_layout(**{
            f'xaxis{i}': dict(zeroline=False, showgrid=False),
            f'yaxis{i}': dict(zeroline=False, showgrid=False),
        })


    return fig_visualisation_4_a