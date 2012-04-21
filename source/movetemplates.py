#!/usr/bin/env python3.2
#import sys;reload(sys);sys.setdefaultencoding('utf-8')
import os, sys, shutil

templatepath = 'templates'
results      = '../results/'
mainpath    = templatepath + "/main.mustache"
indexpath   = templatepath + "/index.mustache"
archivepath = templatepath + "/archive.mustache"
frompath = "/Users/bobuk/Documents/addmetocc"

def build(fname = 'index.html', topath = mainpath,
                        content = '{{& content }}'):
    with open(os.path.join(frompath, fname)) as fl:
        bl = fl.read()
        [first, buuu, last] = bl.split('@@@')
        res = first + content + last
        res = res.replace('@TITLE@', '{{ title }}')
        res = res.replace('@permalink@', '{{ permalink }}')
        res = res.replace('main.css', '/main.css')
        res = res.replace('images/', '/images/')
        with open(topath, 'w') as flw:
            flw.write(res)

if __name__ == '__main__':
    build('index.html', mainpath)
    build('index.html', indexpath)
    build('index.html', archivepath,
        content="""
        <ul>
        {{#items }}
            <li><a href="{{ fname }}">{{ subtitle }}</a></li>
        {{/items }}
        </ul>
        """)
    shutil.copy(os.path.join(frompath, 'main.css'),
                os.path.join(results, 'main.css')
    )
    #os.system('rsync -avr %s %s' %
    #            (os.path.join(frompath, 'images'),
    #            results + '/'))

