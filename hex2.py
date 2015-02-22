import math
from PIL import Image, ImageDraw, ImageOps

def hexagon_generator(edge_length, offset):
  """Generator for coordinates in a hexagon."""
  x, y = offset
  for angle in range(0, 360, 60):
    x += math.cos(math.radians(angle)) * edge_length
    y += math.sin(math.radians(angle)) * edge_length
    yield x, y

def hexagon_generator2(edge_length, center):
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

def main():
  im = Image.open('test.jpg')
  im.thumbnail((300,300))
  mask = Image.new('L', im.size, color=255)
  draw = ImageDraw.Draw(mask)
  edge_length = im.size[0]/2
  hexagon = hexagon_generator2(im.size[0]/2, center=(im.size[0]/2, im.size[1]/2))
  draw.polygon(list(hexagon), fill=0)
  inverted_mask = ImageOps.invert(mask)
  #im.putalpha(inverted_mask)
  canv = Image.new('RGBA', (im.size[0] * 2, im.size[1]*2))
  canv_mask = Image.new('L', canv.size, color=255)
  canv_draw = ImageDraw.Draw(canv_mask)
  (rows, cols) = getNumberOfRowsAndColsForImageSizeAndEdgeLength(canv, edge_length)
  for row in xrange(0,rows):
    for col in xrange(0, cols):
        center = getHexCenter(row, col, edge_length)
        print center
        a_hex = hexagon_generator2(edge_length, center)
        canv_draw.polygon(list(a_hex), fill=0)
        offset = getImageOffset(center, im)
        print offset
        print '-------'
        canv.paste(im, offset, inverted_mask)

        #canv.paste(im, offset, canv_mask)


  
  canv.save('canv.png')
  im.save('trial.png')

if __name__ == '__main__':
    main()
