# -*- coding: utf-8 -*-

# import pythoncom, pyHook
import pyHook
import pythoncom
import time


def OnMouseEvent(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Position:',event.Position
    print 'Wheel:',event.Wheel
    print 'Injected:',event.Injected
    print '---'

    # 返回 True 可将事件传给其它处理程序，否则停止传播事件
    return True

def test_hook():
    # 创建钩子管理对象
    hm = pyHook.HookManager()
    # 监听所有鼠标事件
    hm.MouseAll = OnMouseEvent # 等效于hm.SubscribeMouseAll(OnMouseEvent)
    # 开始监听鼠标事件
    hm.HookMouse()
    # 一直监听，直到手动退出程序
    pythoncom.PumpMessages()

def doMouseClick(x, y):
    import win32api, win32con, windll
    windll.user32.SetCursorPos(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


if __name__ == '__main__':
    test_hook()
    doMouseClick(316, 97)