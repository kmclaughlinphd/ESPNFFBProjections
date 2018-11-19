#!/usr/bin/python

import sys, os
import csv
import requests
import lxml.html as lh
import pandas as pd

sys.path.append('.')
from classes import *

def importLeagueData(leagueID):

    # grab league data
    url = 'http://games.espn.com/ffl/schedule?leagueId=' + str(leagueID)

    # get html and parse out table rows
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements=doc.xpath('//tr')

    PAST_RESULTS = []
    FUTURE_MATCHES = []

    # loop thru table rows, and store shit
    for t in tr_elements:
        if len(t) == 6: # only check rows that have the correct number of elements
            if not t[1].text == 'OWNER(S)': # skip these
                # so these are all the games past and future
                score = t[5][0][0].text

                # if the score cell is "Preview" or "Box" it means that game hasn't happened yet
                # we add those to FUTURE_MATCHES
                if score == 'Preview' or score == 'Box':
                    FUTURE_MATCHES.append([t[1].text, t[4].text])
                else:
                    ss = score.split('-')
                    PAST_RESULTS.append([t[1].text, t[4].text, ss[0], ss[1]])

    return PAST_RESULTS, FUTURE_MATCHES
