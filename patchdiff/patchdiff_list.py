import wikitools
import wconfig

import os
from collections import defaultdict
import datetime
import re

"""

## FIRST STEP is to get data. Need to dump to file. Don't want to run this the whole time.

# Setup wiki
config = wconfig.config['tfwiki']
print 'Logging in.'
wiki = wikitools.Wiki(config['url-api'])
wiki.login(config['usr'], config['pwd'])
print 'Logged in.'

params = {
    'action': 'query',
    'list': 'allpages',
    'aplimit': '5000',
    'apfilterredir': 'nonredirects',
    'apprefix': 'PatchDiff/',
    'apnamespace': '10'
    }

print 'allArticles: getting API data...'

req = wikitools.api.APIRequest(wiki, params)
res = req.query(querycontinue=True)

f = open('patchdiff.0.dump', 'wb').write(unicode(res).encode('utf-8'))

"""

g = eval(open('patchdiff.0.dump','rb').read().decode('utf8')) # BAD BAD Do not do this unless you trust data.

# Now begins a heap of sorting and cutting and other stuff I can't remember because
# I didn't name variables properly or document much.

group = []

for page in g['query']['allpages']:
    title = page['title']
    path = title.split(r'/')
    if len(path) > 2:
        group.append(( path[1], path[2:] ))
    else:
        continue

d = defaultdict(list)

for patch, fpath in group:
    f = u'/'.join(fpath)
    d[f].append(patch)

data = []

for fpath, p in d.items():
    x = []
    for i in p:
        patch = re.sub(r'\sPatch.*', '', i)
        patch_date = datetime.datetime.strptime(patch, '%B %d, %Y').strftime('%Y-%m-%d')
        x.append(( patch_date, patch, i )) # Y-m-d date, human shortened date, patch page name
    data.append(( fpath, x ))

c = defaultdict(list)

for f, patches in data:
    fpath = f.split(r'/')
    if len(fpath) <= 3:
        traverse = 2
    else:
        traverse = 3
    head = u'/'.join(fpath[:traverse])
    c[head].append(( u'/'.join(fpath[traverse:]), patches ))

# Wikitext output
w_folder = u"=== <code>{0}</code> ==="
w_file = u"""<div style="font-size:1.5em; font-weight:bold; font-family:monospace;">[*] {0}</div>"""
w_revision = u"""<div class="diffname {0}" style="margin-left:2em;"><div class="diff-file"><div class="diff-name-text" style="color:#666;">Revision:<span class="diff-name" style="display:none;">[[Template:PatchDiff/{0}/{1}|{1}]]</span> ({2}) {0}</div><div class="diff-contents"></div></div></div>"""

for folder, files in c.items():
    folderPrint = False
    for f in files:
        path = folder + ur'/' + f[0]
        if len(f[1]) > 2:
            if not folderPrint:
                # Print folder name header, but only for folders that have files that meet the requirement
                print w_folder.format(folder)
                folderPrint = True
            print w_file.format(path)
            patches = sorted(f[1], key=lambda a:a[0], reverse=True)
            for patch in patches:
                print w_revision.format(patch[2], path, patch[0])
        else:
            continue # Skip files that have only been diffed once.

"""
# Get all dates in one list
dates = []

for folder, files in c.items():
    for f in files:
        dates.append(f[1])

s = sorted(dates, key=lambda a:a[0], reverse=True)

tt = [ i for i in s if s ]

for z in tt:
    print z
"""