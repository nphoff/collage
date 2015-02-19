#!/usr/local/python

import urllib2
import json
import IPython
import re
import cStringIO
from PIL import Image

def main():
    urls = sanitizeImageUrls(fakeGetUrls())
    makeCollage(urls)

    
    #IPython.embed()

def makeCollage(urls):
    limit = 3
    images = []
    for i in range(limit):
        file = cStringIO.StringIO(urllib2.urlopen(urls[i]).read())
        img = Image.open(file)
        images.append(img)
    IPython.embed()


def getAwwImageUrls():
    response = urllib2.urlopen('http://www.reddit.com/r/aww/.json')
    aww_json = json.loads(response.read())
    #might need some error handling for if I get a bad response
    posts = aww_json['data']['children']
    urls = [x['data']['url'] for x in posts]
    return urls

def sanitizeImageUrls(urls):
    sanitized = []
    for url in urls:
        if re.search(r'\/a\/', url):
            print "album!"
        elif re.search(r'\.gifv', url):
            print "gifv"
        elif re.search(r'imgur', url):
            #good, it's from imgur
            if not re.search(r'i\.imgur', url):
                url = url.replace('imgur.com', 'i.imgur.com')
            url = adjustImageSize(url)
            sanitized.append(url)
    return sanitized

def adjustImageSize(url):
    url = url.replace('.jpeg', 'm.jpeg')
    url = url.replace('.jpg', 'm.jpg')
    url = url.replace('.png', 'm.png')
    return url

def fakeGetUrls():
    return [u'http://imgur.com/a/WNOPk',
            u'http://i.imgur.com/jeUY7Pn.jpg',
            u'http://i.imgur.com/rK6ef3s.jpg',
            u'http://i.imgur.com/oRbEO2z.jpg',
            u'http://i.imgur.com/bZKqoHz.jpg',
            u'http://i.imgur.com/ejcwE6q.jpg',
            u'http://i.imgur.com/RSgNQFo.png',
            u'http://i.imgur.com/WyE7gw7.jpg',
            u'http://i.imgur.com/7rOsrP9.jpg',
            u'http://i.imgur.com/tHtGEQR.jpg',
            u'http://i.imgur.com/aFU8qu5.png',
            u'http://i.imgur.com/dKKDgEF.jpg',
            u'http://i.imgur.com/MTjlmuR.jpg',
            u'http://i.imgur.com/JJBgL2M.jpg',
            u'http://i.imgur.com/48wgd15.jpg',
            u'http://i.imgur.com/1yQYZFQ.jpg',
            u'http://www.imgur.com/ak0QalE.jpeg',
            u'http://i.imgur.com/V2yYUB3.jpg',
            u'http://i.imgur.com/Bz9fanO.gifv',
            u'http://i.imgur.com/0zS6ruQ.png',
            u'http://imgur.com/a/JCJ0n',
            u'http://imgur.com/a/YXNJX',
            u'http://i.imgur.com/tvcJMwe.jpg',
            u'http://i.imgur.com/feMD86N.jpg',
            u'http://imgur.com/i64Uqw9']

if __name__ == "__main__":
    main()
