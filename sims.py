from teams import *
from collections import OrderedDict


# figures out which teams made the playoffs
def check_playoffs(teams):
    teams_list = list(teams.values())
    teams_list.sort()
    teams_list.reverse()
    for i in range(0, 6):
        teams_list[i].increment_playoffs()
    for i in range(0, 2):
        teams_list[i].increment_bye()

    # return ranked teams
    return teams_list


# pair 1v2, 3v4, etc.
def swiss_pairings(teams):
    teams_list = list(teams.values())
    teams_list.sort()
    teams_list.reverse()
    return [[teams_list[i], teams_list[i+1]] for i in range(0, 12, 2)]


# accumulates averages based on simulation -- prob should do this with a class method instead
def update_stats(teams, sim):
    n = float(sim)
    for team in teams.values():
        team.avg_W = (1.0 / (n + 1.0)) * (team.avg_W * sim + team.tot_W())
        team.avg_pts = (1.0 / (n + 1.0)) * (team.avg_pts * sim + team.tot_pts())


# create teams from input file
def create_teams(past_data):
    teams = OrderedDict()

    for matchup in past_data:
        team1 = matchup[0]
        team2 = matchup[1]
        score1 = float(matchup[2])
        score2 = float(matchup[3])

        if score1 > score2:
            result = [1, 0]  # win, loss
        elif score1 < score2:
            result = [0, 1]  # loss, win
        else:
            result = [0.5, 0.5]  # tie

        # check if team 1 exists, init team or add game
        if team1 in teams.keys():
            teams[team1].add_game(result[0], score1)
        else:
            teams[team1] = team(team1, result[0], score1)

        # same for team 2
        if team2 in teams.keys():
            teams[team2].add_game(result[1], score2)
        else:
            teams[team2] = team(team2, result[1], score2)

    return teams


# simulate a game
def faceoff(team1, team2, playoffs=False, champs=False):
    score1 = team1.play_game()
    score2 = team2.play_game()

    # we play two weeks if this is the champs
    if champs:
        score1 += team1.play_game()
        score2 += team2.play_game()

    if (score1 > score2):
        res = [1, 0]
        winner = team1
    else:
        res = [0, 1]
        winner = team2

    # seems like this doesn't do anything important  :shrug:
    if not playoffs:
        team1.add_fut_res(res[0], score1)
        team2.add_fut_res(res[1], score2)

    return winner


# this will need to be modified based on playoff format. in my league
# it's w1 top 6 (2 byes), w2 top 4, and w3+w4 championship
def compute_playoffs(ranked_teams):

    # divisional
    winner1 = faceoff(ranked_teams[2], ranked_teams[5], playoffs=True)
    winner2 = faceoff(ranked_teams[3], ranked_teams[4], playoffs=True)

    ranked_teams[0].add_final_4()
    ranked_teams[1].add_final_4()
    winner1.add_final_4()
    winner2.add_final_4()

    # ranked_teams[0].add_final_4()
    # ranked_teams[1].add_final_4()
    # ranked_teams[2].add_final_4()
    # ranked_teams[3].add_final_4()

    # semis
    winner3=faceoff(winner2, ranked_teams[0], playoffs=True)
    winner4=faceoff(winner1, ranked_teams[1], playoffs=True)
    # winner3 = faceoff(ranked_teams[0], ranked_teams[3])
    # winner4 = faceoff(ranked_teams[1], ranked_teams[2])
    winner3.add_final_2()
    winner4.add_final_2()

    # finals
    champ = faceoff(winner3, winner4, playoffs=True, champs=True)
    champ.add_champ()

    return


def run_sim(sim_ii, teams, future_matchups):

    # simulate each future matchup
    for matchup in future_matchups:
        faceoff(teams[matchup[0]], teams[matchup[1]])

    # simulate week 12 by swiss pairings (if nec)
    if len(list(teams.values())[0].scores) < 12:
        pairings = swiss_pairings(teams)
        for pp in pairings:
            faceoff(pp[0], pp[1])

    # increment playoff counters
    ranked_teams = check_playoffs(teams)

    # update avgW and avgPts
    update_stats(teams, sim_ii)

    # run playoff simulation
    compute_playoffs(ranked_teams)

    # reset future wins/pts
    for team in teams.values():
        team.reset()
