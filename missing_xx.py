import datetime
import wikitools
import settings
import time
import re
from optparse import OptionParser
from wikitools import wiki, api

# Parse CLI arguments
parser = OptionParser()
parser.add_option('--lang', dest='lang')
(options, args) = parser.parse_args()
lang = options.lang # Remapping this for convenience.

print 'Logging in.'
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
print 'Logged in.'

i = 0
reSuffix = re.compile('\/' + lang)
blacklist = settings.blacklist

report_title = settings.page_prefix + 'Missing translations/' + lang
report_template = '''Pages missing in {{lang info|%s}}: <onlyinclude>%s</onlyinclude> articles. Data as of %s.

:\'''Note\''': articles that appear to have been created already may exist as a redirect, or are simply missing from [[:Category:%s]].

== List ==
%s
'''

print 'Getting list_en.'
list_en = wikitools.Page(wiki, 'Team Fortress Wiki:Reports/All English articles').getLinks()
list_xx = []
list_yy = []
list_zz = []

params = {
    'action': 'query',
    'list': 'categorymembers',
    'cmtitle': 'Category:' + lang,
    'cmlimit': '5000',
    'cmnamespace': '0',
    'cmdir': 'asc',
    'indexpageids': '1'
    }
print 'Getting API data based on parameters.'
req = api.APIRequest(wiki, params)
res = req.query(querycontinue=True)

print 'Start parsing for list_xx.'
for j in res['query']['categorymembers']:
    title = reSuffix.sub('', j['title'])
    list_xx.append(title)

print 'Now compare the two.'
list_yy = list(set(list_en)-set(list_xx))

print 'Format contents into wikitext.'
for z in list_yy:
    format = u'# [[%s]] ([[%s/%s|create]])' % (z, z, lang)
    if z not in blacklist:
        list_zz.append(format)
        list_zz.sort()
        i += 1
    
report = wikitools.Page(wiki, report_title)
current_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
report_text = report_template % (lang, i, current_time, lang, '\n'.join(list_zz))
# report_text = report_text.encode('utf-8')
print 'Editing.'

report.edit(report_text, summary=settings.editsumm + ' (%s articles)' % i, bot=1)
print 'Saved. All done.'