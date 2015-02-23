#!/usr/local/python

import urllib2
import json
import IPython
import re
import cStringIO
import math
from PIL import Image, ImageDraw, ImageOps

def main():
    urls = sanitizeImageUrls(getAwwImageUrls())
    images = getImages(urls)
    makeCollageFromImages(images)

def hexagon_generator(edge_length, center):
    """Generator for coordinates in a hexagon."""
    cx, cy = center
    for angle in range(0, 360, 60):
        x = cx + math.cos(math.radians(angle)) * edge_length
        y = cy + math.sin(math.radians(angle)) * edge_length
        yield x, y

def getNumberOfRowsAndColsForImageSizeAndEdgeLength(image, edge_length):
    edge_lengths_x = math.ceil(image.size[0] / edge_length)
    edge_lengths_y = math.ceil(image.size[1] / edge_length)
    cols = int(1 + math.ceil((edge_lengths_x - 1) / 1.5))
    rows = int(1 + math.ceil(edge_lengths_y / (2 * math.sin(math.radians(60)))))
    return rows, cols


def getHexCenter(row, col, edge_length):
#this will guarantee a hexagon in the upper left.
    start_x = edge_length * math.cos(math.radians(60))
    start_y = edge_length * math.sin(math.radians(60))
    x = int(start_x + (col * 1.5 * edge_length))
    y = int(start_y + (2 * row * edge_length * math.sin(math.radians(60))) - ((col % 2) * edge_length * math.sin(math.radians(60))))
    return x,y

def getImageOffset(hex_center, image):
    dx = int(hex_center[0] - (image.size[0] / 2))
    dy = int(hex_center[1] - (image.size[1] / 2))
    return dx, dy

def makeCollageFromImages(images):
    edge_length = getMaxEdgeLength(images)
    canv = Image.new('RGBA', (1366,768))
    canv_mask = Image.new('L', canv.size, color=255)
    canv_draw = ImageDraw.Draw(canv_mask)
    (rows, cols) = getNumberOfRowsAndColsForImageSizeAndEdgeLength(canv, edge_length)
    i = 0
    for row in xrange(0,rows):
        for col in xrange(0, cols):
            im = images[i]
            mask = Image.new('L', im.size, color=255)
            draw = ImageDraw.Draw(mask)
            hexagon = hexagon_generator(edge_length, center=(im.size[0]/2, im.size[1]/2))
            draw.polygon(list(hexagon), fill=0)
            inverted_mask = ImageOps.invert(mask)
            center = getHexCenter(row, col, edge_length)
            a_hex = hexagon_generator(edge_length, center)
            canv_draw.polygon(list(a_hex), fill=0)
            offset = getImageOffset(center, im)
            canv.paste(im, offset, inverted_mask)
            i = (i + 1) % len(images)

    canv.save('canv.png')
    im.save('trial.png')

def getMaxEdgeLength(images):
    MIN_EDGE_LENGTH = 100
    #just a really big number
    edge_length = 20000
    for image in images:
        edge_length = min([image.size[0]/2, image.size[1]/(math.sin(math.radians(60)) * 2), edge_length])
    if edge_length < MIN_EDGE_LENGTH:
        return MIN_EDGE_LENGTH
    return edge_length

def getImages(urls):
    limit = 4
    images = []
    for i in range(limit):
        file = cStringIO.StringIO(urllib2.urlopen(urls[i]).read())
        img = Image.open(file)
        images.append(img)
    return images

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
            if not re.search(r'i\.imgur', url):
                url = url.replace('imgur.com', 'i.imgur.com')
            url = adjustImageSize(url)
            sanitized.append(url)
    return sanitized

def adjustImageSize(url):
    url = url.replace('.jpeg', 'l.jpeg')
    url = url.replace('.jpg', 'l.jpg')
    url = url.replace('.png', 'l.png')
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
