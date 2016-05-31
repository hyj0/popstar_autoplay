#!/usr/bin/env python
# coding=utf-8

'''
Feature-based image matching sample.

Note, that you will need the https://github.com/Itseez/opencv_contrib repo for SIFT and SURF

USAGE
  find_obj.py [--feature=<sift|surf|orb|akaze|brisk>[-flann]] [ <image1> <image2> ]

  --feature  - Feature to use. Can be sift, surf, orb or brisk. Append '-flann'
               to feature name to use Flann-based matcher instead bruteforce.

  Press left mouse button on a feature point to see its matching point.
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
from PIL import Image

from common import anorm, getsize
from config import imageDir, corefileDir
from sketchImage.SketchImage import sketch

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
FLANN_INDEX_LSH    = 6


def init_feature(name):
    chunks = name.split('-')
    if chunks[0] == 'sift':
        detector = cv2.xfeatures2d.SIFT_create()
        norm = cv2.NORM_L2
    elif chunks[0] == 'surf':
        detector = cv2.xfeatures2d.SURF_create(800)
        norm = cv2.NORM_L2
    elif chunks[0] == 'orb':
        detector = cv2.ORB_create(400)
        norm = cv2.NORM_HAMMING
    elif chunks[0] == 'akaze':
        detector = cv2.AKAZE_create()
        norm = cv2.NORM_HAMMING
    elif chunks[0] == 'brisk':
        detector = cv2.BRISK_create()
        norm = cv2.NORM_HAMMING
    else:
        return None, None
    if 'flann' in chunks:
        if norm == cv2.NORM_L2:
            flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        else:
            flann_params= dict(algorithm = FLANN_INDEX_LSH,
                               table_number = 6, # 12
                               key_size = 12,     # 20
                               multi_probe_level = 1) #2
        matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
    else:
        matcher = cv2.BFMatcher(norm)
    return detector, matcher


def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, kp_pairs

g_corner = None

def explore_match(win, img1, img2, kp_pairs, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        #todo:绘制匹配区
        # cv2.polylines(vis, [corners], True, (255, 255, 255))
        cv2.polylines(vis, [corners], True, (0, 0, 255))
        print("corners:", corners)
        global g_corner
        g_corner = corners
        # return vis

    if status is None:
        status = np.ones(len(kp_pairs), np.bool_)
    p1, p2 = [], []  # python 2 / python 3 change of zip unpacking
    for kpp in kp_pairs:
        p1.append(np.int32(kpp[0].pt))
        p2.append(np.int32(np.array(kpp[1].pt) + [w1, 0]))

    green = (0, 255, 0)
    red = (0, 0, 255)
    white = (255, 255, 255)
    kp_color = (51, 103, 236)
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            col = green
            cv2.circle(vis, (x1, y1), 2, col, -1)
            cv2.circle(vis, (x2, y2), 2, col, -1)
        else:
            col = red
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
            cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)
    vis0 = vis.copy()
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            cv2.line(vis, (x1, y1), (x2, y2), green)

    cv2.imshow(win, vis)

    def onmouse(event, x, y, flags, param):
        print("onmouse:", x, y)
        cur_vis = vis
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cur_vis = vis0.copy()
            r = 8
            m = (anorm(p1 - (x, y)) < r) | (anorm(p2 - (x, y)) < r)
            idxs = np.where(m)[0]
            kp1s, kp2s = [], []
            for i in idxs:
                 (x1, y1), (x2, y2) = p1[i], p2[i]
                 col = (red, green)[status[i]]
                 cv2.line(cur_vis, (x1, y1), (x2, y2), col)
                 kp1, kp2 = kp_pairs[i]
                 kp1s.append(kp1)
                 kp2s.append(kp2)
            cur_vis = cv2.drawKeypoints(cur_vis, kp1s, None, flags=4, color=kp_color)
            cur_vis[:,w1:] = cv2.drawKeypoints(cur_vis[:,w1:], kp2s, None, flags=4, color=kp_color)

        cv2.imshow(win, cur_vis)
    cv2.setMouseCallback(win, onmouse)
    return vis

def TakeModeObj(UseSketchImage = False):
    print(__doc__)
    import sys, getopt
    opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
    opts = dict(opts)
    feature_name = opts.get('--feature', 'akaze')
    fn1sk = ''
    fn2sk = ''
    try:
        fn1, fn2 = args
    except:
        # fn1 = '../data/box.png'
        fn1 = imageDir + "downbot.png"
        fn2 = imageDir + 'game_org.png'
        if UseSketchImage == True:
            fn1 = imageDir + "moble_mod.png"

        if UseSketchImage:
            skfn1 = sketch(Image.open(fn1), 1)
            skfn1.save(imageDir + "skfn1.png")
            skfn2 = sketch(Image.open(fn2), 1)
            skfn2.save(imageDir + "skfn2.png")
            fn1sk = imageDir + "skfn1.png"
            fn2sk = imageDir + "skfn2.png"
    img1 = cv2.imread(fn1, 0)
    img2 = cv2.imread(fn2, 0)
    if UseSketchImage:
        img1 = cv2.imread(fn1sk, 0)
        img2 = cv2.imread(fn2sk, 0)

    detector, matcher = init_feature(feature_name)

    if img1 is None:
        print('Failed to load fn1:', fn1)
        sys.exit(1)

    if img2 is None:
        print('Failed to load fn2:', fn2)
        sys.exit(1)

    if detector is None:
        print('unknown feature:', feature_name)
        sys.exit(1)

    print('using', feature_name)

    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)
    print('img1 - %d features, img2 - %d features' % (len(kp1), len(kp2)))

    def match_and_draw(win):
        print('matching...')
        raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) #2
        p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches)
        if len(p1) >= 4:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
        else:
            H, status = None, None
            print('%d matches found, not enough for homography estimation' % len(p1))

        vis = explore_match(win, img1, img2, kp_pairs, status, H)

    match_and_draw('find_obj')
    if True:
        pilimage2 = Image.open(fn2)
        pilimage1 = Image.open(fn1)
        pilimageMod = Image.open(imageDir + "game5.png")
        box = (g_corner[0][0]-pilimage1.width, g_corner[1][1]-pilimageMod.height, g_corner[2][0]-pilimage1.width, g_corner[3][1]-pilimage1.height)
        if UseSketchImage:
            box = (g_corner[0][0]-pilimage1.width, g_corner[1][1], g_corner[2][0] - pilimage1.width, g_corner[3][1])
        print("box:", box)
        region = pilimage2.crop(box)
        # region.show()
        region.save(imageDir + "core.png")
        f = open(corefileDir + "posit.txt", "w")
        f.write(str(box))
        f.close()
    cv2.waitKey()
    cv2.destroyAllWindows()

def TakeModeObjUseCalc():
    heightFix = ((685.0/1920)+(343.0/960))/2
    print("heightFix", heightFix)
    im = Image.open(imageDir+"./game_org.png")
    width, height= im.size
    posit = (0, int(heightFix*height), width, int(heightFix*height+width))
    print("posit", posit)
    region = im.crop(posit)
    region.save(imageDir+"core.png")
    f = open(corefileDir + "posit.txt", "w")
    f.write(str(posit))
    f.close()


if __name__ == '__main__':
    # TakeModeObj(UseSketchImage=True)
    TakeModeObjUseCalc()