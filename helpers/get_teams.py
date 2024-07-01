import pandas as pd
import os

def get_team_names(sport:str):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    par_dir = os.path.dirname(cur_dir)
    path = os.path.join(par_dir,'static',sport.lower())
    df = pd.read_csv(f'{path}_teams.csv')
    return df.team_id.to_list()

if __name__ == '__main__':
    get_team_names('mlb')