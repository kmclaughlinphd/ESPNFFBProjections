#!/usr/bin/python

import sys, os
import numpy as np
import csv

class team(object):
  def __init__(self, teamName, W, score):
    self.teamName = teamName
    self.W = W
    self.scores = []
    self.scores.append(float(score))

    self.futW = 0
    self.futPts = 0

    self.avgW = 0
    self.avgPts = 0

    # regular season finishes
    self.inPlayoffs = 0
    self.firstRoundBye = 0

    # playoff finishes
    self.final4 = 0
    self.final2 = 0
    self.champ = 0


  def addGame(self, W, score):
    self.W += W
    self.scores.append(float(score))

##  def avg(self):
##    return np.mean(self.scores)
##
##  def std(self):
##    return np.std(self.scores)

  def ev(self):
    return np.mean(self.scores)

  def spread(self):
    return np.std(self.scores)


  def pts(self):
    return np.sum(self.scores)

  # get totals = base + future
  def totW(self):
    return self.W + self.futW

  def totPts(self):
    return self.pts() + self.futPts

  # reset future stats (simulated)
  def reset(self):
    self.futW = 0
    self.futPts = 0

  # get a random point total
  def playGame(self):
    if self.spread() == 0:
      print 'warning: received spread = 0. Using spread =', 23.50367
      return np.random.normal(self.ev(), 23.50367)
    return np.random.normal(self.ev(), self.spread())

  # add future results
  def addFutRes(self, W, pts):
    self.futW += W
    self.futPts += pts

  # playoff counter, used for MC simulation
  def IncrementPlayoffs(self):
    self.inPlayoffs += 1

  def IncrementBye(self):
    self.firstRoundBye += 1

  def addFinal4(self):
    self.final4 += 1

  def addFinal2(self):
    self.final2 += 1

  def addChamp(self):
    self.champ += 1

  # order methods (we don't deal with equality cuz it's pretty narrow
  def __lt__(self, other):
    return self.totW() * 1e5 + self.totPts() < other.totW() * 1e5 + other.totPts()


# for creating sortable standings for ensemble
class standing(object):

  def __init__(self, team, player, prob, avgW, avgPts):
    self.team = team
    self.player = player
    self.prob = prob
    self.avgW = avgW
    self.avgPts = avgPts

  def __lt__(self, other):
    return self.prob * 1e10 + self.avgW * 1e5 + self.avgPts < other.prob * 1e10 + other.avgW * 1e5 + other.avgPts


def checkPlayoffs(teams):
  teamsList = teams.values()
  teamsList.sort()
  teamsList.reverse()
  for i in xrange(0,6):
    teamsList[i].IncrementPlayoffs()
  for i in xrange(0,2):
    teamsList[i].IncrementBye()

  # return ranked teams
  return teamsList


def updateStats(teams, sim):
  n = float(sim)
  for team in teams.values():
    team.avgW = (1.0/(n+1.0)) * (team.avgW * sim + team.totW())
    team.avgPts = (1.0/(n+1.0)) * (team.avgPts * sim + team.totPts())

# create teams from input file
def createTeams(inputFile):

  teams = {}

  with open(inputFile, 'rb') as csvfile:
    readFile = csv.reader(csvfile)

    for readLine in readFile:
      # we make no attempt to validate the data
      if float(readLine[1]) > float(readLine[3]):
        result = [1,0] # win, loss
      elif float(readLine[1]) < float(readLine[3]):
        result = [0,1] # loss, win
      else:
        result = [0.5, 0.5] # tie

      # check if team 1 exists, init team or add game
      if readLine[0] in teams.keys():
        teams[readLine[0]].addGame(result[0], readLine[1])
      else:
        teams[readLine[0]] = team(readLine[0], result[0], readLine[1])

      if readLine[2] in teams.keys():
        teams[readLine[2]].addGame(result[1], readLine[3])
      else:
        teams[readLine[2]] = team(readLine[0], result[1], readLine[3])

  return teams

