import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from plotly.subplots import make_subplots

import template


#######################################################
 ################### PREPROCESSING ###################
  ##################################################

def preprocess_vis1():
  # gg_df = pd.read_csv('.\\assets\\data\\golden_globe_awards_withID.csv')
  # osc_df = pd.read_csv('.\\assets\\data\\the_oscar_award_withID.csv')
  # meta_df = pd.read_csv('.\\assets\\data\\awards_metadata.csv')
  # key_df = pd.read_csv('.\\assets\\data\\awards_keywords.csv')
  gg_df = pd.read_csv('./assets/data/golden_globe_awards_withID.csv')
  osc_df = pd.read_csv('./assets/data/the_oscar_award_withID.csv')
  meta_df = pd.read_csv('./assets/data/awards_metadata.csv')
  key_df = pd.read_csv('./assets/data/awards_keywords.csv')

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
  osc_df['award'] = 'Oscars'
  gg_df['award'] = 'Golden Globes'
  awr_df = pd.concat([osc_df, gg_df]).sort_values(['year_ceremony', 'year_film'])
  awr_df.film = awr_df.film.replace(';', '')
  awr_df.tmdb_id = awr_df.tmdb_id.astype(int)
  awr_df = awr_df.rename(columns = {'tmdb_id': 'id'})
  awr_df.category.replace({'Directing': 'Best Director', 'Foreign': 'Foreign Film'}, inplace = True)
  awr_df['Golden Globes'] = awr_df.apply(lambda row: True if row.award == 'Golden Globes' else False, axis = 1)
  awr_df['Oscars'] = awr_df.apply(lambda row: True if row.award == 'Oscars' else False, axis = 1)

  #removing first column in key_df and reformatting keywords
  key_df = key_df.iloc[:, 1:]
  key_df.keywords = key_df.keywords.apply(lambda x: re.findall(r"\'name': '(.*?)'}", x))

  #removing first column in meta_df, unifying movie names, reformatting genres
  meta_df = meta_df[['title', 'genres', 'id']] 
  meta_df.title.replace('So Proudly We Hail', 'So Proudly We Hail!', inplace = True)
  meta_df.genres = meta_df.genres.apply(lambda x: re.findall(r"\'name': '(.*?)'}", x))

  #merging awd_df with meta_df and key_df, keeping only relevant columns
  awr_df = awr_df.merge(key_df[['keywords', 'id']], on = 'id')
  awr_df = awr_df.merge(meta_df[['genres', 'id']], on = 'id')
  
  return awr_df


#function that generates a df for plotting, with 1 as input for genres, and anything else for keywords
def make_plot_df(og_df, flag):
  if flag == 1: plot_col = ['genres', 'Genre']
  else: plot_col = ['keywords', 'Keyword']
  df = og_df.copy().explode(plot_col[0])
  #reformatting keywords
  if flag != 1:
    df[plot_col[0]] = df[plot_col[0]].str.title()
    df[plot_col[0]].replace('World War Ii', 'World War II', inplace = True)
  #keeping unique rows based on film, award, and column to be plotted
  #   keeping top 5 for total prizes for each element to be plotted, 
  #   and for prizes per award for each element to be plotted
  df = df[~df[['film', 'award', 'category', plot_col[0]]].duplicated()]
  df = df[[plot_col[0], 'Golden Globes', 'Oscars']].groupby(plot_col[0]).sum().reset_index()
  df.columns = [plot_col[1], 'Golden Globes', 'Oscars']
  df['Total'] = df['Golden Globes'] + df['Oscars']
  df = df.sort_values('Total', ascending = False).reset_index(drop = True)
  df['Golden Globes Percent'] = (df['Golden Globes'] * 100) / (len(og_df[og_df['award'] == 'Golden Globes']))
  df['Oscars Percent'] = df['Oscars'] * 100 / len(og_df[og_df['award'] == 'Oscars'])
  df['Total Percent'] = df['Total'] * 100 / len(og_df)
  
  return df


#######################################################
 ################### VISUALIZATION ###################
  ##################################################

