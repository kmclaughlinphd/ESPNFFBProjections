#!/usr/bin/python

# MY_LEAGUE = 1179383
# TJ_WORK = 74946947
# TJ_SKUNKS = 239259

import sys, os
from sims import *
from import_webdriver import *
from standings import *

if __name__ == '__main__':

    n_sims = 10000  # i usually run 10k
    LEAGUE_ID = 74946947
    TWO_WEEK_FINALS = False
    ADD_SWISS_ROUND = False

    # if len(sys.argv) <= 1:
    #     print('usage: ' + str(sys.argv[0]) + ' LeagueID(int)')
    #     raise Exception

    # grab league data
    PAST, FUTURE = import_league_data(LEAGUE_ID)

    # create team profiles from the past data
    teams = create_teams(PAST)

    # run the simulation
    for ii in range(n_sims):
        run_sim(ii, teams, FUTURE, ADD_SWISS_ROUND, TWO_WEEK_FINALS)

    # sims are done, let's get playoff odds
    standings = get_standings(teams, n_sims)

    # generate output
    make_output(standings, n_sims)
