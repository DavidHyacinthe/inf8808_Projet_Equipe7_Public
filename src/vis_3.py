import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from plotly.subplots import make_subplots

def preprocess_vis3():
  gg_df = pd.read_csv('./assets/data/golden_globe_awards_withID.csv')
  osc_df = pd.read_csv('./assets/data/the_oscar_award_withID.csv')
  meta_df = pd.read_csv('./assets/data/awards_metadata.csv')

  #keeping only those who won, putting aside those who won atypical categories and removing them from main df
  gg_df.category = gg_df.category.str.title()
  gg_df = gg_df[(gg_df.win == True) & (gg_df.film.isnull() == False)].reset_index(drop = True)

  #same thing for oscars + setting column category to title case
  osc_df.category = osc_df.category.str.title()
  osc_df = osc_df[osc_df.winner == True & (osc_df.film.isnull() == False)].reset_index(drop = True)

  #removing first column, renaming columns of both dfs the same, setting both to same range for year
  gg_df = gg_df.iloc[:, 1:]
  gg_df = gg_df.rename(columns = {'year_award': 'year_ceremony'})
  osc_df = osc_df.iloc[:, 1:]
  osc_df = osc_df.rename(columns = {'winner': 'win', 'name': 'nominee'})

  #combine both award dfs, removing duplicates and random ; from titles, reformatting and renaming id col
  #   create two new boolean columns to state which df each row is from (keeping award col to aid in fig)
  osc_df['award'] = 'Oscar'
  gg_df['award'] = 'Golden Globe'
  awr_df = pd.concat([osc_df, gg_df]).sort_values(['year_ceremony', 'year_film'])
  awr_df.film = awr_df.film.replace(';', '')
  awr_df.tmdb_id = awr_df.tmdb_id.astype(int)
  awr_df = awr_df.rename(columns = {'tmdb_id': 'id'})
  awr_df.category.replace({'Directing': 'Best Director', 
                           'Foreign': 'Foreign Film', 
                           'Best Picture (Animated)': 'Animated Feature Film'}, 
                          inplace = True)
  awr_df['Golden Globe'] = awr_df.apply(lambda row: True if row.award == 'Golden Globe' else False, axis = 1)
  awr_df['Oscar'] = awr_df.apply(lambda row: True if row.award == 'Oscar' else False, axis = 1)

  #removing first column in meta_df, unifying movie names, reformatting genres
  meta_df = meta_df[['title', 'production_countries', 'id']] 
  meta_df.title.replace('So Proudly We Hail', 'So Proudly We Hail!', inplace = True)
  meta_df.production_countries = meta_df.production_countries.apply(lambda x: re.findall(r"\'name': '(.*?)'}", x))

  #merging awd_df with meta_df and key_df, keeping only relevant columns
  awr_df = awr_df.merge(meta_df[['production_countries', 'id']], on = 'id')
  
  return awr_df


#function that generates a df for plotting, with 1 as input for excluding USA, and anything else for including it
def make_plot_df(og_df, flag):
  plot_col = ['production_countries', 'Country']
  df = og_df.copy().explode(plot_col[0])
  if flag == 1:
    df = df[df['production_countries'] != 'United States of America']
  #keeping unique rows based on film, award, and column to be plotted
  #   keeping top 5 for total prizes for each element to be plotted, 
  #   and for prizes per award for each element to be plotted
  df = df[~df[['film', 'award', 'category', plot_col[0]]].duplicated()]
  df = df[[plot_col[0], 'Golden Globe', 'Oscar']].groupby(plot_col[0]).sum().reset_index()
  df.columns = [plot_col[1], 'Golden Globe', 'Oscar']
  df['Total'] = df['Golden Globe'] + df['Oscar']
  df = df.sort_values('Total', ascending = False).reset_index(drop = True)
  df['Golden Globe Percent'] = (df['Golden Globe'] * 100) / (len(og_df[og_df['award'] == 'Golden Globe']))
  df['Oscar Percent'] = df['Oscar'] * 100 / len(og_df[og_df['award'] == 'Oscar'])
  df['Total Percent'] = df['Total'] * 100 / len(og_df)
  
  return df