def vis1(plot_df1, plot_df2):

  fig = make_subplots(rows = 2, cols = 2, shared_yaxes = True, horizontal_spacing = 0.22,
                      vertical_spacing = 0.2)
  
  df1 = plot_df1.copy().iloc[:5, :].sort_values('Total')
  osc_key_vals1 = df1['Oscars']
  osc_key_perc1 = df1['Oscars Percent']
  gg_key_vals1 = df1['Golden Globes']
  gg_key_perc1 = df1['Golden Globes Percent']
  y_vals1 = df1.iloc[::-1, 0]
  fig.append_trace(go.Bar(x = osc_key_perc1, y = y_vals1, marker = {'color': template.COLORS['oscar_base']},
                          orientation = 'h', name = "Oscars", base = 0, customdata = osc_key_vals1,
                          hovertemplate = get_vis1_hover_template()), 
                   1, 1)
  fig.append_trace(go.Bar(x = gg_key_perc1, y = y_vals1, marker = {'color': template.COLORS['globe_base']},
                          orientation = 'h', name = "Golden Globes", base = 0, customdata = gg_key_vals1,
                          hovertemplate = get_vis1_hover_template()), 
                  1, 2)
  
  df2 = plot_df2.iloc[:5, :].sort_values('Total')
  osc_key_vals2 = df2['Oscars']
  osc_key_perc2 = df2['Oscars Percent']
  gg_key_vals2 = df2['Golden Globes']
  gg_key_perc2 = df2['Golden Globes Percent']
  y_vals2 = df2.iloc[::-1, 0].to_list()
  fig.append_trace(go.Bar(x = osc_key_perc2, y = y_vals2, marker = {'color': template.COLORS['oscar_base']},
                          orientation = 'h', name = "Oscars", base = 0, customdata = osc_key_vals2,
                          hovertemplate = get_vis1_hover_template()), 
                  2, 1)
  fig.append_trace(go.Bar(x = gg_key_perc2, y = y_vals2, marker = {'color': template.COLORS['globe_base']},
                          orientation = 'h', name = "Golden Globes", base = 0, customdata = gg_key_vals2,
                          hovertemplate = get_vis1_hover_template()), 
                  2, 2)
  
  fig.update_layout(
      title = {'text': "Les 5 genres ayant gagné le plus de prix",
               'x': 0.5,
               'xanchor': 'center'}
      )
  fig = add_annotations(fig, y_vals1, y_vals2)
  
  return fig

def get_vis1_hover_template():
  indent = "&nbsp;"
    
  return f"<b style='font-family: Roboto Slab; color: black;'>" + indent + \
                  "<span style='font-family: Roboto; font-weight: normal;'>%{x:.0f}%</span>" + indent + "<br>"\
                    + indent + "<span style='font-family: Roboto; font-weight: normal;'>%{customdata}</span>" + indent\
                        + '<extra></extra>'


