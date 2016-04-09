# !/usr/bin/env python
# -*- coding: gb2312 -*-
#code from http://bbs.csdn.net/topics/390145455
import datetime, sys

import image2arr
from config import imageDir

ENUM_0 = ''
ENUM_1 = "1"
ENUM_2 = "2"
ENUM_3 = "3"
ENUM_4 = "4"
ENUM_5 = "5"

global global_cur_max_score, global_cur_max_routine, global_target_score
global_target_score = 99999999
global_cur_max_score = 0
global_cur_max_routine = []
global_start_time = 0
global_cost_time_disired = 120  # 你可以忍受的默认时间120S
# 从底行到头行输入
input = [
    ['Hua', 'Lan', 'Hua', 'Lan', 'Hua', 'Hua', 'Lan', 'Lv ', 'Hon', 'Hon'],
    ['Hua', 'Lv ', 'Lv ', 'Lv ', 'Fen', 'Lan', 'Hon', 'Lv ', 'Lan', 'Hua'],
    ['Fen', 'Lan', 'Fen', 'Lv ', 'Lv ', 'Lv ', 'Lan', 'Hua', 'Hua', 'Hua'],
    ['Fen', 'Lv ', 'Fen', 'Lan', 'Hua', 'Fen', 'Hon', 'Lan', 'Lv ', 'Lan'],
    ['Lv ', 'Lv ', 'Lan', 'Fen', 'Lan', 'Lan', 'Lan', 'Lan', 'Fen', 'Fen'],
    ['Hua', 'Lv ', 'Lv ', 'Lan', 'Hua', 'Lan', 'Fen', 'Lv ', 'Lv ', 'Lan'],
    ['Lan', 'Lan', 'Fen', 'Lv ', 'Hon', 'Hua', 'Lan', 'Hon', 'Lv ', 'Lan'],
    ['Hon', 'Lv ', 'Lv ', 'Hon', 'Hua', 'Lan', 'Lv ', 'Fen', 'Hua', 'Hon'],
    ['Hon', 'Hua', 'Hua', 'Fen', 'Lv ', 'Hon', 'Hon', 'Hon', 'Lan', 'Lan'],
    ['Fen', 'Hua', 'Hon', 'Hua', 'Hon', 'Fen', 'Lan', 'Fen', 'Hua', 'Hua'],
]


# 从底行到头行输入
# input = [
# ['Hua','Lan','Hua','Lan','Hua','Hua'],
# ['Hua','Lv ','Lv ','Lv ','Fen','Lan'],
# ['Fen','Lan','Fen','Lv ','Lv ','Lv '],
# ['Fen','Lv ','Fen','Lan','Hua','Fen'],
# ['Lv ','Lv ','Lan','Fen','Lan','Lan'],
# ['Hua','Lv ','Lv ','Lan','Hua','Lan'],
# ]

def copyinput(input, target=None):
    if (target == None):
        new_input = []
        for line in input:
            new_input.append(line[:])
        return new_input
    else:
        for x in range(len(input[0])):
            for y in range(len(input)):
                target[x][y] = input[x][y]


def getNotBlankCount(input_data):
    temp_map = {}
    for x in range(len(input_data[0])):
        for y in range(len(input_data)):
            if (input_data[x][y] <> ENUM_0):
                if (not temp_map.has_key(input_data[x][y])):
                    temp_map[input_data[x][y]] = 0
                temp_map[input_data[x][y]] += 1
    temp_list = temp_map.values()
    count = sum(temp_list)
    max_item_count = max(temp_list)
    return (count, max_item_count)


# 获得一个点所有的联通点。
# 返回set()为没有，返回set((x,y))为只有自己，否则返回set((x,y),(m,n),...)
def getDotLiantong(x, y, input_data):  # x,y= line,col
    if (input_data[x][y] == ENUM_0):
        return set()
    toSelDots = set()
    toSelDots.add((x, y))
    seledDots = set()
    while (len(toSelDots) > 0):
        (curDotx, curDoty) = toSelDots.pop()
        # print "(curDotx,curDoty)=(%d,%d)"%(curDotx,curDoty)
        if (curDotx - 1 >= 0 and input_data[curDotx - 1][curDoty] == input_data[curDotx][curDoty]):
            toSelDots.add((curDotx - 1, curDoty))
        if (curDotx + 1 < len(input_data[0]) and input_data[curDotx + 1][curDoty] == input_data[curDotx][curDoty]):
            toSelDots.add((curDotx + 1, curDoty))
        if (curDoty - 1 >= 0 and input_data[curDotx][curDoty - 1] == input_data[curDotx][curDoty]):
            toSelDots.add((curDotx, curDoty - 1))
        if (curDoty + 1 < len(input_data) and input_data[curDotx][curDoty + 1] == input_data[curDotx][curDoty]):
            toSelDots.add((curDotx, curDoty + 1))
        seledDots.add((curDotx, curDoty))
        toSelDots = toSelDots - seledDots
    return seledDots


