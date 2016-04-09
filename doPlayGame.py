# coding=utf-8
#http://www.4399.com/flash/106202.htm
import traceback
from time import sleep

import MouseEvent
from config import corefileDir, imageDir
from find_obj import TakeModeObj
from screenGrab import getScreanImage
from CreateSteps import createStep

import crach_on_ipy

g_score = 0
g_allScore = 0

def playGame():
    #save screen
    pic = getScreanImage()
    pic.save(imageDir + "game_org.png")

    #获取图像位置
    TakeModeObj()

    #生成步骤
    createStep()

    #show score
    f = open(corefileDir + "score.txt", "r")
    score = eval(f.read())
    f.close()
    print("score:", score)
    global g_score
    g_score = score
    global  g_allScore
    f = open(corefileDir + "allscore.txt", "r")
    g_allScore = eval(f.read())
    g_allScore += g_score
    f.close()
    f = open(corefileDir + "allscore.txt", "w")
    f.write(str(g_allScore))
    f.close()

    #play
    f = open(corefileDir + "posit.txt")
    box  = eval(f.read())
    f.close()
    f = open(corefileDir + "step.txt")
    steps = eval(str(f.read()))
    f.close()

    print(box)
    print(steps)
    X0 = box[0]
    Y0 = box[1]
    eachH = int((box[2] - box[0])/10)
    eachW = int((box[3] - box[1])/10)
    fixH = int(eachH/2)
    fixW = int(eachW/2)

    print("====")
    x = 0
    y = 0
    mouseX = X0 + eachH*x + fixH
    mouseY = Y0 + eachW * y + fixW
    print("mouse ", mouseX, mouseY)
    MouseEvent.mouse_click(mouseX, mouseY)
    print("====start====")
    print("score:", score)


    hasDoStep = 0
    for oneStep in steps:
        hasDoStep+=1

        if g_score < 2000 and hasDoStep > 6:
            return False
        if hasDoStep > 10:
            return False

        step = None
        for stepT in oneStep:
            step = stepT
            break
        print("step:", step)
        x = step[1]
        y = step[0]
        mouseX = X0 + eachH*x + fixH
        mouseY = Y0 + eachW * y + fixW
        print("click mouse ", mouseX, mouseY)

        MouseEvent.mouse_click(mouseX, mouseY)
        # sleep(0.05)
        MouseEvent.mouse_click(mouseX, mouseY)
        # sleep(0.1)
        MouseEvent.mouse_click(mouseX, mouseY)
        # sleep(0.3)
        # return
        sleep(1)
        if len(oneStep) > 6:
            print("delete too long ...")
            sleep(1.4)
    print("finish ")
    return True

if __name__ == "__main__":
    for i in range(0, 600):
        try:
            isFinish = playGame()
            print("g_score", g_score)
            print("g_allScore", g_allScore)
            MouseEvent.mouse_move(0, 0)
            if isFinish == True:
                print("finish ...")
                sleep(15)
            else:
                sleep(1)
        except Exception as e:
            traceback.print_exc()
            raise