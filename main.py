#!/usr/bin/python

import sys, os
from sims import *
from import_webdriver import *
from standings import *

if __name__ == '__main__':

    n_sims = 10000  # i usually run 10k

    if len(sys.argv) <= 1:
        print('usage: ' + str(sys.argv[0]) + ' LeagueID(int)')
        raise Exception

    # grab league data
    PAST, FUTURE = import_league_data(sys.argv[1])

    # create team profiles from the past data
    teams = create_teams(PAST)

    # run the simulation
    for ii in range(n_sims):
        run_sim(ii, teams, FUTURE)

    # sims are done, let's get playoff odds
    standings = get_standings(teams, n_sims)

    # generate output
    make_output(standings, n_sims)
