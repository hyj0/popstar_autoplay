# coding=utf-8
#qinxuye.me/article/implement-sketch-and-pencil-with-pil/
from PIL import Image

from config import imageDir


def sketch(img, threshold):
    '''
    素描
    param img: Image实例
    param threshold: 介于0到100
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100

    width, height = img.size
    img = img.convert('L') # convert to grayscale mode
    pix = img.load() # get pixel matrix

    for w in xrange(width):
        for h in xrange(height):
            if w == width-1 or h == height-1:
                continue

            src = pix[w, h]
            dst = pix[w+1, h+1]

            diff = abs(src - dst)

            if diff >= threshold:
                pix[w, h] = 0
            else:
                pix[w, h] = 255

    return img

if __name__ == '__main__':
    image = Image.open("../" + imageDir + 'game.png')
    newImage = sketch(image, 10)
    newImage.show()
    sketch(Image.open("../" + imageDir + "game5.png"), 10).show()