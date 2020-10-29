# ESPNFFBProjections
Crappy tool to simulate ROS using Monte Carlo

Uses data from matchups that have already been played this season to build a team profiles (avg points, and std dev);
then performs Monte Carlo simulation to figure out playoff odds, etc.

Output looks something like this:

```
#   Player          Playoff%   Bye% Final4% Final2% Champ% AvgWins  AvgPts
 1   xxxxxxxxxxxxxx     1.000  0.964   0.979   0.572  0.371    9.41 1692.35
 2   xxxxxxxxxxxxxx     1.000  0.836   0.916   0.432  0.169    9.41 1580.50
 3   xxxxxxxxxxxxxx     1.000  0.115   0.486   0.195  0.059    8.28 1534.93
 4   xxxxxxxxxxxxxx     1.000  0.085   0.485   0.191  0.076    8.00 1557.33
 5   xxxxxxxxxxxxxx     0.899  0.000   0.550   0.321  0.186    6.38 1694.43
 6   xxxxxxxxxxxxxx     0.762  0.000   0.445   0.241  0.128    6.25 1671.34
 7   xxxxxxxxxxxxxx     0.307  0.000   0.127   0.044  0.009    6.03 1494.01
 8   xxxxxxxxxxxxxx     0.032  0.000   0.012   0.004  0.002    4.69 1460.83
 9   xxxxxxxxxxxxxx     0.000  0.000   0.000   0.000  0.000    3.85 1352.10
 10  xxxxxxxxxxxxxx     0.000  0.000   0.000   0.000  0.000    3.73 1540.07
 11  xxxxxxxxxxxxxx     0.000  0.000   0.000   0.000  0.000    3.43 1309.24
 12  xxxxxxxxxxxxxx     0.000  0.000   0.000   0.000  0.000    2.54 1190.13
```

it doesn't currently support divisions. to add that support, would take some work 
* need to parse more html to determine the divisions
* need to modify how playoff berths and byes are decided
* need to add division keys to team class

probably I won't do this, unless I get a few requests


Notes:
* there is some hardcoded stuff that I'm too lazy to automate -- this includes knowing how many weeks of the schedule to parse, etc. Change the "parse weeks" range in import_webdriver.py:import_league_data()
* in my league, we run week 12 matchups based on standings, and week 13/14 are reserved for manual playoff entry (because reasons), so you'll want to mess with that too probably. Take a look at sims.py:run_sim(), and sims.py:compute_playoffs() to customize to your league settings.
* if you want to use this and need help, lmk. i'm not against improving the code, but currently I'm the only user afaik
* check that your chrome version matches the chrome-driver version in Requirements.txt

Math Note:
* Weekly scores are simulated assuming normal distribution using a team's average score and standard deviation. I've done some analysis and this is pretty good. I don't find a lot of evidence that adding higher moments would matter, nor have I found that including autocorrelation improves anything (e.g., a team scored well in weeks (5+)6+7, so they'll do better in 8). That last bit was counter intuitive to me since it would seem to better take into account things like successful transactions, injuries, etc., but alas, FFB is random af.
