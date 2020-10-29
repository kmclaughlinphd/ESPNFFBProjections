import string

# for creating sortable standings for ensemble
class standing(object):

    def __init__(self, team, player, prob, avg_W, avg_pts):
        self.team = team
        self.player = player
        self.prob = prob
        self.avg_W = avg_W
        self.avg_pts = avg_pts

    # this is used to sort the output table -- you can customize this one
    def __lt__(self, other):
        return self.prob * 1e10 + self.avg_W * 1e5 + self.avg_pts < other.prob * 1e10 + other.avg_W * 1e5 + other.avg_pts


def get_standings(teams, nsims):
    standings = []
    for player in teams.keys():
        standings += [standing(teams[player], player, float(teams[player].in_playoffs) / float(nsims),
                               teams[player].avg_W, teams[player].avg_pts)]
    standings.sort()
    standings.reverse()

    return standings


# customize this to your needs
def make_output(standings, n_sims):
    output = ["#   Player                 Playoff% Bye%   Final4% Final2% Champ% AvgWins AvgPts"]
    for ii in range(len(standings)):
        player = filter(lambda x: x in set(string.printable), standings[ii].player)
        player_name = ''.join(list(filter(lambda x: x in set(string.printable), standings[ii].player)))
        output.append(str("%-3d %-24s %.3f  %.3f   %.3f   %.3f  %.3f    %.2f   %.0f" %
                          (ii + 1, player_name, standings[ii].prob, standings[ii].team.first_round_bye / float(n_sims),
                           standings[ii].team.final4 / float(n_sims), standings[ii].team.final2 / float(n_sims),
                           standings[ii].team.champ / float(n_sims), standings[ii].avg_W, standings[ii].avg_pts)))

    # print readable output
    print('')
    for line in output:
        print(' ' + line)
    print('')
    print('')
