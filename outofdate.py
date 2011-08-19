# -*- coding: UTF-8 -*-

import sys
import datetime
import re

import settings
import wikitools
from wikitools import wiki, api

def u(s):
	if type(s) is type(u''):
		return s
	if type(s) is type(''):
		try:
			return unicode(s)
		except:
			try:
				return unicode(s.decode('utf8'))
			except:
				try:
					return unicode(s.decode('windows-1252'))
				except:
					return unicode(s, errors='ignore')
	try:
		return unicode(s)
	except:
		try:
			return u(str(s))
		except:
			return s

print 'Logging in.'
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
print 'Logged in.'

print 'Getting list_en.'
# list_en = wikitools.Page(wiki, 'Team Fortress Wiki:Reports/All English articles').getLinks()

list_en = []
list_xx = [ 'Soldier', 'Scout', "Batter's Helmet" ]
rc_format = '%s: %s %s (Talk | contribs | block) (%s)'
lang = 'ru'

params = {
    'action': 'query',
    'prop': 'revisions',
    'indexpageids': '1'
    }
params['titles'] = '|'.join(list_xx)

print 'Getting API data based on params.'
req = api.APIRequest(wiki, params)
res = req.query(querycontinue=False)

for pid in res['query']['pageids']:
    page_xx = res['query']['pages'][pid]['title'] + '/' + lang
    page_xx = u(str(page_xx))

    params_xx = {
        'action': 'query',
        'prop': 'revisions',
        'indexpageids': '1',
        'titles': page_xx
        }
    req_xx = api.APIRequest(wiki, params_xx)
    res_xx = req.query(querycontinue=False)

    pid_xx = res_xx['query']['pageids'][0]
    revision = res['query']['pages'][pid]['revisions'][0]
    revision_xx = res_xx['query']['pages'][pid_xx]['revisions'][0]

    print res['query']['pages'][pid]['title'], res_xx['query']['pages'][pid_xx]['title']
    print revision['timestamp'], revision_xx['timestamp']
    print revision['user'], revision_xx['user']