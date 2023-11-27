import pandas as pd
import os

def get_team_names(sport:str):
    path = os.path.join(os.pardir,'static',sport.lower())
    df = pd.read_csv(f'{path}_teams.csv')
    return df.team_id.to_list()