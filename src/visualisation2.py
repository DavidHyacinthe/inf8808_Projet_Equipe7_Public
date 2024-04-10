'''
Preprocessing functions for the visualisation part
'''

import pandas as pd
import cpi
from template import COLORS, create_custom_theme

def transform_meta(df):
    """
    Transforms the metadata dataframe to a more readable format

    Args:
    df: dataframe to transform

    Returns:
    df_bis: transformed dataframe
    """
    df_bis = df[['title', 'release_date', 'budget', 'revenue']]
    df_bis['release_date'] = pd.to_datetime(df_bis['release_date']).dt.year
    df_bis = df_bis.rename(columns={'release_date': 'year', 'revenue' : 'box_office', 'title' : 'movie'})
    df_bis['box_office'] = df_bis.apply(lambda x: cpi.inflate(x['box_office'], x['year'], to=2016), axis=1)
    df_bis['budget'] = df_bis.apply(lambda x: cpi.inflate(x['budget'], x['year'], to=2016), axis=1)
    return df_bis


def tranform_globes(df):
    """
    Transforms the Golden Globes dataframe to a more readable format

    Args:
    df: dataframe to transform

    Returns:
    df_bis: transformed dataframe
    """
    df_bis = df[['year_film', 'film', 'win']]
    df_bis = df_bis[df_bis['win'] == True].groupby(['year_film','film']).count()
    df_bis = df_bis.reset_index()
    df_bis = df_bis.rename(columns={'year_film': 'year', 'film' : 'movie', 'win' : 'number_globes'})
    return df_bis


def tranform_oscars(df):
    """
    Transforms the Oscars dataframe to a more readable format

    Args:
    df: dataframe to transform

    Returns:
    df_bis: transformed dataframe
    """
    df_bis = df[['year_film', 'film', 'winner']]
    df_bis = df_bis[df_bis['winner'] == True].groupby(['year_film','film']).count()
    df_bis = df_bis.reset_index()
    df_bis = df_bis.rename(columns={'year_film': 'year', 'film' : 'movie', 'winner' : 'number_oscars'})
    return df_bis


def merge_data(df_meta, df_globes, df_oscars):
    """
    Merges the 3 dataframes

    Args:
    df_meta: metadata dataframe
    df_globes: Golden Globes dataframe
    df_oscars: Oscars dataframe

    Returns:
    df_merged: merged dataframe
    """
    df_merged = pd.merge(df_meta, df_globes, how='left', on=['year', 'movie'])
    df_merged = pd.merge(df_merged, df_oscars, how='left', on=['year', 'movie'])
    df_merged = df_merged.fillna(0)
    df_merged['number_globes'] = df_merged['number_globes'].astype(int)
    df_merged['number_oscars'] = df_merged['number_oscars'].astype(int)
    df_merged['total_awards'] = df_merged['number_globes'] + df_merged['number_oscars']
    df_merged = df_merged[df_merged['total_awards'] > 0]
    df_merged = df_merged[(df_merged['box_office'] != 0 ) & (df_merged['budget'] != 0)] # à voir
    df_merged = df_merged.reset_index(drop=True)
    df_merged['recompense_oscar'] = ['Oscars' if x > 0 else 'None' for x in df_merged['number_oscars']]
    df_merged['recompense_globes'] = ['Golden Globes' if x > 0 else 'None' for x in df_merged['number_globes']]
    df_merged['recompense'] = ['Oscars' if x > 0 and y == 0 else 'Golden Globes' if x == 0 and y > 0 else 'Both' for x, y in zip(df_merged['number_oscars'], df_merged['number_globes'])]
    df_merged['number_globes_exp'] = df_merged['number_globes'].apply(lambda x: x**2 if x > 0 else 0)
    df_merged['number_oscars_exp'] = df_merged['number_oscars'].apply(lambda x: x**2 if x > 0 else 0)
    df_merged['total_awards_exp'] = df_merged['total_awards'].apply(lambda x: x**2 if x > 0 else 0)
    df_merged = df_merged.sort_values(by='recompense')
    return df_merged



'''
    Provides the template for the tooltips.
'''

def get_bubble_hover_template():
    '''
        Generates the content of the tooltip for the bubble chart
        returns:
            The content of the tooltip
    '''
    # TODO : Generate tooltip

    heatmap_hover_template = (
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Movie : </b>%{customdata[0]}<br>' +
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Year : </b>%{customdata[1]}<br>' +
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Budget : </b>%{x} $ (USD)<br>' + 
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Box office: </b>%{y} $ (USD) <br>' + 
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Nombre oscars : </b>%{customdata[2]} <br>' + 
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Nombre globes: </b>%{customdata[3]} <br>' + 

            '<extra></extra>' # retirer le trace écrit par défaut
    )
    return heatmap_hover_template


'''
    Functions for the visualisation part
'''

import plotly.express as px

def update_title(fig):
    '''
        Updates the title of the figure

        Args:
            fig: The figure to update
            title: The new title
        Returns:
            The updated figure
    '''
    fig.update_layout(title_text='Budget vs Box office pour les films à récompenses')
    return fig


def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    #mise en place des titres pour les axes

    fig.update_layout(
        xaxis_title="Budget ($ USD)",
        yaxis_title="Box office ($ USD)",
    )
    return fig


def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    #ajout du titre pour la légende
    fig.update_layout(legend_title_text='Légende')
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'custom_theme'

        Args:
            fig: The figure to update
        Returns
            The updated figure
    '''
    #ajouter le bon template
    fig.update_layout(template='custom_theme')
    return fig


def display_animated_graph(selection, my_df_merged):
    """
        Displays the animated graph

        Args:
        selection: the selection
        df_meta: metadata dataframe
        df_globes: Golden Globes dataframe
        df_oscars: Oscars dataframe

        Returns:
        fig: the figure to display
    """
   
    create_custom_theme()

    animations = {
        'Oscars': px.scatter(
            my_df_merged, 
            x="budget", 
            y="box_office", 
            size="number_oscars_exp",
            color="recompense", 
            log_x=True, 
            log_y=True, 
            size_max = 50,
            hover_name = 'movie',
            custom_data = ['movie', 'year', 'number_oscars', 'number_globes'],
            color_discrete_sequence = [COLORS['both_base'], COLORS['globe_base'], COLORS['oscar_base']]),
        'Golden Globes': px.scatter(
            my_df_merged, 
            x="budget", 
            y="box_office", 
            size="number_globes_exp",
            color="recompense", 
            log_x=True, 
            log_y=True, 
            size_max = 50,
            hover_name = 'movie',
            custom_data = ['movie', 'year', 'number_oscars', 'number_globes'],
            color_discrete_sequence = [COLORS['both_base'], COLORS['globe_base'], COLORS['oscar_base']]),
        'Oscars et Golden Globes': px.scatter(
            my_df_merged, 
            x="budget", 
            y="box_office", 
            size="total_awards_exp",
            color="recompense", 
            log_x=True, 
            log_y=True, 
            size_max = 50,
            hover_name = 'movie',
            custom_data = ['movie', 'year', 'number_oscars', 'number_globes'],
            color_discrete_sequence = [COLORS['both_base'], COLORS['globe_base'], COLORS['oscar_base']]),
    }

    fig = animations[selection]

    fig.update_traces(marker=dict(sizemin=2))
    fig.update_traces(hovertemplate= get_bubble_hover_template())

    fig = update_title(fig)
    fig = update_axes_labels(fig)
    fig = update_template(fig)
    fig = update_legend(fig)
    fig = fig.update_layout(height=500, width=1000)


    return fig
