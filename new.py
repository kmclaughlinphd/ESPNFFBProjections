#!/usr/bin/python

import sys, os
import numpy as np
import csv

sys.path.append('.')
from classes import *

# figures out which teams made the playoffs
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

# accumulates averages based on simulation -- prob should do this with a class method instead
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


# this will need to be modified based on playoff format. in my league
# it's w1 top 6 (2 byes), w2 top 4, and w3+w4 championship
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

  NSims = 1000  # i usually run 10k

  if len(sys.argv) <= 1:
    print 'usage: ' + str(sys.argv[0]) + ' input'
    raise Exception

  teams = createTeams(sys.argv[1])

  # need to find a way to automate this step
  for sim in xrange(NSims):
    # week 11
 #   faceoff(teams['Keith McLaughlin'], teams['Paul Hyden'])
 #   faceoff(teams['Devon Antczak'], teams['Vipon Kawpunna'])
 #   faceoff(teams['TJ Snell'], teams['Dean Kruse'])
 #   faceoff(teams['Blayne Lee'], teams['William DuBois'])
 #   faceoff(teams['hugo rodriguez'], teams['IAN LEE'])
 #   faceoff(teams['Jared Rivers'], teams['Kenny Halligan'])

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


