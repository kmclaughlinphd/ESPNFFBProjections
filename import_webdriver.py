from pandas.io.html import read_html
from selenium import webdriver
import chromedriver_binary
import lxml.html as lh
import time

def get_league_data(league_id):
    driver = webdriver.Chrome()

    # load web html
    driver.get('https://fantasy.espn.com/football/league/schedule?leagueId=%s' % str(league_id))
    time.sleep(5)
    table_scraps = driver.find_elements_by_class_name('matchup--table')
    doc = [lh.fromstring(table_scrape.get_attribute('innerHTML'))[0] for table_scrape in table_scraps]
    driver.close()

    return doc


# get scores from xml element
def get_scores(elem, offset):
    team1 = elem[offset][0][0][0][0][1][0][1].text
    team2 = elem[offset][5][0][0][0][1][0][1].text

    if elem[offset][2][0].getchildren():
        score1 = float(elem[offset][2][0][0][0].text)
        score2 = float(elem[offset][3][0][0][0].text)
    else:
        score1, score2 = 0, 0

    return team1, team2, score1, score2


# called from main
# grabs data via selenium, parses out scores, returns results arrays
def import_league_data(leagueID):

    # init results arrays
    past_results = []
    future_matches = []

    # scrape league data
    xml_weeks = get_league_data(leagueID)
    results_total = len(xml_weeks)

    # parse weeks
    for jj in range(results_total):

        # pull relevant xml from xpath
        week_array = xml_weeks[jj].xpath('//table/tbody/tr') # pull array of tags for each match in week jj

        # push results to array
        results = []
        for ii in range(len(week_array)):
            results.append(get_scores(week_array, ii))

        # if all scores are non-zero, then we assume the score is final
        if len(results) > 0:
            if sum([r[2] + r[3] for r in results]) == 0:
                # # add future matchups if this is week 11 or earlier (for my league, we manually pair week 12)
                # if jj < 11:
                for r in results:
                    future_matches.append([r[0], r[1]])
            else:
                for r in results:
                    past_results.append([r[0], r[1], r[2], r[3]])

    return past_results, future_matches