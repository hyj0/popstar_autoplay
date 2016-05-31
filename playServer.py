# coding=utf-8
import tornado.ioloop
import tornado.web
import os
import json

from CreateSteps import createStep
from config import imageDir, corefileDir
from find_obj import TakeModeObj, TakeModeObjUseCalc


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class PlayHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        file_metas = self.request.files['binaryFile']  # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filepath = imageDir + "game_org.png"
            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        #获取图像位置
        # TakeModeObj(UseSketchImage=True)
        TakeModeObjUseCalc()
        #生成步骤
        createStep()

        clickLst = self.getClickList()
        self.write(json.dumps(clickLst))

    def getClickList(self):
        retXYList = []
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
        # MouseEvent.mouse_click(mouseX, mouseY)
        print("====start====")


        hasDoStep = 0
        for oneStep in steps:
            hasDoStep+=1

            # if g_score < 2000 and hasDoStep > 6:
            #     return False
            # if hasDoStep > 10:
            #     return False

            step = None
            for stepT in oneStep:
                step = stepT
                break
            print("step:", step)
            if step == None:
                continue
            x = step[1]
            y = step[0]
            mouseX = X0 + eachH*x + fixH
            mouseY = Y0 + eachW * y + fixW
            print("click mouse ", mouseX, mouseY)

            # MouseEvent.mouse_click(mouseX, mouseY)
            # sleep(0.05)
            # MouseEvent.mouse_click(mouseX, mouseY)
            # sleep(0.1)
            # MouseEvent.mouse_click(mouseX, mouseY)
            retXYList.append([mouseX, mouseY])

            if len(oneStep) > 6:
                print("delete too long ...")
                # sleep(1.4)
        print("finish ")
        return retXYList

application = tornado.web.Application([
    (r"/", MainHandler),
    ("/play_game", PlayHandler)
])

if __name__ == "__main__":
    application.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
