# coding=utf-8
from copy import deepcopy
from time import sleep, time

import image2arr
from config import imageDir, corefileDir
from popstar_solver import popstars

ENUM_0 = ''

#剩余BONUS的公式为2000-20*(N^2)，N为剩余的块数，N<10（N>=10后BONUS为0）
def getEndScore(status):
    resCount = 0
    ret = 0
    for line in status:
        for one in line:
            if one != ENUM_0:
                resCount += 1
    if resCount < 10:
        return 2000 - 20*(resCount*resCount)
    return 0

# 获得一个点所有的联通点。
# 返回set()为没有，返回set((x,y))为只有自己，否则返回set((x,y),(m,n),...)
def getDotLiantong(x, y, input_data):  # x,y= line,col
    try:
        if (input_data[x][y] == ENUM_0):
            return set()
    except Exception as e:
        print("getDotliantong ", x, y, input_data)
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
    for x in range(len(input_data[0])):
        for y in range(len(input_data)):
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

def getAllLiantongSetScore(liantongSet):
    sumS = 0
    for s in liantongSet:
        sumS += getScore(s)
    return sumS

def getBestNext(node):
    #ret  stepset nextStatus
    liangtongSet = getWholeLiantong(node.status)
    if len(liangtongSet) == 0:
        return set(), deepcopy(node.status), 0
    resultLst = []
    for oneLs in liangtongSet:
        oneScore = getScore(oneLs)
        nextStatus = node.calc_new_status_withFix(oneLs)
        nextLiantongSet = getWholeLiantong(nextStatus)
        nextScore = getAllLiantongSetScore(nextLiantongSet)
        totalScore = oneScore + nextScore
        resultLst.append([totalScore, oneLs, oneScore, nextStatus])
    resultLst = sorted(resultLst, key=lambda x:x[0], reverse=True)
    bestStep = resultLst[0]
    return bestStep[1], bestStep[3], bestStep[0]

gStep = []

def doPopStars1(node, preScore, deepFlag=True):
    resultLst = []
    liantongSet = getWholeLiantong(node.status)
    if len(liantongSet) == 0:
        return getEndScore(node.status)
    for oneLs in liantongSet:
        oneScore = getScore(oneLs)
        nextStatus = node.calc_new_status_withFix(oneLs)
        nextStep1, nextStatus1, allsore = getBestNext(popstars.PopstarsNode(nextStatus))
        oneScore1 = getScore(nextStep1)
        nextScore = getAllLiantongSetScore(getWholeLiantong(nextStatus1))
        totalScore = oneScore + oneScore1 + nextScore
        if deepFlag:
            resultLst.append([totalScore, oneLs, oneScore, nextStep1, nextStatus1])
        else:
            resultLst.append([totalScore, oneLs, oneScore, nextStep1, nextStatus])
    resultLst = sorted(resultLst, key=lambda x:x[0], reverse=True)
    bestNext = resultLst[0]

    cmpLst = []
    if len(resultLst) > 1:
        for i in range(1, len(resultLst)-1):
            if resultLst[i][0] == bestNext[0]:
                # lst0 = sorted(resultLst[i][1], key=lambda x:x[1], reverse=True)[0]
                # lst1 = sorted(bestNext[1], key=lambda x:x[1],reverse=True)[0]
                # if lst0[1] > lst1[1]:
                #     bestNext = resultLst[i]
                steps, nstatus, totalScore  = getBestNext(popstars.PopstarsNode(resultLst[i][4]))
                cmpLst.append([resultLst[i], totalScore])
    if len(cmpLst) != 0:
        steps, nstatus, totalScore = getBestNext(popstars.PopstarsNode(bestNext[4]))
        cmpLst.append([bestNext, totalScore])
        bestNext = sorted(cmpLst, key=lambda x:x[1], reverse=True)[0][0]



    print(bestNext)
    for w in bestNext[4]:
        print(w)
    print("score ", bestNext[2]+preScore)
    gStep.append(bestNext[1])
    if deepFlag:
        gStep.append(bestNext[3])
    return bestNext[2] + doPopStars1(popstars.PopstarsNode(bestNext[4]), preScore + bestNext[2], deepFlag)