# 返回联通点集合
def getWholeLiantong(input_data):
    seed = set()
    retList = []
    for x in range(len(input[0])):
        for y in range(len(input)):
            seed.add((x, y))
    while (len(seed) > 0):
        (dotx, doty) = seed.pop()
        dotLiantong = getDotLiantong(dotx, doty, input_data)
        seed = seed - dotLiantong
        if (len(dotLiantong) >= 2):  # 只有两个以上才可以被消掉
            retList.append(dotLiantong)
    return retList


def getScore(liantongset):
    dotCnt = len(liantongset)
    return ((dotCnt - 2) * 5 + 10) * dotCnt


def removeDot(curx, cury, input_data):
    for x in range(curx, len(input_data) - 1):
        input_data[x][cury] = input_data[x + 1][cury]
        if (input_data[x][cury] == ENUM_0):
            return;
    input_data[len(input_data) - 1][cury] = ENUM_0


def removeLiantongSet(liantongset, input_data):
    temp_list = list(liantongset)
    temp_list = sorted(temp_list, cmp=lambda item1, item2: cmp(item2[0], item1[0]))
    # print temp_list
    for x, y in temp_list:
        removeDot(x, y, input_data)


def filterBlankCol(input_data):
    firstCOlBlank = 0
    firstCOlNotBlank = 0
    while (firstCOlBlank < len(input_data[0]) and firstCOlNotBlank < len(input_data[0])):
        # 找到空列
        while (firstCOlBlank < len(input_data[0]) and input_data[0][firstCOlBlank] <> ENUM_0): firstCOlBlank += 1;
        if (firstCOlBlank >= len(input_data[0])): return;  # 没有空列
        # 找到空列后的第一个非空列
        firstCOlNotBlank = firstCOlBlank + 1
        while (firstCOlNotBlank < len(input_data[0]) and input_data[0][
            firstCOlNotBlank] == ENUM_0): firstCOlNotBlank += 1;
        if (firstCOlNotBlank >= len(input_data[0])): return;  # 后面全是空列
        # swap two cols
        for x in range(len(input_data)):
            input_data[x][firstCOlBlank] = input_data[x][firstCOlNotBlank]
            input_data[x][firstCOlNotBlank] = ENUM_0
        firstCOlBlank += 1
        firstCOlNotBlank += 1


def getPossibleScore(input_data):
    stat_map = {}
    for x in range(len(input_data[0])):
        for y in range(len(input_data)):
            if (not stat_map.has_key(input_data[x][y])):
                stat_map[input_data[x][y]] = set([])
            stat_map[input_data[x][y]].add((x, y))
    possible_score = 0
    for liantongset in stat_map.values():
        score = getScore(liantongset)
        possible_score += score
    return possible_score