# simulate a game
def faceoff(team1, team2, playoffs=False, champs=False):
  score1 = team1.playGame()
  score2 = team2.playGame()
  
  # we play two weeks if this is the champs
  if champs:
    score1 += team1.playGame()
    score2 += team2.playGame()
  
  if (score1 > score2):
    res = [1,0]
    winner = team1
  else:
    res = [0,1]
    winner = team2

  # seems like this doesn't do anything important  :shrug:
  if not playoffs:
    team1.addFutRes(res[0],score1)
    team2.addFutRes(res[1],score2)

  return winner
  
  

def computePlayoffs(rankedTeams):

  #divisional

  winner1=faceoff(rankedTeams[2], rankedTeams[5], playoffs=True)
  winner2=faceoff(rankedTeams[3], rankedTeams[4], playoffs=True)

  rankedTeams[0].addFinal4()
  rankedTeams[1].addFinal4()
  winner1.addFinal4()
  winner2.addFinal4()


  # semis
  winner3=faceoff(winner2, rankedTeams[0], playoffs=True)
  winner4=faceoff(winner1, rankedTeams[1], playoffs=True)
  winner3.addFinal2()
  winner4.addFinal2()

  #finals
  champ = faceoff(winner3,winner4, playoffs=True, champs=True)
  champ.addChamp()

  return


if __name__ == '__main__':

  NSims = 1000

  if len(sys.argv) <= 1:
    print 'usage: ' + str(sys.argv[0]) + ' input'
    raise Exception

  teams = createTeams(sys.argv[1])

  for sim in xrange(NSims):
    # week 11
    faceoff(teams['Keith McLaughlin'], teams['Paul Hyden'])
    faceoff(teams['Devon Antczak'], teams['Vipon Kawpunna'])
    faceoff(teams['TJ Snell'], teams['Dean Kruse'])
    faceoff(teams['Blayne Lee'], teams['William DuBois'])
    faceoff(teams['hugo rodriguez'], teams['IAN LEE'])
    faceoff(teams['Jared Rivers'], teams['Kenny Halligan'])
    
    # week 12
    faceoff(teams['hugo rodriguez'], teams['Kenny Halligan'])
    faceoff(teams['Devon Antczak'], teams['Paul Hyden'])
    faceoff(teams['Dean Kruse'], teams['Blayne Lee'])
    faceoff(teams['Vipon Kawpunna'], teams['TJ Snell'])
    faceoff(teams['Keith McLaughlin'], teams['IAN LEE'])
    faceoff(teams['Jared Rivers'], teams['William DuBois'])

    # increment playoff counters
    rankedTeams = checkPlayoffs(teams)

    #update avgW and avgPts
    updateStats(teams, sim)

    # run playoff simulation
    computePlayoffs(rankedTeams)

    # reset future wins/pts
    for team in teams.values():
      team.reset()

  # sims are done, let's get playoff odds
  standings = []
  for player in teams.keys():
    standings += [standing(teams[player], player, float(teams[player].inPlayoffs) / float(NSims),
      teams[player].avgW, teams[player].avgPts)]
  standings.sort()
  standings.reverse()

  # generate output
  output = []
  output.append("#   Player          Playoff%   Bye% Final4% Final2% Champ% AvgWins  AvgPts")
  for ii in xrange(len(standings)):
    player = standings[ii].player
    output.append(str("%-3d %-18s %.3f  %.3f   %.3f   %.3f  %.3f    %.2f %.2f" % \
      (ii+1, player, standings[ii].prob, standings[ii].team.firstRoundBye/float(NSims),
      standings[ii].team.final4/float(NSims), standings[ii].team.final2/float(NSims),
      standings[ii].team.champ/float(NSims), standings[ii].avgW, standings[ii].avgPts)))

  #print readable output
  print ''
  for line in output:
    print ' ' + line
  print ''
  print ''
  