def doPopStars(node, preScore):
    resultLst = []
    liantongSet = getWholeLiantong(node.status)
    if len(liantongSet) == 0:
        endScore =  getEndScore(node.status)
        return endScore
    for oneLs in liantongSet:
        oneScore = getScore(oneLs)
        nextStatus = node.calc_new_status_withFix(oneLs)
        nextLiantongSet = getWholeLiantong(nextStatus)
        nextScore = getAllLiantongSetScore(nextLiantongSet)
        totalScore = oneScore + nextScore
        resultLst.append([totalScore, oneLs, oneScore])
    resultLst = sorted(resultLst, key=lambda x:x[0], reverse=True)
    # print(resultLst)
    bestStep = resultLst[0]
    # if len(resultLst) > 1:
    #     for i in range(1, len(resultLst)-1):
    #         if resultLst[i][0] == bestStep[0]:
    #             lst0 = sorted(resultLst[i][1], key=lambda x:x[1], reverse=True)[0]
    #             lst1 = sorted(bestStep[1], key=lambda x:x[1],reverse=True)[0]
    #             if lst0[1] > lst1[1]:
    #                 bestStep = resultLst[i]

    print(bestStep)
    score = bestStep[2]
    print("has score", preScore+bestStep[2])
    nextStatus = node.calc_new_status_withFix(bestStep[1])

    for line in nextStatus:
        print(line)
    gStep.append(bestStep[1])
    nextnode = popstars.PopstarsNode(nextStatus)
    return bestStep[2] + doPopStars(nextnode, score+preScore)


def __doLessSolv(hasScore, hasDosSteps, status):
    resultLst = []
    node = popstars.PopstarsNode(status)
    liantongSet = getWholeLiantong(status)
    # print("liantongSet", len(liantongSet), status)
    if len(liantongSet) == 0:
        return hasScore + getEndScore(status), hasDosSteps
    for liantong in liantongSet:
        score = getScore(liantong)
        nextStatus = node.calc_new_status_withFix(liantong)
        nexthasDosSteps = deepcopy(hasDosSteps)
        nexthasDosSteps.append(liantong)
        maxScore, steps  = __doLessSolv(hasScore+score, nexthasDosSteps,  nextStatus)
        resultLst.append([maxScore, steps])
        # break
    resultLst = sorted(resultLst, key=lambda x:x[0], reverse=True)
    bestRes = resultLst[0]
    return bestRes[0], bestRes[1]

def doLessSolv():
    status = image2arr.getStatusFromImage(imageDir + "core.png")

    popScore, steps = __createStep(status)
    print("doPop score", popScore)

    f = open(corefileDir + "step.txt", "w")
    f.write(str(steps))
    f.close()
    f = open(corefileDir + "score.txt", "w")
    f.write(str(popScore))
    f.close()
    score = 0
    nextStatus = status
    hasDosSteps = []
    count = len(steps)
    for step in steps:
        if count < 6:
            break
        count -= 1
        score += getScore(step)
        nextStatus = popstars.PopstarsNode(nextStatus).calc_new_status_withFix(step)
        hasDosSteps.append(step)
    print("doLessSolv has", score, nextStatus)

    ret = __doLessSolv(score, hasDosSteps, nextStatus)
    print(ret)
    lessSolvScore = ret[0]
    lessSolvSteps = ret[1]
    print("doLessSolv score", lessSolvScore)
    print("doPop score", popScore)
    if lessSolvScore > popScore:
        f = open(corefileDir + "step.txt", "w")
        f.write(str(lessSolvSteps))
        f.close()
        f = open(corefileDir + "score.txt", "w")
        f.write(str(lessSolvScore))
        f.close()
    return ret


