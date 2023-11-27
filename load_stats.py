#!/Users/jim/anaconda3/envs/sb/bin/python

import pandas as pd
import baseball_scraper.baseball_reference as bsr
from helpers import get_teams
import time
import os
from datetime import datetime as dt
import logging

def scrape_handler(logger,s,x):
    try:
        results = s.scrape(x)
        logger.debug('results from {team} scraped'.format(team=x))
    except ValueError as e:
        results = pd.DataFrame()
    return results

def main():
    base_dir = os.path.abspath(os.path.pardir)
    log_path = os.path.join(base_dir,'logs')
    working_path = os.path.join(base_dir,'data')

    logging.basicConfig(filename=f"{log_path}/get_stats.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    season_year = dt.now().year
    teams = get_teams.get_team_names('mlb')

    s = bsr.TeamScraper()
    s.set_season(season_year)
    i = 0
    for x in teams:
        if i == 0:
            results = scrape_handler(logger,s,x)
            i+=1
        elif i > 0 and i % 4 != 0:
            new = scrape_handler(logger,s,x)
            results = pd.concat([results,new],ignore_index=True)
            i+=1
        else:
            time.sleep(2*60)
            new = scrape_handler(logger,s,x)
            results = pd.concat([results,new],ignore_index=True)
            i+=1

    results.to_csv(f'{working_path}/{season_year}_mlb_results.csv',index=False)
    logger.debug('csv results written to {working_path}/{season_year}_mlb_results.csv'.format(working_path=working_path,season_year=season_year))
    return "completed"

if __name__ == '__main__':
    main()