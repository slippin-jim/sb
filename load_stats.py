#!/Users/jim/anaconda3/envs/sb/bin/python

import pandas as pd
import numpy as np
import baseball_scraper.baseball_reference as bsr
from helpers import get_teams
import time
import os

def main():
    teams = get_teams.get_team_names('mlb')

    s = bsr.TeamScraper()
    s.set_season(2023)
    i = 0
    for x in teams:
        if i == 0:
            results = s.scrape(x)
        elif i > 0 and i % 4 != 0:
            new = s.scrape(x)
            results = pd.concat([results,new],ignore_index=True)
            i+=1
        else:
            time.sleep(7*60)
            results = pd.concat([results,new],ignore_index=True)
            i+=1

    path = os.path.join(os.curdir,'data')
    results.to_csv(f'{path}mlb_stats.csv')