'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

CATEGORY_GLOBES_TO_OSCAR = {
    'ACTRESS IN A SUPPORTING ROLE': 'ACTRESS IN A SUPPORTING ROLE',
    'ACTOR IN A SUPPORTING ROLE': 'ACTOR IN A SUPPORTING ROLE',
    'DIRECTING': 'BEST DIRECTOR',
    'BEST PICTURE (DRAMA)': 'BEST PICTURE',
    'ACTRESS (DRAMA)': 'ACTRESS',
    'ACTOR (DRAMA)': 'ACTOR',
    'BEST SCORE': 'BEST SCORE',
    'CINEMATOGRAPHY': 'CINEMATOGRAPHY',
    'FOREIGN': 'FOREIGN FILM',
    'ACTOR (COM)': 'ACTOR',
    'ACTRESS (COM)': 'ACTRESS',
    'BEST PICTURE (COM)': 'BEST PICTURE',
    'BEST PICTURE (ANIMATED)': 'ANIMATED FEATURE FILM',
    'BEST SONG': 'BEST SONG'
}



def prepare_data(oscar, globe):
    '''

    '''

    oscar = oscar[~(oscar['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)
    globe = globe[~(globe['category'] == "SPECIAL AWARD")].drop("Unnamed: 0", axis = 1)

    oscar = oscar[oscar['winner']].drop(['year_film', 'ceremony', 'winner'], axis = 1)
    oscar['ceremony'] = 'oscars'
    oscar['common'] = ''
    oscar = oscar.reset_index()

    globe = globe[globe['win']].drop(["year_film", 'ceremony', 'win'], axis = 1).rename({'year_award':'year_ceremony', 'nominee': 'name'}, axis = 1)
    globe['ceremony'] = 'globes'
    globe['common'] = ''
    globe = globe.reset_index()
    
    return oscar, globe

def combine_awards(oscar, globe):
    for i, row in globe.iterrows():
        id = row['tmdb_id']
        matching_oscar = oscar[oscar['tmdb_id'] == id]
        matching_oscar = matching_oscar[matching_oscar['year_ceremony'] == row['year_ceremony']]
        screenplay_flag = False
        if row['category'] == 'BEST SCREENPLAY':
            matching_oscar_orig = matching_oscar[matching_oscar['category'] == 'ORIGINAL SCREENPLAY']
            matching_oscar_adap = matching_oscar[matching_oscar['category'] == 'ADAPTED SCREENPLAY']
            matching_oscar = pd.concat([matching_oscar_orig, matching_oscar_adap])
            screenplay_flag = True
        else:
            matching_oscar = matching_oscar[matching_oscar['category'] == CATEGORY_GLOBES_TO_OSCAR[row['category']]]
        if len(matching_oscar) > 0:
            common_category = 'BEST SCREENPLAY' if screenplay_flag else CATEGORY_GLOBES_TO_OSCAR[row["category"]]
            oscar.loc[matching_oscar.index, 'ceremony'] = 'BOTH'
            oscar.loc[matching_oscar.index, 'common'] = common_category
            globe.loc[i, 'ceremony'] = 'BOTH'
            globe.loc[i, 'common'] = common_category
    all_award = pd.concat([oscar, globe])
    all_award = all_award.sort_values(['year_ceremony', 'tmdb_id']).reset_index().drop(['level_0', 'index'], axis = 1)
    return all_award


class Ranker:
  def __init__(self):
    self.year = 0
    self.rank = 0
    self.n_award = 50
    self.tmdb_id = 0

  def ranks(self, tmdb_id, year, n_award):
    if tmdb_id == self.tmdb_id:
      return self.rank
    if year > self.year:
      self.year = year
      self.rank = 0
    elif year < self.year or self.n_award < n_award:
      print(tmdb_id, year, n_award)
      print(self.year, self.rank, self.n_award, self.tmdb_id)
      raise ValueError
    self.tmdb_id = tmdb_id
    self.n_award = n_award
    self.rank += 1
    return self.rank
  
def ranking(all_award):
    ranker = Ranker()
    all_award['#award'] = all_award.groupby(['year_ceremony', 'tmdb_id'])['common'].transform('count')
    all_award = all_award.sort_values(['year_ceremony', '#award', 'tmdb_id', 'ceremony'], ascending = [True, False, True, True])
    ranks = []
    for i, row in all_award.iterrows():
        ranks.append(ranker.ranks(row['tmdb_id'], row['year_ceremony'], row['#award']))
    all_award['rank'] = ranks

    return all_award

class Clusterer:
   def __init__(self, column_width = 3):
      self.column_left = - column_width - 1
      self.column_width = column_width
      self.year = 0
      self.current = -1
      self.year_to_X = dict()
    
   def cluster(self, year):
        if year == self.year:
            self.current += 1
        elif year > self.year:
            self.current = 0
            self.column_left += self.column_width + 1
            self.year = year
            self.year_to_X[year] = tuple(range(self.column_left, self.column_left + self.column_width))
        else:
           raise ValueError
        X = self.column_left + self.current % self.column_width
        Y = self.current // self.column_width
        if X == self.column_width:
           raise ValueError(self.current, self.column_width, X, self.column_left)
        return X, Y

def clustering(all_award, column_width = 3):
    all_award = all_award.drop(all_award[all_award['ceremony'] == 'BOTH'][['common', 'year_ceremony']].drop_duplicates().index)
    all_award = all_award.reset_index().drop('index', axis=1)

    clusterer = Clusterer(column_width)
    years = all_award['year_ceremony'].values.astype(float)
    clustered = [clusterer.cluster(year) for year in years]    
    X = [c[0] for c in clustered]
    Y = [c[1] for c in clustered]
    all_award['X'] = X
    all_award['Y'] = Y
    

    return all_award, clusterer.year_to_X

def colors(all_award):
   color_dict = {'BOTH': 1, 'oscars': 2, 'globes': 3, pd.NA: 0}
   all_award['color'] = all_award['ceremony'].apply(lambda ceremony: color_dict[ceremony])
   return all_award

def special_colors(all_award):
   all_award.loc[all_award['tmdb_id'] == 122., 'color'] += 10 # Lord of the Rings
   all_award.loc[all_award['tmdb_id'] == 665., 'color'] += 10 # ben Hur
   all_award.loc[all_award['tmdb_id'] == 597., 'color'] += 10 # Titanic

   all_award.loc[all_award['tmdb_id'] == 313369.0, 'color'] += 10 # La La Land
   
   all_award.loc[all_award['year_ceremony'] == 2013., 'color'] += 10 # 2013
   all_award.loc[all_award['year_ceremony'] == 1957., 'color'] += 10 # 1957
   all_award.loc[all_award['year_ceremony'] == 1945., 'color'] += 10 # 1945
   all_award.loc[all_award['year_ceremony'] == 1948., 'color'] += 10 # 1948
   all_award.loc[all_award['year_ceremony'] == 1983., 'color'] += 10 # 1948

   return all_award

def space_awards(all_award, column_width = 3):
   all_award = all_award[['tmdb_id', 'year_ceremony', 'ceremony', 'name', 'film', 'category', 'color', 'X', 'Y']]
   empty_columns = pd.DataFrame([{'ceremony': None, 'name': None, 'film': None, 'category': None, 'color': 0, 'X': x, 'Y': y} for x in range(column_width, max(all_award['X']), column_width + 1) for y in range(max(all_award['Y']) + 1)])
   all_award = pd.concat([all_award, empty_columns])
   all_award = all_award.sort_values('X')
   return all_award


def hover(row):
    if row['color'] == 0:
       return None
    ceremony = row['ceremony']
    if ceremony == 'BOTH':
        ceremony = 'OSCAR & GLOBES'
    else:
       ceremony = ceremony.upper()
    template = f"{ceremony} {int(row['year_ceremony'])} - {row['category']}<br>"
    template += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><i>{row['film']}</i></b>"
    return template

def add_hover(data):
    data['hover'] = [hover(row) for i, row in data.iterrows()]
    return data