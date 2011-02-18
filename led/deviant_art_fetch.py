#!/usr/bin/env python2.6
import httplib, re, shutil

def list_photos(user):
    c = httplib.HTTPConnection(user+'.deviantart.com')
    c.request('GET', '/gallery/?catpath=scraps')
    r = c.getresponse()
    page = r.read()
    
    img_urls = []
    
    # I will burn in hell for this...
    matches = re.findall('<a [^>]*class=[\'"]?thumb[\'"]?[^>]*>', page)
    for m in matches:
        print str(m)
        m2 = re.search('super_img=[\'"]?([^\s\'"]*)[\'"]?', m)
        if m2:
            img_urls.append(m2.group(1))
    
    return img_urls

def save_photos(photos):
    for p in photos:
        if p.startswith('http://'):
            p = p[7:]
        
        host, path = p.split('/', 1)
        basename = p.rpartition('/')[-1]
        print host, path

        c = httplib.HTTPConnection(host)
        c.request('GET', '/'+path)
        r = c.getresponse()
        
        f = open(basename, 'w')
        shutil.copyfileobj(r, f)
        r.close()
        f.close()

if __name__ == '__main__':
    p = list_photos('bemis100')
    save_photos(p)