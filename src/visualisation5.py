import pandas as pd
import numpy as np
import plotly.graph_objects as go


def preprocessing_vis5(oscar, globe) :
  """Process data from scarped tmdb databases

  Args:
      oscar (DataFrame): Dataframe of the Oscar Ceremony
      globe (DataFrame): Dataframe of the Golden Globes Ceremony

  Returns:
      all_films (DataFrame): Dataframe with a column for every major award
  """
  oscar = oscar[~(oscar['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)
  globe = globe[~(globe['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)

  # Award names
  oscar["category"] = oscar["category"].apply(lambda x : "OSCAR "+ x)
  globe["category"] = globe["category"].apply(lambda x : "GLOBE "+ x)

  # Select winners only, interesting columns only
  oscar = oscar[oscar['winner']].drop(['year_film', 'year_ceremony', 'ceremony', 'name', 'winner'], axis = 1)
  oscar['ceremony'] = 'oscars'
  oscar = oscar.reset_index()

  globe = globe[globe['win']].drop(["year_film", 'year_award', 'ceremony', 'nominee', 'win'], axis = 1).rename({'year_award':'year_ceremony'}, axis = 1)
  globe['ceremony'] = 'globes'
  globe = globe.reset_index()

  all_award = pd.concat([oscar, globe])
  all_award = all_award.sort_values(['tmdb_id']).reset_index().drop(['level_0', 'index'], axis = 1)

  # Group by film
  all_films = all_award[["tmdb_id", "category"]].groupby("tmdb_id").agg(list)

  list_cat = list(all_award["category"].unique())

  # Create a colum for every award category
  for cat in list_cat :
    all_films[cat] = all_films["category"].apply(lambda x : cat in x)

  return all_films


def heatmap_awards(fig, all_films, annot= False, sep= False) :
  """_summary_

  Args:
      fig : Graph Object Figure
      all_films (DataFrame): Dataframe with a column for every major award
      annot (bool, optional): Toggle annotation ("Faible", "Forte"). Defaults to False.
      sep (bool, optional): Toggle separation between the 2 ceremonies. Defaults to False.

  Returns:
      fig : Graph Object Figure
  """
  best_cat = [ 'OSCAR BEST PICTURE',
  'OSCAR BEST DIRECTOR',
  'OSCAR ACTOR',
  'OSCAR ACTRESS',
  'OSCAR ORIGINAL SCREENPLAY',
  'GLOBE BEST PICTURE (COM)',
  'GLOBE BEST PICTURE (DRAMA)',
  'GLOBE ACTOR (COM)',
  'GLOBE ACTOR (DRAMA)',
  'GLOBE ACTRESS (COM)',
  'GLOBE ACTRESS (DRAMA)',
   'GLOBE BEST SCREENPLAY']

  best_cat_fr = [ 'OSCAR MEILLEUR FILM',
  'OSCAR MEILLEUR REALISATEUR',
  'OSCAR MEILLEUR ACTEUR',
  'OSCAR MEILLEURE ACTRICE',
  'OSCAR MEILLEUR SCENARIO ORIGINAL',
  'GLOBE MEILLEUR FILM (COMEDIE)',
  'GLOBE MEILLEUR FILM (DRAME)',
  'GLOBE MEILLEUR ACTEUR (COMEDIE)',
  'GLOBE MEILLEUR ACTEUR (DRAME)',
  'GLOBE MEILLEUR ACTRICE (COMEDIE)',
  'GLOBE MEILLEUR ACTRICE (DRAME)',
   'GLOBE MEILLEUR SCENARIO']

  n_cat = len(best_cat)
  proba_mat = np.zeros((n_cat, n_cat))

  # Get conditional probability
  for i in range(n_cat) :
    for j in range(n_cat) :
      cat_i = best_cat[i]
      cat_j = best_cat[j]
      freq_i_j = (all_films[cat_i] == all_films[cat_j]).sum()
      freq_i_j = all_films[all_films[cat_i] == all_films[cat_j]][[cat_i]].sum()
      freq_i = all_films[cat_i].sum()
      proba_mat[i][j] = int(freq_i_j / freq_i *100)

  # Hover and Anotations:     
  text_mat = []
  hover_mat = []
  for i in range(len(best_cat_fr)) :
    text_mat_i = []
    hover_mat_i = []
    for j in range(len(best_cat_fr)) :
      hover_mat_i.append(f"Probabilité qu'un film obtienne la récompense <br><b>{best_cat_fr[i]}</b> sachant qu'il a obtenu <br><b>{best_cat_fr[j]}</b> : {proba_mat[i][j]} % <extra></extra>")
      if annot :
        if proba_mat[i][j] < 5 :
          text_mat_i.append("Faible")
        elif 60 < proba_mat[i][j] < 100 :
          text_mat_i.append("Forte")
        else :
          text_mat_i.append("")
      else :
        text_mat_i.append("")
    text_mat.append(text_mat_i)
    hover_mat.append(hover_mat_i)
  
  text_mat = np.array(text_mat)
  hover_mat = np.array(hover_mat)
  

  # Create Separator
  if sep :
    best_cat_fr = np.insert(best_cat_fr, 5, "", axis=0)
    proba_mat = np.insert(proba_mat, 5, [None] * proba_mat.shape[0], axis=1)
    proba_mat = np.insert(proba_mat, 5, [None] * proba_mat.shape[1], axis=0)
    text_mat = np.insert(text_mat, 5, [""] * text_mat.shape[0], axis=1)
    text_mat = np.insert(text_mat, 5, [""] * text_mat.shape[1], axis=0)
    hover_mat = np.insert(hover_mat, 5, [""] * hover_mat.shape[0], axis=1)
    hover_mat = np.insert(hover_mat, 5, [""] * hover_mat.shape[1], axis=0)
    
    
  # Colorscale
  custom_colorscale = [
      [0.0,  '#2a2b2e'],
      [1.0,  '#FFFFFF']
  ]
  
  # Figure
  fig = go.Figure(data=go.Heatmap(
                    z=proba_mat,
                    x=best_cat_fr,
                    y=best_cat_fr,
                    text=  text_mat,
                    texttemplate="%{text}",
                    textfont={"size":15},
                    colorscale=custom_colorscale,
                    hovertext= hover_mat, 
                    hovertemplate='%{hovertext}<extra></extra>',
                    hoverongaps=False
                    ))

  # Titles
  fig.update_layout(
      title='Probabilité conditionnelle de remporter une récompense',
      xaxis=dict(title="Categorie", title_font=dict(size=18), tickfont=dict(size=15)),
      yaxis=dict(title="Categorie", title_font=dict(size=18), tickfont=dict(size=15)),
      title_font=dict(size=24),  
      width=1100, height=900
  )
  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=False)
  
  # Adding lines
  if sep :
    # Adding horizontal lanes :
    fig.add_shape(
      type='line',
      x0=-0.5, y0=5.5, x1=4.5, y1=5.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=-0.5, y0=4.5, x1=4.5, y1=4.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=5.5, y0=5.5, x1=12.5, y1=5.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=5.5, y0=4.5, x1=12.5, y1=4.5,
      line=dict(color='white', width=2)
    )

    
    # Adding vertical lanes : 
    fig.add_shape(
      type='line',
      x0=4.5, y0=-0.5, x1=4.5, y1=4.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=4.5, y0=5.5, x1=4.5, y1=12.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=5.5, y0=-0.5, x1=5.5, y1=4.5,
      line=dict(color='white', width=2)
    )
    fig.add_shape(
      type='line',
      x0=5.5, y0=5.5, x1=5.5, y1=12.5,
      line=dict(color='white  ', width=2)
    )

  return fig