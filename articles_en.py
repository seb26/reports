import datetime
import wikitools
import settings
import time
import re
import webbrowser
from wikitools import wiki, api

print 'Logging in.'
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
print 'Logged in.'

# Setting up
report_title = settings.page_prefix + 'All English articles'

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

req = api.APIRequest(wiki, params)
res = req.query(querycontinue=True)

print 'Gottam.'

i = 0
output = []
current_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
blacklist = [ 'TF2 Official Blog/new' ]

print 'Start formatting into variables.'

bad_sub = re.compile('\/(ar|cs|da|de|es|fi|fr|hu|it|ja|ko|nl|no|pl|pt|pt-br|ro|ru|sv|tr|zh-hans|zh-hant|OTFWH|titles|Archive|Header|Footer|diff)')

for j in res['query']['allpages']:
    if not bad_sub.search(j['title']) and j['title'] not in blacklist:
        pageid = j['pageid']
        title = j['title']
        table_row = u'# [[%s]]' % title
        output.append(table_row)
        i += 1

print 'Everything now saved as "output".'

report = wikitools.Page(wiki, report_title)
report_text = report_template % (i, current_time, '\n'.join(output))
# report_text = report_text.encode('utf-8')
print 'Editing.'

report.edit(report_text, summary=settings.editsumm + ' (%s articles total)' % i, bot=1)
print 'Saved. All done.'

webbrowser.open_new_tab('http://wiki.teamfortress.com/w/index.php?title=Team_Fortress_Wiki:Reports/All_English_articles&diff=cur')