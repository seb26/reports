# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import reports
import wconfig

wprefs = {

    'tfwiki': {
        'prefix': 'Team Fortress Wiki:Reports/',
        'summ': 'Updated page.',
        'blacklist': [],
        'blacklist-missingArticles': [ 'WebAPI', 'WebAPI/GetPlayerItems', 'WebAPI/GetSchema' ],
        'langs': ['ar', 'cs', 'da', 'de', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sv', 'tr', 'zh-hans', 'zh-hant' ]
    },

    'pwiki': {
        'prefix': 'Portal Wiki:Reports/',
        'summ': 'Updated page.',
        'blacklist': [],
        'langs': ['ar', 'cs', 'da', 'de', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sv', 'zh-hans', 'zh-hant' ]
    }
}

for wiki in [ 'tfwiki' ]:
    c = wprefs[wiki]
    r = reports.report(wiki)
    r.login()
    r.allArticlesEn( c['prefix'] + 'All articles/en', c['langs'], c['blacklist'], c['summ'] + ' (%s articles)')