def reverseStatus(status):
    new_status = []
    index = len(status) - 1
    while True:
        if (index < 0):
            break
        line = status[index]
        lineIndex = len(line) - 1
        new_line = []
        while True:
            if lineIndex < 0:
                break
            new_line.append(line[lineIndex])
            lineIndex -= 1
        new_status.append(new_line)
        index -= 1
    return new_status


def __createStep(status):

    global gStep
    #use onePopstarts solv
    # cellCount = 0
    # for line in status:
    #     for cell in line:
    #         if cell != ENUM_0:
    #             cellCount += 1
    # score = 0
    # scoreSteps = []
    # onePopstarsSteps = []
    # if cellCount < 0:
    #     print("using onePopstars.....")
    #     import onePopstars
    #     score, steps = onePopstars.getMaxScore(0, reverseStatus(status), [])
    #     onePopstarsSteps = steps
    #     for oneStep in steps:
    #         fixStep = (10-oneStep[0], 10-oneStep[1])
    #         gStep.append(set([fixStep]))
    #     print(score, gStep)
    #     f = open("step.txt", "w")
    #     f.write(str(gStep))
    #     f.close()
    #     scoreSteps = deepcopy(gStep)
    #     gStep = []
        # return

    node = popstars.PopstarsNode(status)
    ret = doPopStars(node, 0)
    score0 = ret
    score0Steps = deepcopy(gStep)
    gStep = []

    score1 = doPopStars1(node, 0)
    score1Steps = deepcopy(gStep)
    gStep = []

    score2 = doPopStars1(node, 0, deepFlag=False)
    score2Steps = deepcopy(gStep)
    gStep = []

    solvLst = [[score0, "score0", score0Steps],
               [score1, "deep search", score1Steps],
               [score2, "deep false search", score2Steps]]
    solvLst = sorted(solvLst, key=lambda x:x[0], reverse=True)

    bestSolve = solvLst[0]
    f = open(corefileDir + "step.txt", "w")
    f.write(str(bestSolve[2]))
    gStep = []
    f.close()

    f = open(corefileDir + "score.txt", "w")
    f.write(str(bestSolve[0]))
    f.close()

    for s in solvLst:
        print(s)

    return bestSolve[0], bestSolve[2]

def createStep():
    # doLessSolv()

    status = image2arr.getStatusFromImage(imageDir + "core.png")
    if True:
        return __createStep(status)

    # for test
    t0 = time()
    nextStatus = status
    AllScore = 0
    AllSteps = []
    SolveLst = []
    while True:
        score, steps = __createStep(nextStatus)
        SolveLst.append([score+AllScore, steps])
        ssScore = score+AllScore
        if len(steps) == 0:
            break
        LL = 4
        if score < 2000:
            LL = 2
        for onestep in steps[0:LL]:
            AllSteps.append(onestep)
            AllScore += getScore(onestep)
            nextStatus = popstars.PopstarsNode(nextStatus).calc_new_status_withFix(onestep)
        # if score> 4000:
        #     break
    AllScore += getEndScore(nextStatus)
    print("Allscore", AllScore, AllSteps)
    SolveLst.append([AllScore, AllSteps])
    SolveLst = sorted(SolveLst, key=lambda x:x[0], reverse=True)
    for solv in SolveLst:
        print(solv)

    sleep(1)
    BestSolv = SolveLst[0]

    f = open(corefileDir + "step.txt", "w")
    f.write(str(AllSteps))
    f.close()
    f = open(corefileDir + "score.txt", "w")
    f.write(str(BestSolv[0]))
    f.close()
    print("use time ", time()-t0)

def testSolve():
    status = image2arr.getStatusFromImage(imageDir + "core.png")

    node = popstars.PopstarsNode(status)
    solver = popstars.PopstarsSolver(node)
    score = solver.search()
    res  = solver.find_result()
    print(score)
    print(res)
    return score, res


if __name__ == '__main__':
    # doLessSolv()
    # testSolve()
    createStep()
