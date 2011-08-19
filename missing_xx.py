# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import datetime
import wikitools
import testpyconfig as config

if len(sys.argv) > 2 and sys.argv[1] == '-l':
    langs = sys.argv[2:]
else:
    langs = config.langs

template = u'''Pages missing in {{{{lang info|{0}}}}}: \'''<onlyinclude>{1}</onlyinclude>\''' in total. Data as of {2}.

== List ==
{3}
'''

print 'Logging in.'
wiki = wikitools.Wiki(config.apiurl)
wiki.login(config.username, config.password)
print 'Logged in.'

print 'Getting list_en.'
list_en = wikitools.Page(wiki, 'Team Fortress Wiki:Reports/All English articles').getLinks()

for lang in langs:
    list_z = []
    print '{0} > Preparing & getting links...'.format(lang)
    raw_z = wikitools.Page(wiki, 'Team Fortress Wiki:Reports/All articles/{0}'.format(lang)).getLinks()
    if list_z != 0:
        list_z.extend(raw_z)
    else:
        print '{0} > Error. getLinks() on Team Fortress Wiki:Reports/All articles/{0} didn\' return anything'.format(lang)
        list_z.append('ERROR')

    formatstr = u'# [[{0}]] ([[{0}/{1}|create]])'
    print '{0} > Formatting list...'.format(lang)
    list_y = [ item[:-len(lang)-1] for item in list_z ] # Strip '/xx' from names and create a new list.
    diff = list(set(list_en)-set(list_y)) # List comparison. Articles in the en list that aren't on lang's own list.
    diff.sort()

    # Format names into wikicode if they don't appear in config.blacklist.
    list_output = [ formatstr.format(name, lang) for name in diff if name not in config.blacklist ]
    list_output.sort()

    report = wikitools.Page(wiki, config.page_prefix + 'Missing translations/' + lang)
    time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
    text = template.format(lang, len(list_output), time, u'\n'.join(list_output))

    print '{0} > Editing...'.format(lang)
    report.edit(text, summary=config.editsumm + ' ({0} articles)'.format(len(list_output)), bot=1)
    print '{0} > Done.'.format(lang)