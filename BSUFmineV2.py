# -*- coding: utf-8 -*-

# 12-21 ver:2.0

import copy
import random
import time
import LoadData
import Combine



class MQTtree:
    def __init__(self, nameValue, parentNode):
        self.name = nameValue
        self.TID = []
        self.parent = parentNode
        self.children = {}

    def disp(self, ind=1):
        print '  '*ind, self.name, ' ', self.TID
        for child in self.children.values():
            child.disp(ind+1)


def initMQTdatas():
    matrix = {}
    for i in itemSet:
        matrix[i] = [0] * (w * w_tuple + 1)
    tree = MQTtree('MQTtree', None)
    queue = {}
    return matrix, tree, queue


def genDataStruct(dataSet, i):
    # 写入 matrix
    # 窗口未满的情况，直接写入。根据批次确定写入的位置
    if i < w:
        # i 决定写入矩阵的位置,也就是列。dataSet -> matrix
        loc = i * w_tuple
        for trans in dataSet:
            for item in trans:
                matrix[item][loc] = trans[item]
            loc += 1

    # 若窗口已满，需要删除旧事务
    if i >= w:
        # 矩阵左移 w_tuple 列
        for trans in matrix:
            # range: 0 -- 2
            for col in range((w-1) * w_tuple):
                matrix[trans][col] = matrix[trans][col + w_tuple]
        # 矩阵后 w_tuple 排清0
        for trans in matrix:
            # range: -4 -- -2
            for col in range(2, 2 + w_tuple):
                matrix[trans][-col] = 0
        # 数据写入后面的列
        j = w_tuple + 1  # 4 3 2
        for trans in dataSet:
            for item in trans:
                matrix[item][-j] = trans[item]
            j -= 1
        # 删除树和队列中的过时信息
        deleteOverTransInTree(i)

    freqItem = []
    # 矩阵最后一列为期望支持度
    for trans in dataSet:
        for item in trans:
            matrix[item][-1] = sum(matrix[item][0:-1])
    for item in matrix.keys():
        if matrix[item][-1] >= minSup:
            freqItem.append(item)

    # 输出1-频繁项集
    print '1-Frequent Pattern', freqItem

    # print matrix, freqItem
    # 对树中剪枝非频繁项集
    if i >= w:
        deleteNFPNodeInTree(freqItem, tree)


    # 构建树
    index = i * w_tuple - 1
    for trans in dataSet:
        # 获取当前事务的频繁项集，并更新树结构
        Item_unInsertInTree = []
        index += 1
        # 转换为一个 list
        for item in trans:
            Item_unInsertInTree.append(item)
        # 字典排序后插入树中
        orderedItems = sorted(Item_unInsertInTree)
        updateTree(orderedItems, tree, queue, index)


# 删除树中过时信息
def deleteOverTransInTree(i):
    for index in range((i-w) * w_tuple, (i-w+1) * w_tuple):
        nodename, node = queue[index]
        if nodename == 'MQTtree':
            del queue[index]
            node.TID.remove(index)
        elif node.children != {}:  # 若不是叶子节点，直接删除 TID 标示即可
            del queue[index]
            node.TID.remove(index)
        else:
            # 是叶子节点，判断 TID 是否唯一
            if len(node.TID) > 1:
                # TID 不唯一，只需删除队列中的项，以及树中该节点中的 TID 标示
                del queue[index]
                node.TID.remove(index)
            elif len(node.TID) == 1:
                # 沿着该节点向上搜索，删除不含TID的节点
                nparent = node.parent
                nparentname = nparent.name
                for children in node.children.keys():
                    children.parent = nparent
                if nodename in node.parent.children.keys():
                    del node.parent.children[nodename]
                del queue[index]
                ascendDeleteFromTree(node.parent, nparentname)
                del node


def ascendDeleteFromTree(node, nodename):
    if node.name != 'MQTtree':
        if len(node.TID) == 0 and len(node.children) == 0:
            # 只有树中节点只有一个孩子
            nparent = node.parent
            nparentname = node.parent.name
            for children in node.children.keys():
                children.parent = nparent
            if nodename in node.parent.children.keys():
                del node.parent.children[nodename]
            ascendDeleteFromTree(nparent, nparentname)


# 剪枝树中非频繁项目
# 从上到下遍历树中的节点，删除不在频繁项集中的节点。
# 如果该节点不是末项频繁项集，则直接删除。将孩子节与自己父节点链接。
# 如果该节点是末项，则应将该节点的 TID 标示上传给父节点，并更新 queue 中数据
# 删除该节点的空间。
def deleteNFPNodeInTree(freqItem, intree):
    if len(intree.children) == 0:
        return
    for nodename in intree.children.keys():
        node = intree.children[nodename]
        if nodename not in freqItem:
            # 末项频繁项集，TID 上传
            if len(node.TID) >= 1:
                for index in node.TID:
                    queue[index] = [intree.name, intree]
                    intree.TID.append(index)

            deleteNFPNodeInTree(freqItem, node)

            # 孩子节点与父节点链接
            for cpykey in node.children.keys():
                intree.children[cpykey] = node.children[cpykey]
                node.children[cpykey].parent = intree
            # 扫描删除节点的孩子节点。
            del node.parent.children[nodename]
        # 否则继续向下扫描孩子节点
        else:
            deleteNFPNodeInTree(freqItem, node)


