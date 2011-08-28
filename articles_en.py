# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import datetime
import re
import wikitools
import webbrowser
import wconfig
config = wconfig.config[wconfig.config['default']]

print 'Logging in.'
wiki = wikitools.Wiki(config['url-api'])
wiki.login(config['usr'], config['pwd'])
print 'Logged in.'

# Setting up
report_title = config['pagepref'] + 'All articles/en'

report_template = '''
List of all English articles; <onlyinclude>%s</onlyinclude> in total. Data as of %s.

* ''See also:'' [[Special:RecentChangesLinked/Team_Fortress_Wiki:Reports/All_English_articles|Recent changes to English articles]]

== List ==
%s
'''

params = {
    'action': 'query',
    'list': 'allpages',
    'aplimit': '5000',
    'apfilterredir': 'nonredirects'
    }

print 'Getting API data based on parameters.'

req = wikitools.api.APIRequest(wiki, params)
res = req.query(querycontinue=True)

print 'Gottam.'

i = 0
output = []
blacklist = []

print 'Start formatting into variables.'

bad_sub = re.compile('\/(ar|cs|da|de|es|fi|fr|hu|it|ja|ko|nl|no|pl|pt|pt-br|ro|ru|sv|tr|zh-hans|zh-hant|OTFWH|titles|Archive|Header|Footer|diff)')

for j in res['query']['allpages']:
    if not bad_sub.search(j['title']) and j['title'] not in blacklist and not j['title'].endswith('/prop'):
        pageid = j['pageid']
        title = j['title']
        table_row = u'# [[%s]]' % title
        output.append(table_row)
        i += 1

print 'Everything now saved as "output".'

report = wikitools.Page(wiki, report_title)
time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
report_text = report_template % (i, time, '\n'.join(output))
# report_text = report_text.encode('utf-8')
print 'Editing.'

report.edit(report_text, summary=config['summ'] + ' (%s articles total)' % i, bot=1)
print 'Saved. All done.'

webbrowser.open_new_tab(config['url'] + 'index.php?title=Project:Reports/All_articles/en&diff=cur')