# coding=utf-8
from PIL import Image
import colorsys

from config import imageDir


class ColorSplit:
    def __init__(self):
        self.callLst = []
        self.callIndex = 0

    def isSameColor(self, color1, color2):
        newRBG = [0, 0, 0]
        for i in range(0, 3):
            if abs(color1[i] - color2[i]) > 40:
                return False, ()
            else:
                newRBG[i] = int((color1[i]+color2[i])/2)
        return True, (newRBG[0], newRBG[1], newRBG[2])

    def modcolor(self, color):
        if len(self.callLst) == 0:
            self.callLst.append([color, [color]])
            self.callIndex += 1
            return 0
        for i in range(0, len(self.callLst)):
            line = self.callLst[i]
            avcolor = line[0]
            ret, newRBG =  self.isSameColor(color, avcolor)
            if  ret:
                self.callLst[i][0] =  newRBG
                self.callLst[i][1].append(color)
                return i
        #not found
        self.callLst.append([color, [color]])
        self.callIndex += 1
        return self.callIndex - 1

def getAv(c, avc):
    if avc == 0:
        return c
    return int((c + avc) / 2)

def getAvColor(image):
    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))

    avR = 0
    avG = 0
    avB = 0
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        avR = getAv(r, avR)
        avG = getAv(g, avG)
        avB = getAv(b, avB)
    dominant_color = (avR, avG, avB)
    return dominant_color



#at http://www.sharejs.com/codes/python/8655
def __get_dominant_color(image):
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color

def get_dominant_color(image):
    # return __get_dominant_color(image)
    dominant_color = __get_dominant_color(image)
    r, g, b = dominant_color[0], dominant_color[1], dominant_color[2]
    if r < 30 and g < 30 and b < 30:
        return getAvColor(image)
    else:
        return dominant_color

def getStatusFromImage(filename):
    image = Image.open(filename)
    # image.show()
    imW = image.width
    imH = image.height
    eachW = imW/10
    eachH = imH/10
    arrImage = []
    #a , b
    #x , y
    for i in range(0, 10):
        line = []
        for j in range(0, 10):
            box = (j*eachW, i*eachH, j*eachW+eachW, i*eachH+eachH)
            # print(box)
            fix = int(eachH*0.2)
            box = (box[0]+ fix, box[1]+fix, box[2]-fix, box[3]-fix)
            region = image.crop(box)
            line.append(region)
        arrImage.append(line)

    print(":")
    colorArr = []
    for i in range(0, 10):
        line = []
        for j in range(0, 10):
            domiColor = get_dominant_color(arrImage[i][j])
            line.append(domiColor)
        colorArr.append(line)
    for cline in colorArr:
        print(cline)

    cs = ColorSplit()
    csArr = []
    for cline in colorArr:
        line = []
        for color in cline:
            index = cs.modcolor(color)
            #if color is black
            if color[0] < 50 and color[1] < 50 and color[2] < 50:
                line.append("")
                continue
            line.append("%d" % (index,))
        csArr.append(line)

    for cline in csArr:
        print(cline)

    # show image
    for i in range(0, 10):
        line = []
        for j in range(0, 10):
            box = (j*eachW, i*eachH, j*eachW+eachW, i*eachH+eachH)
            fix = 0
            box = (box[0]+ fix, box[1]+fix, box[2]-fix, box[3]-fix)
            region = image.crop(box)
            width, height = region.size
            imPix = region.convert("RGBA")
            pix = imPix.load()

            if csArr[i][j] == '':
                #空区域不用填
                continue
            newcolor = cs.callLst[int(csArr[i][j])][0]
            for x in xrange(0, width):
                for y in xrange(0, height):
                    imPix.putpixel((x, y), newcolor)
            image.paste(imPix, box)
    # image.show()
    newImage = image.crop((0, 0, image.width, image.height))
    newImage.save(imageDir + "core_m.png")

    return csArr

if __name__ == "__main__":
    status = getStatusFromImage(imageDir + "./game5.png")
    print("====")
    print(status)