# 没有考虑最后剩余10个以下的奖励分
def getMaxScore(score_until_now, input_data, routine_until_now):
    global global_cur_max_score, global_cur_max_routine, global_target_score
    if (score_until_now > global_cur_max_score):  # 目前最好路径，时间到时就输出这个
        global_cur_max_score = score_until_now
        global_cur_max_routine = routine_until_now[:]
    if (score_until_now > global_target_score):  # 已经有路径大于期望目标！立即输出
        print 'found routine whose socre is %d>%d: %s' % (score_until_now, global_target_score, routine_until_now)
        sys.exit(0)
    # if ((datetime.datetime.now() - global_start_time).seconds > global_cost_time_disired):
    #     print 'found routine whose socre is %d: %s' % (global_cur_max_score, global_cur_max_routine)
    #     sys.exit(0)
    count, max_item_count = getNotBlankCount(input_data)
    if (count < 21 or max_item_count < 11):  # 20个以下也得不了多少分了
        return (0, [])
    liantongSet_list = getWholeLiantong(input_data)
    if (len(liantongSet_list) == 0):
        return (0, [])

    max_liantongSet = []
    max_len = 0
    for liantongSet in liantongSet_list:
        if (len(liantongSet) > max_len):
            max_len = len(liantongSet)
            max_liantongSet = liantongSet
    if (max_len > len(input_data) * len(input_data[0]) / 4.0):  # 种子路径
        # print 'found seed routine'
        thisStepScore = getScore(max_liantongSet)  # 消掉一个联通点集合得分thisStepScore
        removeLiantongSet(max_liantongSet, input_data)  # 消掉一个联通点集合，得到新数据
        filterBlankCol(input_data)  # 左移，把空列去掉
        oneDot = max_liantongSet.pop()
        routine_until_now.append(oneDot)
        (nextStepsScore, routine_list) = getMaxScore(score_until_now + thisStepScore, input_data, routine_until_now)
        routine_until_now.pop()
        total_score = thisStepScore + nextStepsScore
        total_routine_list = []
        total_routine_list.append(oneDot)
        total_routine_list.extend(routine_list)
        return (total_score, total_routine_list)
    input_copy = copyinput(input_data)  # input_copy为原来的数据
    geZhongRoutine_list = []
    for liantongSet in liantongSet_list:  # 各种消掉尝试
        thisStepScore = getScore(liantongSet)  # 消掉一个联通点集合得分thisStepScore
        removeLiantongSet(liantongSet, input_data)  # 消掉一个联通点集合，得到新数据
        filterBlankCol(input_data)  # 左移，把空列去掉
        # total_possible_score = untilnow_total_score+thisStepScore+getPossibleScore(input_data)
        # if(total_possible_score<global_cur_max_score):#这个分支不用走了
        # print '%d<%d'%(total_possible_score,global_cur_max_score)
        # copyinput(input_copy,input_data)#恢复原始数据，以备下次循环
        # continue;
        # (nextStepsScore,routine_list) = getMaxScore(untilnow_total_score+thisStepScore,input_data)
        oneDot = liantongSet.pop()
        routine_until_now.append(oneDot)
        (nextStepsScore, routine_list) = getMaxScore(score_until_now + thisStepScore, input_data, routine_until_now)
        routine_until_now.pop()
        total_score = thisStepScore + nextStepsScore
        total_routine_list = []
        # print 'oneDot=',oneDot
        # print 'routine_list=',routine_list
        total_routine_list.append(oneDot)
        total_routine_list.extend(routine_list)
        geZhongRoutine_list.append((total_score, total_routine_list))
        copyinput(input_copy, input_data)  # 恢复原始数据，以备下次循环
    # 选出本次最优方案
    # geZhongRoutine_list=sorted(geZhongRoutine_list,cmp=lambda item1,item2:cmp(item2[0],item1[0]))
    # return geZhongRoutine_list[0]
    temp_max_score = 0
    temp_routine_list = []
    for score, routine_list in geZhongRoutine_list:
        if (score > temp_max_score):
            temp_routine_list = routine_list
            temp_max_score = score
    return (temp_max_score, temp_routine_list)


def printInputData(input_data):
    for record in input_data:
        print record


def test(input_data, steps):
    total_socre = 0
    for x, y in steps:
        printInputData(input_data)
        liantongset = getDotLiantong(x, y, input_data)
        print 'to remove:', liantongset
        score = getScore(liantongset)
        total_socre += score
        print 'get score:%d, total score:%d' % (score, total_socre)
        removeLiantongSet(liantongset, input_data)
        filterBlankCol(input_data)


if __name__ == '__main__':
    print 'usage: %s target_score cost_time' % (sys.argv[0])
    # print getPossibleScore(input)
    global_start_time = datetime.datetime.now()
    if (len(sys.argv) > 1):
        global_target_score = int(sys.argv[1])
    if (len(sys.argv) > 2):
        global_cost_time_disired = int(sys.argv[2])

    status = image2arr.getStatusFromImage(imageDir + "core.png")
    print getMaxScore(0, status, [])
    endtime = datetime.datetime.now()
    print 'cost time:', (endtime - global_start_time).seconds
# steps = [(1, 2), (3, 0), (2, 0), (1, 2), (0, 5), (2, 5), (0, 1), (2, 0), (1, 3)]
# steps = [(1, 2), (3, 0), (2, 0), (1, 2), (2, 0), (0, 3), (1, 2)]
# steps =  [(5, 9), (0, 7), (3, 8), (3, 7), (3, 8), (6, 9), (6, 9), (1, 2), (8, 1), (3, 1), (7, 6), (0, 5), (2, 7), (1, 6), (1, 5), (0, 6), (1, 5), (0, 1), (3, 0), (5, 0), (3, 8), (3, 2), (3, 4), (0, 3), (1, 2), (0, 8), (0, 3)]
# test(input,steps)
