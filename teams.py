# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      keyth
#
# Created:     19/11/2018
# Copyright:   (c) keyth 2018
# Licence:     <your licence>
# ------------------------------------------------------------------------------

import numpy as np


# class for each team in the league
## it is assumed that the league only have 1 division with all the teams
## i can add multi division support maybe at a later time
class team(object):
    def __init__(self, team_name, W, score):
        self.team_name = team_name
        self.W = W

        # list of all scores from previous weeks for this team
        self.scores = []
        self.scores.append(float(score))

        # this will hold projected wins and PF
        self.fut_W = 0
        self.fut_pts = 0

        # this will accumulate averages (past + future)
        self.avg_W = 0
        self.avg_pts = 0

        # regular season finishes
        self.in_playoffs = 0
        self.first_round_bye = 0

        # playoff finishes
        self.final4 = 0
        self.final2 = 0
        self.champ = 0

    # add a game outcome (win vs loss, and PF)
    def add_game(self, W, score):
        self.W += W
        self.scores.append(float(score))

    # get average
    def ev(self):
        return np.mean(self.scores)

    # get stdev
    def spread(self):
        return np.std(self.scores)

    # get total PF (past games)
    def pts(self):
        return np.sum(self.scores)

    # get Wins, past + simulated
    def tot_W(self):
        return self.W + self.fut_W

    # get PF, past + simulated
    def tot_pts(self):
        return self.pts() + self.fut_pts

    # reset future stats -- prep for next simulation
    def reset(self):
        self.fut_W = 0
        self.fut_pts = 0

    # get a random point total
    def play_game(self):
        if self.spread() == 0:
            print('warning: received spread = 0. Using spread = %f' % 23.50367)
            return np.random.normal(self.ev(), 23.50367)
        return np.random.normal(self.ev(), self.spread())

    # add future results
    def add_fut_res(self, W, pts):
        self.fut_W += W
        self.fut_pts += pts

    # accumulate results from a simulation
    ## did we make playoffs?
    def increment_playoffs(self):
        self.in_playoffs += 1

    ## did we get a 1st round bye?
    def increment_bye(self):
        self.first_round_bye += 1

    ## did we make final 4?
    def add_final_4(self):
        self.final4 += 1

    ## did we make finals?
    def add_final_2(self):
        self.final2 += 1

    ## are we the champ?
    def add_champ(self):
        self.champ += 1

    # order methods (we don't deal with equality cuz it's pretty narrow
    ## this is used to sort for standings to determine playoff berths, etc.
    def __lt__(self, other):
        return self.tot_W() * 1e5 + self.tot_pts() < other.tot_W() * 1e5 + other.tot_pts()