def vis3(plot_df:pd.DataFrame):

  fig = make_subplots(rows = 1, cols = 2, shared_yaxes = True, horizontal_spacing = 0.28)
  
  df = plot_df.copy().iloc[:5, :].sort_values('Total')
  osc_key_vals = df['Oscar Percent']
  gg_key_vals = df['Golden Globe Percent']
  y_vals = df.iloc[::-1, 0].to_list()
  fig.append_trace(go.Bar(x = osc_key_vals, y = y_vals, marker = {'color': '#AB00FF'},
                          orientation = 'h', name = "Oscars", base = 0, customdata = plot_df.iloc[:5, :]), 
                   1, 1)
  fig.append_trace(go.Bar(x = gg_key_vals, y = y_vals, marker = {'color': '#FFBB00'},
                          orientation = 'h', name = "Golden Globes", base = 0),
                  1, 2)
  
  fig.update_layout(
      title = {'text': "Les 5 pays étrangers ayant gagné le plus de prix",
              'x': 0.42,
              'xanchor': 'center'}
      )
  fig = add_annotations(fig, y_vals)
  
  return fig


#add annotation to plots, mostly reformatting text in x- and y-axes
def add_annotations(fig, y_vals):
  fig = go.Figure(fig)
  fig.update_layout(
      width = 850,
      height = 600,
      margin = {'l': 40,
                'r': 20,
                'b': 35,
                't': 85},
      xaxis = {'ticksuffix': '%',
               'autorange': 'reversed',
               'tickangle': 0},
      xaxis2 = {'ticksuffix': '%',
                'tickangle': 0},
      xaxis3 = {'ticksuffix': '%',
                'autorange': 'reversed',
                'tickangle': 0},
      xaxis4 = {'ticksuffix': '%',
                'tickangle': 0},
      yaxis = {'tickvals': [],
                'automargin': True},
      yaxis2 = {'tickvals': [],
                'automargin': True},
      yaxis3 = {'tickvals': [],
                'automargin': True},
      yaxis4 = {'tickvals': [],
                'automargin': True},
      legend = {'yanchor': 'middle',
                'y': 0.53},
      dragmode = False,
      annotations = [
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.18,
                      'y': 1.05,
                      'text': 'Oscars',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.82,
                      'y': 1.05,
                      'text': 'Golden Globes',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 4,
                      'text': y_vals[0],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 3,
                      'text': y_vals[1],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 2,
                      'text': y_vals[2],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 1,
                      'text': y_vals[3],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 0,
                      'text': y_vals[4],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },],
      )
  
  return fig

# Function to update the DataFrame based on the category or sorting criteria
def update_dataframe(sort_col, cat, initial_df, usa_option):
    if cat != 'All':
      df = initial_df.copy()[initial_df['category'] == cat]
    else:
      df = initial_df.copy()
    df = make_plot_df(df, usa_option)
    if sort_col == 'Total':
      df = df.sort_values(sort_col, ascending=False).reset_index(drop=True).iloc[:5, :]
    else:
      df = df.sort_values([sort_col, 'Total'], ascending=False).reset_index(drop=True).iloc[:5, :]

    return df.iloc[:5, :].fillna(0)

# Function to update the figure based on the data in the DataFrame
def update_figure(fig, plot_df):
    y_vals = plot_df.iloc[:, 0].to_list()
    plot_df = plot_df.iloc[::-1]

    awr_lst = ['Golden Globe Percent', 'Oscar Percent',]

    for i in range(2):
        col_name = awr_lst[(i + 1) % 2]
        fig['data'][i]['x'] = plot_df[col_name]
        fig['data'][i]['y'] = y_vals

    return add_annotations(fig, y_vals)