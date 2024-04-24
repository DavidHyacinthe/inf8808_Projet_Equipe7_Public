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

def create_heatmap_list(df_studio):
    top_studios = df_studio['production_companies_name'].value_counts().head(5)

    hover_list = []
    
    #tri de df_studio par année de cérémonie
    df_studio = df_studio.sort_values(by='year_ceremony')
    # on crée une liste des studios les plus primés
    studios_list = list(top_studios.index)
    
    z_studio1 = np.zeros((5,20),dtype=int)

    studio1 = studios_list[0]
    hover1 = []

    df_studio1 = df_studio[df_studio['production_companies_name'] == studio1].sort_values(by='year_ceremony')

    column = 0
    line = 0
    hover_line = []
    for index, row in df_studio1.iterrows():
        z_studio1[line][column] = convert[row['ceremony']][row['category']]
        hover_line.append(f"<b>Année de la cérémonie : </b>{row['year_ceremony']}<br><b>Nom du film : </b>{row['film']}<br><b>Année de sortie : </b>{row['year_film']}")
        column += 1
        if column == 20:
            line += 1
            column = 0
            hover1.append(hover_line)
            hover_line = []
    if column < 20:
        hover1.append(hover_line)
        
    #Remplissage du reste du hover
    for missing_line in range(5-len(hover1)):
        hover1.append([])
    for hoverline in hover1:
        for missing_column in range(20-len(hoverline)):
            hoverline.append("")
           
    z_studio1 = z_studio1/n
            
    # Remplace tout les 0 par des None pour ne pas les afficher
    for i in range(len(z_studio1)):
        for j in range(len(z_studio1[i])):
            if z_studio1[i][j] == 0:
                z_studio1[i][j] = None



    # Inverse z_studio1 et hover1 pour que les films les plus récents soient en haut
    z_studio1 = z_studio1[::-1]
    hover1 = hover1[::-1]

    heatmap_studio_1 = go.Heatmap(
        y=[" ","  ",studio1,"   ","    "],
        z=z_studio1,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = hover1,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    hover_list.append(heatmap_studio_1)
    
    
    # on fait la même pour studio2
    studio2 = studios_list[1]
    hover2 = []

    z_studio2 = np.zeros((5,20),dtype=int)

    df_studio2 = df_studio[df_studio['production_companies_name'] == studio2].sort_values(by='year_ceremony')

    column = 0
    line = 0
    hover_line = []
    for index, row in df_studio2.iterrows():
        z_studio2[line][column] = convert[row['ceremony']][row['category']]
        hover_line.append(f"<b>Année de la cérémonie : </b>{row['year_ceremony']}<br><b>Nom du film : </b>{row['film']}<br><b>Année de sortie : </b>{row['year_film']}")
        column += 1
        if column == 20:
            line += 1
            column = 0
            hover2.append(hover_line)
            hover_line = []
    if column < 20:
        hover2.append(hover_line)
        
    #Remplissage du reste du hover
    for missing_line in range(5-len(hover2)):
        hover2.append([])
    for hoverline in hover2:
        for missing_column in range(20-len(hoverline)):
            hoverline.append("")
    
    z_studio2 = z_studio2/n
            
    # Remplace tout les 0 par des None pour ne pas les afficher
    for i in range(len(z_studio2)):
        for j in range(len(z_studio2[i])):
            if z_studio2[i][j] == 0:
                z_studio2[i][j] = None


    # Inverse z_studio2 et hover2 pour que les films les plus récents soient en haut
    z_studio2 = z_studio2[::-1]
    hover2 = hover2[::-1]

    heatmap_studio_2 = go.Heatmap(
        y=[" ","  ",studio2,"   ","    "],
        z=z_studio2,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = hover2,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    hover_list.append(heatmap_studio_2)
    
    
    # on fait la même pour studio3
    studio3 = studios_list[2]
    hover3 = []
    
    z_studio3 = np.zeros((5,20),dtype=int)
    
    df_studio3 = df_studio[df_studio['production_companies_name'] == studio3].sort_values(by='year_ceremony')
    
    column = 0
    line = 0
    hover_line = []
    
    for index, row in df_studio3.iterrows():
        z_studio3[line][column] = convert[row['ceremony']][row['category']]
        hover_line.append(f"<b>Année de la cérémonie : </b>{row['year_ceremony']}<br><b>Nom du film : </b>{row['film']}<br><b>Année de sortie : </b>{row['year_film']}")
        column += 1
        if column == 20:
            line += 1
            column = 0
            hover3.append(hover_line)
            hover_line = []
    if column < 20:
        hover3.append(hover_line)
        
    #Remplissage du reste du hover
    for missing_line in range(5-len(hover3)):
        hover3.append([])
    for hoverline in hover3:
        for missing_column in range(20-len(hoverline)):
            hoverline.append("")
    
    z_studio3 = z_studio3/n
    
    # Remplace tout les 0 par des None pour ne pas les afficher
    for i in range(len(z_studio3)):
        for j in range(len(z_studio3[i])):
            if z_studio3[i][j] == 0:
                z_studio3[i][j] = None
    
    # Inverse z_studio3 et hover3 pour que les films les plus récents soient en haut
    z_studio3 = z_studio3[::-1]
    hover3 = hover3[::-1]
    
    heatmap_studio_3 = go.Heatmap(
        y=[" ","  ",studio3,"   ","    "],
        z=z_studio3,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = hover3,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    hover_list.append(heatmap_studio_3)
    
    
    # on fait la même pour studio4
    studio4 = studios_list[3]
    hover4 = []
    
    z_studio4 = np.zeros((5,20),dtype=int)
    
    df_studio4 = df_studio[df_studio['production_companies_name'] == studio4].sort_values(by='year_ceremony')
    
    column = 0
    line = 0
    hover_line = []
    
    for index, row in df_studio4.iterrows():
        z_studio4[line][column] = convert[row['ceremony']][row['category']]
        hover_line.append(f"<b>Année de la cérémonie : </b>{row['year_ceremony']}<br><b>Nom du film : </b>{row['film']}<br><b>Année de sortie :</b>{row['year_film']}")
        column += 1
        if column == 20:
            line += 1
            column = 0
            hover4.append(hover_line)
            hover_line = []
    if column < 20:
        hover4.append(hover_line)
        
    #Remplissage du reste du hover
    for missing_line in range(5-len(hover4)):
        hover4.append([])
    for hoverline in hover4:
        for missing_column in range(20-len(hoverline)):
            hoverline.append("")
    
    z_studio4 = z_studio4/n        
    
    # Remplace tout les 0 par des None pour ne pas les afficher
    for i in range(len(z_studio4)):
        for j in range(len(z_studio4[i])):
            if z_studio4[i][j] == 0:
                z_studio4[i][j] = None
    
    # Inverse z_studio4 et hover4 pour que les films les plus récents soient en haut
    z_studio4 = z_studio4[::-1]
    hover4 = hover4[::-1]

    heatmap_studio_4 = go.Heatmap(
        y=[" ","  ",studio4,"   ","    "],
        z=z_studio4,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = hover4,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    hover_list.append(heatmap_studio_4)
    
    
    # on fait la même pour studio5
    studio5 = studios_list[4]
    hover5 = []
    
    z_studio5 = np.zeros((5,20),dtype=int)
    
    df_studio5 = df_studio[df_studio['production_companies_name'] == studio5].sort_values(by='year_ceremony')
    
    column = 0
    line = 0
    hover_line = []
    
    for index, row in df_studio5.iterrows():
        z_studio5[line][column] = convert[row['ceremony']][row['category']]
        hover_line.append(f"<b>Année de la cérémonie : </b>{row['year_ceremony']}<br><b>Nom du film : </b>{row['film']}<br><b>Année de sortie : </b>{row['year_film']}")
        column += 1
        if column == 20:
            line += 1
            column = 0
            hover5.append(hover_line)
            hover_line = []
    if column < 20:
        hover5.append(hover_line)
        
    #Remplissage du reste du hover
    for missing_line in range(5-len(hover5)):
        hover5.append([])
    for hoverline in hover5:
        for missing_column in range(20-len(hoverline)):
            hoverline.append("")
    
    z_studio5 = z_studio5/n
    
    # Remplace tout les 0 par des None pour ne pas les afficher
    for i in range(len(z_studio5)):
        for j in range(len(z_studio5[i])):
            if z_studio5[i][j] == 0:
                z_studio5[i][j] = None
    
    # Inverse z_studio5 et hover5 pour que les films les plus récents soient en haut
    z_studio5 = z_studio5[::-1]
    hover5 = hover5[::-1]
    
    heatmap_studio_5 = go.Heatmap(
        y=[" ","  ",studio5,"   ","    "],
        z=z_studio5,
        xgap=3, ygap=10,
        colorscale=colorscale,
        text = hover5,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate='%{text}<extra></extra>',
        hoverongaps=False
    )
    hover_list.append(heatmap_studio_5)
    
    return hover_list


def create_visualisation_4_b(df_studio):
    hover_list = create_heatmap_list(df_studio)
    
    fig_visualisation_4_b = make_subplots(rows=5, cols=1, 
                                      vertical_spacing = 0.05)
    
    for i in range(5):
        fig_visualisation_4_b.add_trace(hover_list[i], row=i+1, col=1)

    fig_visualisation_4_b.update_layout(height=1500, width=1000, #à ajuster en fonction des besoins
                    title_text="Studios ayant gagnés le plus de prix")

    # Légende
    categories = ['Oscar: Meilleur réalisation', 'Oscar: Meilleur acting', 'Oscar: Meilleur second rôle',
                'Golden Globe: Meilleur réalisation', 'Golden Globe: Meilleur acting', 'Golden Globe: Meilleur second rôle']
    colors = [COLORS['oscar_dark'], COLORS['oscar_base'], COLORS['oscar_light'], COLORS['globe_dark'], COLORS['globe_base'], COLORS['globe_light']]

    fig_visualisation_4_b.update_layout(xaxis=dict(zeroline=False, showgrid=False),
                        yaxis=dict(zeroline=False, showgrid=False))
    for cat, color in zip(categories, colors):
        fig_visualisation_4_b.add_trace(go.Scatter
                                (x=[None], y=[None], mode='markers',
                                    marker=dict(size=10, color=color, symbol='square'),
                                    legendgroup=cat, showlegend=True, name=cat))

    # Pour avoir la légende à droite
    # fig_visualisation_4_b.update_layout(
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
    fig_visualisation_4_b.update_layout(
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

    fig_visualisation_4_b.update_layout(
        legend=dict(
            y=-0.1, # à ajuster
            x=0.5, # pour centre la légende horizontalement
            xanchor='center'
        )
    )

    # Pour enlever la grille de tous les axes
    for i in range(1, 6): # Mise à jour pour 5 subplots
        fig_visualisation_4_b.update_layout(**{
            f'xaxis{i}': dict(zeroline=False, showgrid=False),
            f'yaxis{i}': dict(zeroline=False, showgrid=False),
        })
    
    
    return fig_visualisation_4_b
    