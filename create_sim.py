import pandas as pd
import numpy as np
from scipy import stats as sci
from helpers import get_teams
import os
import logging
from datetime import datetime as dt

def main(year='2023',league='mlb'):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(cur_dir,'logs')
    out_path = f'{cur_dir}/predictions/{year}_{league}_{dt.now().strftime("%Y-%m-%d")}_projections.csv'

    logging.basicConfig(filename=f"{log_path}/predictions.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.debug("teams = {year} league = {league}".format(year=year,league=league))
    teams = get_teams.get_team_names(league)
    historicals_path = os.path.join(cur_dir,'data')
    csv_path = f'{historicals_path}/{year}_{league}_results.csv'
    team_results = pd.read_csv(csv_path)
    logger.debug("read from {csv_path}".format(csv_path=csv_path))
    teams = team_results.Tm.unique()

    teams_df = team_results.groupby('Tm')[['R','RA']].agg(avg_runs=('R','mean'),avg_runs_allowed=('RA','mean'),stdev_runs=('R','std'))
    teams_df.reset_index(inplace=True)
    teams_ct = teams_df.merge(teams_df,how='cross',suffixes=('_tm','_opp'))
    teams_ct.rename(columns={'Tm_tm':'Tm','Tm_opp':'Opp'},inplace=True)
    teams_gp = teams_ct.groupby(['Tm','Opp']).max()
    teams_gp.reset_index(inplace=True)
    teams_gp['adj_runs_tm'] = np.sqrt(teams_gp.avg_runs_tm*teams_gp.avg_runs_allowed_opp)

    def rand_results(rand=None,avg_runs=None,stdev_runs=None):
        return max(round(sci.norm.ppf(rand, loc=avg_runs, scale=stdev_runs),2),0)

    def sim_results(n=5,avg_runs=None,stdev_runs=None):
        empty_arr = np.random.random(size=n).tolist()
        rand_ = np.vectorize(rand_results)
        results = rand_(empty_arr,avg_runs,stdev_runs)
        return results

    teams_gp['sim_results'] = teams_gp.apply(lambda x: sim_results(avg_runs=x.avg_runs_tm,stdev_runs=x.stdev_runs_tm),axis=1)

    def opposing_runs(team,opp):
        team_runs = teams_gp[(teams_gp.Tm == team) & (teams_gp.Opp == opp)]['sim_results'].values 
        opp_runs = teams_gp[(teams_gp.Tm == opp) & (teams_gp.Opp == team)]['sim_results'].values
        output = np.subtract(team_runs,opp_runs).ravel()
        return output

    teams_gp['sim_differential'] = teams_gp.apply(lambda x: opposing_runs(x.Tm, x.Opp), axis=1)

    def unravel(layer1):
        for a1 in layer1:
            return a1

    def win_loss(arr):
        return np.where(arr>0,1,0)

    def win_loss_ratio(arr):
        return np.sum(arr) / arr.shape[0]

    teams_gp['sim_differential'] = teams_gp.apply(lambda x: unravel(x.sim_differential), axis=1)
    teams_gp['win_loss'] = teams_gp.apply(lambda x: win_loss(x.sim_differential), axis=1)
    teams_gp['w_l_ratio'] = teams_gp.apply(lambda x: win_loss_ratio(x.win_loss), axis=1)
    teams_gp.to_csv(out_path)

if __name__ == '__main__':
    main(2023,'mlb')