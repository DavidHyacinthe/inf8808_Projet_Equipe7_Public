import pandas as pd

PATH_oscar = './src/assets/data/the_oscar_award_withID.csv'
PATH_golden = './src/assets/data/golden_globe_awards_withID.csv'
PATH_meta = './src/assets/data/awards_metadata.csv'


def preprocessing_visualisation4_oscar():
    df_oscar = pd.read_csv(PATH_oscar)
    # Create new dataframes with only columns year_film, year_ceremony, category, name, film, win
    df_oscar = df_oscar[df_oscar['winner'] == True]
    # On garde seulement les colonnes qui nous intéressent  : year_film, year_ceremony, category, name, film
    df_oscar = df_oscar[['year_film', 'year_ceremony', 'category', 'name', 'film']]
    
    return df_oscar

def preprocessing_visualisation4_golden():
    df_golden = pd.read_csv(PATH_golden)
    # On garde que les lignes où win = True
    df_golden = df_golden[df_golden['win'] == True]
    # On garde que les colonnes year_film, year_award, category, nominee, film
    df_golden = df_golden[['year_film', 'year_award', 'category', 'nominee', 'film']]
    # Remonne year_award en year_ceremony
    df_golden.rename(columns={'year_award': 'year_ceremony'}, inplace=True)
    # On renomme nominee en name
    df_golden.rename(columns={'nominee': 'name'}, inplace=True)
    
    return df_golden

def preprocessing_visualisation4_metadata():
    df_meta = pd.read_csv(PATH_meta)
    
    return df_meta

def preprocessing_visualisation4_actors(df_oscar, df_golden):
    # On crée un dataframe où category = "ACTOR" ou "ACTOR IN A SUPPORTING ROLE" 
    df_oscar_actors = df_oscar[(df_oscar['category'] == 'ACTOR') | (df_oscar['category'] == 'ACTOR IN A SUPPORTING ROLE')]
    #ajoute une colonne ceremony avec la valeur "Oscar"
    df_oscar_actors['ceremony'] = 'Oscar'

    # meme chose pour les golden globes avec "'ACTOR IN A SUPPORTING ROLE', 'ACTOR (DRAMA)', 'ACTOR (COM)"
    df_golden_actors = df_golden[(df_golden['category'] == 'ACTOR IN A SUPPORTING ROLE') | (df_golden['category'] == 'ACTOR (DRAMA)') | (df_golden['category'] == 'ACTOR (COM)')]

    # On fusionne dans df_golden_actors les categories 'ACTOR (DRAMA)' et 'ACTOR (COM)' en 'ACTOR'
    df_golden_actors['category'] = df_golden_actors['category'].replace('ACTOR (DRAMA)', 'ACTOR')
    df_golden_actors['category'] = df_golden_actors['category'].replace('ACTOR (COM)', 'ACTOR')
    #ajoute une colonne ceremony avec la valeur "Golden Globe"
    df_golden_actors['ceremony'] = 'Golden Globe'

    #Fusionne les deux dataframes en un seul
    df_actors = pd.concat([df_oscar_actors, df_golden_actors])
    #tri par nom
    df_actors = df_actors.sort_values(by='year_ceremony')
    
    return df_actors
    

def preprocessing_visualisation4_actresses(df_oscar, df_golden):
    # On crée un dataframe où category = "ACTRESS" ou "ACTRESS IN A SUPPORTING ROLE"
    df_oscar_actresses = df_oscar[(df_oscar['category'] == 'ACTRESS') | (df_oscar['category'] == 'ACTRESS IN A SUPPORTING ROLE')]
    df_oscar_actresses['ceremony'] = 'Oscar'
    
    # meme chose pour les golden globes avec "'ACTRESS IN A SUPPORTING ROLE', 'ACTRESS (DRAMA)', 'ACTRESS (COM)"
    df_golden_actresses = df_golden[(df_golden['category'] == 'ACTRESS IN A SUPPORTING ROLE') | (df_golden['category'] == 'ACTRESS (DRAMA)') | (df_golden['category'] == 'ACTRESS (COM)')]
    df_golden_actresses['category'] = df_golden_actresses['category'].replace('ACTRESS (DRAMA)', 'ACTRESS')
    df_golden_actresses['category'] = df_golden_actresses['category'].replace('ACTRESS (COM)', 'ACTRESS')
    df_golden_actresses['ceremony'] = 'Golden Globe'
    
    # Fusionne les deux dataframes en un seul
    df_actresses = pd.concat([df_oscar_actresses, df_golden_actresses])
    df_actresses = df_actresses.sort_values(by='year_ceremony')
    
    return df_actresses

