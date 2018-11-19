#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      keyth
#
# Created:     19/11/2018
# Copyright:   (c) keyth 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# class for each team in the league
## it is assumed that the league only have 1 division with all the teams
## i can add multi division support maybe at a later time
class team(object):
  def __init__(self, teamName, W, score):
    self.teamName = teamName
    self.W = W

    # list of all scores from previous weeks for this team
    self.scores = []
    self.scores.append(float(score))

    # this will hold projected wins and PF
    self.futW = 0
    self.futPts = 0

    # this will accumulate averages (past + future)
    self.avgW = 0
    self.avgPts = 0

    # regular season finishes
    self.inPlayoffs = 0
    self.firstRoundBye = 0

    # playoff finishes
    self.final4 = 0
    self.final2 = 0
    self.champ = 0

  # add a game outcome (win vs loss, and PF)
  def addGame(self, W, score):
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
  def totW(self):
    return self.W + self.futW

  # get PF, past + simulated
  def totPts(self):
    return self.pts() + self.futPts

  # reset future stats -- prep for next simulation
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

  # accumulate results from a simulation
  ## did we make playoffs?
  def IncrementPlayoffs(self):
    self.inPlayoffs += 1

  ## did we get a 1st round bye?
  def IncrementBye(self):
    self.firstRoundBye += 1

  ## did we make final 4?
  def addFinal4(self):
    self.final4 += 1

  ## did we make finals?
  def addFinal2(self):
    self.final2 += 1

  ## are we the champ?
  def addChamp(self):
    self.champ += 1

  # order methods (we don't deal with equality cuz it's pretty narrow
  ## this is used to sort for standings to determine playoff berths, etc.
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

  ## this is used to sort the output table -- you can customize this one
  def __lt__(self, other):
    return self.prob * 1e10 + self.avgW * 1e5 + self.avgPts < other.prob * 1e10 + other.avgW * 1e5 + other.avgPts

