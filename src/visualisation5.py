import pandas as pd
import numpy as np
import plotly.graph_objects as go


def preprocessing_vis5(oscar, globe) :
  oscar = oscar[~(oscar['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)
  globe = globe[~(globe['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)

  # Award names
  oscar["category"] = oscar["category"].apply(lambda x : "OSCAR "+ x)
  globe["category"] = globe["category"].apply(lambda x : "GLOBE "+ x)

  # Select only winners, only the interesting columns
  oscar = oscar[oscar['winner']].drop(['year_film', 'year_ceremony', 'ceremony', 'name', 'winner'], axis = 1)
  oscar['ceremony'] = 'oscars'
  oscar = oscar.reset_index()

  globe = globe[globe['win']].drop(["year_film", 'year_award', 'ceremony', 'nominee', 'win'], axis = 1).rename({'year_award':'year_ceremony'}, axis = 1)
  globe['ceremony'] = 'globes'
  globe = globe.reset_index()

  all_award = pd.concat([oscar, globe])
  all_award = all_award.sort_values(['tmdb_id']).reset_index().drop(['level_0', 'index'], axis = 1)

  all_films = all_award[["tmdb_id", "category"]].groupby("tmdb_id").agg(list)

  list_cat = list(all_award["category"].unique())

  for cat in list_cat :
    all_films[cat] = all_films["category"].apply(lambda x : cat in x)

  return all_films


def heatmap_awards(fig, all_films, annot= False, sep= False) :
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

  for i in range(n_cat) :
    for j in range(n_cat) :
      cat_i = best_cat[i]
      cat_j = best_cat[j]
      freq_i_j = (all_films[cat_i] == all_films[cat_j]).sum()
      freq_i_j = all_films[all_films[cat_i] == all_films[cat_j]][[cat_i]].sum()
      freq_i = all_films[cat_i].sum()
      proba_mat[i][j] = freq_i_j / freq_i

      # prompt: display a plotly heatmap

  # Anotations:
  text_mat = np.array([ ["000000" for j in range(proba_mat.shape[1])] for j in range(proba_mat.shape[0])])
  if annot :
    for i in range(text_mat.shape[0]) :
      for j in range(text_mat.shape[1]) :
        if proba_mat[i][j] < 0.05 :
          text_mat[i][j] = "Faible"
        elif 0.6 < proba_mat[i][j] < 1 :
          text_mat[i][j] = "Forte"
        else :
          text_mat[i][j] = ""
  else :
    text_mat[:,:] = ""

  # Separator
  if sep :
    best_cat_fr = np.insert(best_cat_fr, 5, "", axis=0)
    proba_mat = np.insert(proba_mat, 5, [0] * proba_mat.shape[0], axis=1)
    proba_mat = np.insert(proba_mat, 5, [0] * proba_mat.shape[1], axis=0)
    text_mat = np.insert(text_mat, 5, [""] * text_mat.shape[0], axis=1)
    text_mat = np.insert(text_mat, 5, [""] * text_mat.shape[1], axis=0)

  # Figure
  fig = go.Figure(data=go.Heatmap(
                    z=proba_mat,
                    x=best_cat_fr,
                    y=best_cat_fr,
                    text=  text_mat,
                    texttemplate="%{text}",
                    textfont={"size":15},
                    colorscale= "Greys"))


  fig.update_layout(
      title='Probabilité conditionnelle de remporter une récompense',
      xaxis_title='Categorie',
      yaxis_title='Categorie',
      width=1000, height=900
  )
  fig.update_traces(hovertemplate="Probabilité qu'un film obtienne la récompense <br><b>%{x}</b> sachant qu'il a obtenu <br><b>%{y}</b> : %{z:.2f}")


  return fig



