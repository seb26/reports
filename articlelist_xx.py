# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import datetime
import wikitools
import wconfig
config = wconfig.config[wconfig.config['default']]

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

template = u'''All articles in {{{{lang info|{0}}}}}; \'''<onlyinclude>{1}</onlyinclude>\''' in total. Data as of {2}.

; See also
* [[Project:Reports/Missing translations/{0}|Missing translations in {{{{lang name|name|{0}}}}}]]
* [[Special:RecentChangesLinked/Project:Reports/All articles/{0}|Recent changes to articles in {{{{lang name|name|{0}}}}}]]

== List ==
{3}
'''

if len(sys.argv) > 2 and sys.argv[1] == '-l':
    langs = sys.argv[2:]
else:
    langs = config['langs']

print 'Logging in.'
wiki = wikitools.Wiki(config['url-api'])
wiki.login(config['usr'], config['pwd'])
print 'Logged in.'

params = {
    'action': 'query',
    'list': 'allpages',
    'aplimit': '5000',
    'apfilterredir': 'nonredirects'
    }

print 'Getting API data based on parameters.'

req = wikitools.api.APIRequest(wiki, params)
res = req.query(querycontinue=True)

allp = [ z['title'] for z in res['query']['allpages'] ]

print 'Got all pages.'
print 'Today I\'m preparing lists for: {0}'.format(', '.join(langs))

for lang in langs:
    print '{0} > preparing list...'.format(lang)
    output = []
    output.extend([ u'# [[%s]]' % z for z in allp if z.endswith('/' + lang)])
    time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
    output_u = [ u(s) for s in output ]
    report_text = template.format(lang, len(output_u), time, '\n'.join(output_u))

    report = wikitools.Page(wiki, config['pagepref'] + 'All articles/' + lang)
    print '{0} > editing...'.format(lang)
    report.edit(report_text, summary=config['summ'] + ' ({0} articles)'.format(len(output_u)), bot=1)
    print '{0} > done.'.format(lang)