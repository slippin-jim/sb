#!/Users/jim/anaconda3/envs/sb/bin/python

import pandas as pd
import baseball_scraper.baseball_reference as bsr
from helpers import get_teams, load_stats, create_sim
import time
import os
from datetime import datetime as dt
import logging

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir,'logs')
    working_path = os.path.join(base_dir,'data')

    logging.basicConfig(filename=f"{log_path}/nightly_wrapper.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    s = bsr.TeamScraper()

    load_results = load_stats.scrape_results(s)
    if load_results == 'completed':
        logging.debug('finished scraping, beginning predictions')
        create_sim.generate_predictions()


if __name__ == '__main__':
    main()