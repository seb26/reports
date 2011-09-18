# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import re
import datetime
import wikitools
import webbrowser
import wconfig

class report:

    def __init__(self, wiki):
        self.templates = {
            'allArticlesEn': '''
List of all English articles; <onlyinclude>%s</onlyinclude> in total. Data as of %s.

* ''See also:'' [[Special:RecentChangesLinked/Team_Fortress_Wiki:Reports/All_English_articles|Recent changes to English articles]]

== List ==
%s
''',

            'allArticles': u'''All articles in {{{{lang info|{0}}}}}; \'''<onlyinclude>{1}</onlyinclude>\''' in total. Data as of {2}.

; See also
* [[Project:Reports/Missing translations/{0}|Missing translations in {{{{lang name|name|{0}}}}}]]
* [[Special:RecentChangesLinked/Project:Reports/All articles/{0}|Recent changes to articles in {{{{lang name|name|{0}}}}}]]

== List ==
{3}
''',
            'missingArticles': u'''Pages missing in {{{{lang info|{0}}}}}: \'''<onlyinclude>{1}</onlyinclude>\''' in total. Data as of {2}.

; See also
* [[Project:Reports/All articles/{0}|All articles in {{{{lang name|name|{0}}}}}]]
* [[Special:RecentChangesLinked/Project:Reports/All articles/{0}|Recent changes to articles in {{{{lang name|name|{0}}}}}]]

== List ==
{3}
'''

        }

        self.wikiname = wiki
        self.config = wconfig.config[wiki]

    def login(self):
        print 'Logging in.'
        self.wiki = wikitools.Wiki(self.config['url-api'])
        self.wiki.login(self.config['usr'], self.config['pwd'])
        print 'Logged in.'

    def allArticlesEn(self, pagetitle, langs, blacklist, summ):

        def isGoodTitle(title):
            if title in blacklist:
                return False
            badguys = [ 'OTFWH', 'titles', 'Archive', 'Header', 'Footer', 'diff' ]
            badguys.extend(langs)
            for bad in badguys:
                if title.endswith('/' + bad):
                    return False
            if title.endswith('/prop'):
                return False

            return True # Otherwise, he's clean.

        params = {
            'action': 'query',
            'list': 'allpages',
            'aplimit': '5000',
            'apfilterredir': 'nonredirects'
            }

        print 'allArticlesEn: getting API data...'

        req = wikitools.api.APIRequest(self.wiki, params)
        res = req.query(querycontinue=True)

        print 'allArticlesEn: filtering list...'

        row = u'# [[%s]]'
        output = [ row % n['title'] for n in res['query']['allpages'] if isGoodTitle(n['title']) ]

        print 'allArticlesEn: preparing to edit...'

        report = wikitools.Page(self.wiki, pagetitle)
        time = (datetime.datetime.utcnow() - datetime.timedelta(seconds=0)).strftime('%H:%M, %d %B %Y (UTC)')
        text = self.templates['allArticlesEn'] % (len(output), time, '\n'.join(output))

        print 'allArticlesEn: editing...'
        report.edit(text, summary=summ % len(output), bot=1)
        print 'allArticlesEn: saved.'

        webbrowser.open_new_tab(self.config['url'] + 'index.php?title=%s&diff=cur' % pagetitle.replace(' ', '_') )

    def allArticles(self, pagetitle, langs):
        params = {
            'action': 'query',
            'list': 'allpages',
            'aplimit': '5000',
            'apfilterredir': 'nonredirects'
            }

        print 'allArticles: getting API data...'

        req = wikitools.api.APIRequest(self.wiki, params)
        res = req.query(querycontinue=True)

        allp = [ z['title'] for z in res['query']['allpages'] ]

        print 'allArticles: got all pages.'
        print 'allArticles: today I\'m preparing lists for: {0}'.format(', '.join(langs))

        for lang in langs:
            log = 'allArticles: {0} >'.format(lang)
            print log, 'preparing list...'
            output = [ u'# [[{0}]]'.format(z) for z in allp if z.endswith('/' + lang)]
            time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
            output_u = [ u(s) for s in output ]
            text = self.templates['allArticles'].format(lang, len(output_u), time, '\n'.join(output_u))

            report = wikitools.Page(self.wiki, pagetitle.format(lang))
            print log, 'editing...'
            report.edit(text, summary=self.config['summ'] + ' ({0} articles)'.format(len(output_u)), bot=1)
            print log, 'done.'

    def missingArticles(self, pagetitle, langs, title_list_en, title_list, blacklist):
        print 'missingArticles: getting list_en...'
        list_en = wikitools.Page(self.wiki, title_list_en).getLinks()

        for lang in langs:
            log = 'missingArticles: {0} >'.format(lang)
            list_z = []
            print log, 'preparing & getting links...'
            raw_z = wikitools.Page(self.wiki, title_list).getLinks()
            if list_z != 0:
                list_z.extend(raw_z)
            else:
                print log, 'error: getLinks() on {0} returned nothing'.format(title_list)
                list_z.append('ERROR')

            formatstr = u'# [[{0}]] ([[{0}/{1}|create]])'
            print log, 'formatting list...'
            list_y = [ item[:-len(lang)-1] for item in list_z ] # Strip '/xx' from names and create a new list.
            diff = list(set(list_en)-set(list_y)) # List comparison. Articles in the en list that aren't on lang's own list.
            diff.sort()

            # Format names into wikicode if they don't appear in config['blacklist'].
            list_output = [ formatstr.format(name, lang) for name in diff if name not in blacklist ]
            list_output.sort()

            report = wikitools.Page(self.wiki, pagetitle.format(lang))
            time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
            text = self.templates['missingArticles'].format(lang, len(list_output), time, u'\n'.join(list_output))

            print log, 'editing...'
            report.edit(text, summary=self.config['summ'] + ' ({0} articles)'.format(len(list_output)), bot=1)
            print log, 'done.'