# 更新树的函数，递归的过程，每个函数只处理 item 的第一个值
def updateTree(items, inTree, inqueue, index):
    # 若无此节点，则建立一个
    if items[0] not in inTree.children:
        inTree.children[items[0]] = MQTtree(items[0], inTree)
    # 判断是否为末项频繁项集，若是，加入到 queue 中
    if len(items) == 1:
        inTree.children[items[0]].TID.append(index)
        inqueue[index] = [items[0], inTree.children[items[0]]]
    else:
        updateTree(items[1::], inTree.children[items[0]], queue, index)

def minetest(mine_i):
    freqItems = []  # 存储频繁项集
    ExSupport = {}  # 各项集 与 期望支持度 的字典
    NotFPI = []     # 非频繁项
    handledRoute = []  # 已经处理过的矩阵列
    for index in queue.keys():
        if index in handledRoute:       # 如果该 TID 路径已经计算过，则无需重复计算
            continue
        route = []       # 当前路径
        node = queue[index][1]
        needCalCol = []  # 需要计算的矩阵列
        for handledTID in node.TID:
            # handledTID --> matrix_col
            needCalCol.append(handledTID - ((mine_i-w+1) if mine_i >= w else 0) * w_tuple)  # 当前需要处理的矩阵列，通过 TID 号映射到矩阵到列号
            handledRoute.append(handledTID)
        findroute(node, route)

        stopLoopFlag = False        # 停止循环标识位，暂未实现功能。
        for k in range(2, 5 if 5 < len(route) else 1+len(route)):
            # print k, ' combine',
            # if stopLoopFlag:
            #     break
            k_itemCombined = Combine.generatekitems(route, k)   # 根据路径与 k 生成组合，然后对其遍历
            k_itemCombined = k_itemCombined[0:-1]
            # print 'OK, Callen=',

            for item in k_itemCombined:
                real_item = []      # 该组合项集的列表
                item_hash = ''      # hash 编码，唯一表示该组合项集路径
                for num in item:
                    item_hash += route[num - 1]
                    real_item.append(route[num-1])
                # if hasNotFPIset(item_hash, NotFPI):     # 如果该组合项集有子集是非频繁项集，则无需对其进一步计算
                    # continue
                if item_hash not in ExSupport.keys():
                    ExSupport[item_hash] = 0
                ExSupport[item_hash] += caluExSpuuort(real_item, needCalCol)    # 计算支持度
            # for item_h in ExSupport.keys():
            #     if ExSupport[item_h] < minSup:
            #         NotFPI.append(item_hash)

            # print 'OK.'
    # 所有 TID 遍历完
    # 筛选频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    if len(freqItems) >= 1:
        print freqItems


def hasNotFPIset(NowI, NotFPI):
    # NotFPI 中是否有 NowI 的子集
    for NI in set(NotFPI):   # [1,4]
        # if set(NI).issubset(NowI):
        if NI in NowI:
            return True
    return False


def caluExSpuuort(route, needCalTID):
    Sumresult = 0
    for matrix_col in needCalTID:
        result = 1
        for i in route:
            if matrix_col < 0:
                print matrix_col, 'error'
            Multiplier = matrix[i][matrix_col]
            if Multiplier != 0:
                result *= Multiplier
        Sumresult += result
    if Sumresult == len(needCalTID):
        return 0
    else:
        return Sumresult


def findroute(node, route):
    if node.name != 'MQTtree':
        route.append(node.name)
        findroute(node.parent, route)


if __name__ == '__main__':

    w = 4  # 窗口数量  4 * 37
    w_tuple = 40  # 每个窗口包含 3 条元组
    siga = 0.005
    minSup = w * w_tuple * siga # 160 * 0.01 = 1.6

    time_start = time.time()
    dataSet, itemSet = LoadData.loadIBMDataSet()
    # dataSet, itemSet = LoadData.loadConnectData()
    # dataSet, itemSet = LoadData.loadSimpleData()
    # 初始化数据结构
    matrix, tree, queue = initMQTdatas()

    # costTime = 0
    # 开始读取数据流
    # for i in range(len(dataSet)/w_tuple):
    for i in range(10):
        # if i % 100 == 0:
        print i
        # 截取数据
        data = dataSet[i * w_tuple:(i+1) * w_tuple]
        # 构造数据结构
        genDataStruct(data, i)

        # print 'matrix: ', matrix
        # print 'queue: ', queue
        # tree.disp()

        # print '开始挖掘'
        # mineTree()


        minetest(i)

    time_end = time.time()
        # costTime += (time_end - time_start)
    # print 'final cost time for mine: ',costTime,' s'
    print time_end - time_start