#add annotation to plots, mostly reformatting text in x- and y-axes
def add_annotations(fig, y_vals1, y_vals2):
  fig = go.Figure(fig)
  fig.update_layout(
      width = 850,
      height = 1200,
      margin = {'l': 30,
                'r': 30,
                'b': 35,
                't': 85},
      xaxis = {'ticksuffix': '%',
               'autorange': 'reversed',
               'rangemode': 'nonnegative',
               'tickangle': 0},
      xaxis2 = {'ticksuffix': '%',
                'rangemode': 'nonnegative',
                'tickangle': 0},
      xaxis3 = {'ticksuffix': '%',
                'autorange': 'reversed',
                'rangemode': 'nonnegative',
                'tickangle': 0},
      xaxis4 = {'ticksuffix': '%',
                'rangemode': 'nonnegative',
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
                'y': 0.52,
                'xanchor': 'center',
                'x': 0.385},
                        # }]),
      annotations = [{'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.5,
                      'y': 0.445,
                      'text': "Les 5 mots clés ayant gagné le plus de prix",
                      'font_size': 17,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.195,
                      'y': 1.027,
                      'text': 'Oscars',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.805,
                      'y': 1.027,
                      'text': 'Golden Globes',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.195,
                      'y': 0.415,
                      'text': 'Oscars',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     
                     {'xref': 'paper',
                      'yref': 'paper',
                      'x': 0.805,
                      'y': 0.415,
                      'text': 'Golden Globes',
                      'font_size': 14,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 4,
                      'text': y_vals1[0],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 3,
                      'text': y_vals1[1],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 2,
                      'text': y_vals1[2],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 1,
                      'text': y_vals1[3],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y1',
                      'x': 0.5,
                      'y': 0,
                      'text': y_vals1[4],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                    
                     {'xref': 'paper',
                      'yref': 'y3',
                      'x': 0.5,
                      'y': 4,
                      'text': y_vals2[0],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y3',
                      'x': 0.5,
                      'y': 3,
                      'text': y_vals2[1],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y3',
                      'x': 0.5,
                      'y': 2,
                      'text': y_vals2[2],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                     {'xref': 'paper',
                      'yref': 'y3',
                      'x': 0.5,
                      'y': 1,
                      'text': y_vals2[3],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     },
                      {'xref': 'paper',
                      'yref': 'y3',
                      'x': 0.5,
                      'y': 0,
                      'text': y_vals2[4],
                      'font_size': 13,
                      'showarrow': False,
                      'xanchor': 'center',
                     }],
      )
  
  return fig


#function that updates the content of the plots according to the radio button the user pressed
def update_sorting(sort_col, fig, plot_df1, plot_df2):
  if sort_col == 'Total':
    df1 = plot_df1.copy().sort_values(sort_col, ascending = False).reset_index(drop = True).iloc[:5, :]
    df2 = plot_df2.copy().sort_values(sort_col, ascending = False).reset_index(drop = True).iloc[:5, :]
  else:
    df1 = plot_df1.copy().sort_values([sort_col, 'Total'], ascending = False).reset_index(drop = True).iloc[:5, :]
    df2 = plot_df2.copy().sort_values([sort_col, 'Total'], ascending = False).reset_index(drop = True).iloc[:5, :]
  
  y_vals1 = df1.iloc[:, 0].to_list()
  y_vals2 = df2.iloc[:, 0].to_list()
  df1 = df1.iloc[::-1]
  df2 = df2.iloc[::-1]
  
  awr_lst = ['Golden Globes', 'Oscars']
  
  for i in range(4):
    col_name = awr_lst[(i + 1) % 2]
    if i < 2:
      fig['data'][i]['x'] = df1[col_name + ' Percent']
      fig['data'][i]['y'] = y_vals1
      fig['data'][i]['customdata'] = df1[col_name]
    else:
      fig['data'][i]['x'] = df2[col_name + ' Percent']
      fig['data'][i]['y'] = y_vals2
      fig['data'][i]['customdata'] = df2[col_name]
  
  fig = add_annotations(fig, y_vals1, y_vals2)
  
  return fig

#function that updates which category the visualization is limited to
def update_category(cat, fig, og_df):
  if cat != 'All':
    df = og_df.copy()[og_df['category'] == cat]
  else:
    df = og_df.copy()
  plot_df1 = make_plot_df(df, 1).iloc[:5, :].fillna(0)
  plot_df2 = make_plot_df(df, 2).iloc[:5, :].fillna(0)
  
  y_vals1 = plot_df1.iloc[::-1, 0].to_list()
  y_vals2 = plot_df2.iloc[::-1, 0].to_list()
 
  awr_lst = ['Golden Globes Percent', 'Oscars Percent',]  
  
  for i in range(4):
    col_name = awr_lst[(i + 1) % 2]
    if i < 2:
      fig['data'][i]['x'] = plot_df1.sort_values(col_name)[col_name]
      fig['data'][i]['y'] = y_vals1
    else:
      fig['data'][i]['x'] = plot_df2.sort_values(col_name)[col_name]
      fig['data'][i]['y'] = y_vals2
  
  fig = add_annotations(fig, y_vals1, y_vals2)
  
  return fig