def preprocessing_visualisation4_directors(df_oscar, df_golden):
    # On crée un dataframe où category = "BEST DIRECTOR"
    df_oscar_directors = df_oscar[df_oscar['category'] == 'BEST DIRECTOR']
    df_oscar_directors['ceremony'] = 'Oscar'
    # on retire la ligne pour la réalisatrice Kathryn Bigelow
    df_oscar_directors = df_oscar_directors[df_oscar_directors['name'] != 'Kathryn Bigelow']
    #renomme la colonne name en directing
    df_oscar_directors['category'] = 'DIRECTING'
    
    # meme chose pour les golden globes
    df_golden_directors = df_golden[df_golden['category'] == 'DIRECTING']
    df_golden_directors['ceremony'] = 'Golden Globe'
    #enlever nom Barbra Streisand
    df_golden_directors = df_golden_directors[df_golden_directors['name'] != 'Barbra Streisand']

    # Fusionne les deux dataframes en un seul
    df_directors = pd.concat([df_oscar_directors, df_golden_directors])
    df_directors = df_directors.sort_values(by='year_ceremony')
    
    return df_directors

def preprocessing_visualisation4_female_directors(df_oscar, df_golden):
    # On crée un dataframe avec seulement les lignes de Kathryn Bigelow et Barbra Streisand

    # On crée un dataframe où category = "BEST DIRECTOR"
    df_oscar_female_directors = df_oscar[df_oscar['category'] == 'BEST DIRECTOR']
    df_oscar_female_directors['ceremony'] = 'Oscar'
    # on ajoute
    df_oscar_female_directors = df_oscar_female_directors[df_oscar_female_directors['name'] == 'Kathryn Bigelow']
    #renomme la colonne name en directing
    df_oscar_female_directors['category'] = 'DIRECTING'

    # meme chose pour les golden globes
    df_golden_female_directors = df_golden[df_golden['category'] == 'DIRECTING']
    df_golden_female_directors['ceremony'] = 'Golden Globe'
    #enlever nom Barbra Streisand
    df_golden_female_directors = df_golden_female_directors[df_golden_female_directors['name'] == 'Barbra Streisand']

    # Fusionne les deux dataframes en un seul
    df_female_directors = pd.concat([df_oscar_female_directors, df_golden_female_directors])
    df_female_directors = df_female_directors.sort_values(by='year_ceremony')
    return df_female_directors

def preprocessing_visualisation4_studio(df_metadata, df_actors, df_actresses, df_directors, df_female_directors):
    df_studio = pd.concat([df_actors, df_actresses, df_directors, df_female_directors])
    # ajoute une colonne name minuscule
    df_studio['film_lower'] = df_studio['film'].str.lower()
    df_studio
    
    df_studio = pd.concat([df_actors, df_actresses, df_directors, df_female_directors])
    # ajoute une colonne name minuscule
    df_studio['film_lower'] = df_studio['film'].str.lower()

    df_metadata['film_lower'] = df_metadata['title'].str.lower()
    #ajoute la ligne production_companies à df_studio 
    df_studio = df_studio.merge(df_metadata[['film_lower', 'production_companies']], on='film_lower', how='left')
    # on ajoute une colonne prodution_companies_name et prodution_companies_logo_path
    df_studio['production_companies_name'] = df_studio['production_companies'].str.split(',').str[2].str.split('\'').str[3]
    df_studio['production_companies_logo_path'] = df_studio['production_companies'].str.split(',').str[1].str.split('\'').str[3]
    
    return df_studio


def preprocessing_visualisation_4():
    df_oscar = preprocessing_visualisation4_oscar()
    df_golden = preprocessing_visualisation4_golden()
    df_metadata = preprocessing_visualisation4_metadata()
    
    df_actors = preprocessing_visualisation4_actors(df_oscar, df_golden)
    df_actresses = preprocessing_visualisation4_actresses(df_oscar, df_golden)
    df_directors = preprocessing_visualisation4_directors(df_oscar, df_golden)
    df_female_directors = preprocessing_visualisation4_female_directors(df_oscar, df_golden)
    
    df_studio = preprocessing_visualisation4_studio(df_metadata, df_actors, df_actresses, df_directors, df_female_directors)
    
    return df_actors, df_actresses, df_directors, df_female_directors, df_studio
    
    