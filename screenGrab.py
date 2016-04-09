from PIL import ImageGrab

from config import imageDir


def getScreanImage():
    pic = ImageGrab.grab()
    return pic

if __name__ ==  "__main__":
    pic = getScreanImage()
    # pic.show()
    pic.save(imageDir + "game_org.png")