# -*- coding: utf-8 -*-

"""
BSUFmine
"""


import copy
import random
import time

# 全局变量
w = 4 # 窗口数量
w_tuple = 37  # 每个窗口包含 3 条元组
siga = 0.02
minSup = w * w_tuple * siga


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


def createInitSet():
    result = [{'a': 0.9, 'd': 0.8, 'e': 0.7, 'f': 0.2},
                {'a': 0.9, 'c': 0.7, 'd': 0.7, 'e': 0.6},
                {'b': 1.0, 'c': 0.9},

                {'b': 1.0, 'c': 0.9, 'd': 0.3},
                {'a': 0.9, 'd': 0.8},
                {'b': 1.0, 'd': 0.7, 'e': 0.1},

                {'a': 0.9, 'd': 0.8},
                {'b': 1.0, 'c': 0.9, 'd': 0.3},
                {'a': 0.9, 'd': 0.8, 'e': 0.7},

                {'d': 0.5, 'f': 0.7},
                {'d': 0.6, 'e': 0.5},
                {'a': 0.3, 'e': 0.8},

               {'a': 0.4, 'e': 0.2, 'c': 0.7, 'f': 0.6},
               {'a': 0.6, 'd': 0.5, 'e': 0.3, 'f': 0.3},
               {'e': 0.1, 'c': 0.7, 'f': 0.5}
                ]
    itemSet = []
    for trans in result:
        for item in trans:
            itemSet.append(item)
    itemSet = frozenset(itemSet)
    # frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    return result, itemSet


def loadDataSet():
    fo = open("/Users/Faulkner/PycharmProjects/MLinActionCode/MQTmine/T10I4D100K.txt", 'r')
    result = []
    for line in fo.readlines():
        trans = line.strip().split(' ')
        retDict = {}
        for i in trans:
            # retDict[i] = random.random()
            retDict[i] = 0.5
        result.append(retDict)
    itemSet = []
    for trans in result:
        for item in trans:
            itemSet.append(item)
    itemSet = frozenset(itemSet)
    return result, itemSet


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

    # # print matrix, freqItem
    # # 对树中剪枝非频繁项集
    # if i >= w:
    #     deleteNFPNodeInTree(freqItem, tree)


    # 构建树
    index = i * w_tuple - 1
    for trans in dataSet:
        # 获取当前事务的频繁项集，并更新树结构
        fpInTrans = []
        index += 1
        for item in trans:
            if item in freqItem:
                fpInTrans.append(item)
        if len(fpInTrans) == 0:
            tree.TID.append(index)
            queue[index] = [tree.name, tree]
        elif len(fpInTrans) > 0:
            # 字典序排序
            orderedItems = sorted(fpInTrans)
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


def mineTree():
    freqItems = []
    ExSupport = {}
    index_route = {}
    matrix_col = 0
    for index in queue.keys():
        route = []
        node = queue[index][1]
        findroute(node, route)
        # 将路径映射为一个序号：route_hash , 存入字典 index_route 中，以便以后查阅
        # 先将 全路径 ，计算支持度，存入 ExSupport[route_index] 中
        route_hash = ''
        for i in route:
            route_hash += i
        index_route[route_hash] = route
        if route_hash not in ExSupport.keys():
            ExSupport[route_hash] = 0
        ExSupport[route_hash] += caluExSpuuort(route, matrix_col)  # matrix_col 控制计算时的TID号，对应矩阵中的每一列

        Allitems = generateallkitems(route)
        # print '产生全组合的序号', Allitems
        # print '其项集组合为： '
        for item in Allitems:  # item: [1,2]
            temp_item = []
            temp_item_hash = ''
            for num in item:  # num: 1
                temp_item.append(route[num - 1])
            # print temp_item
            for j in temp_item:
                temp_item_hash += j
            if temp_item_hash not in ExSupport.keys():
                ExSupport[temp_item_hash] = 0
            ExSupport[temp_item_hash] += caluExSpuuort(temp_item, matrix_col)
        matrix_col += 1

    # print '期望支持度',ExSupport
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    # 加入 1- 项集
    for item in matrix.keys():
        if matrix[item][-1] >= minSup:
            freqItems.append(item)

    # print '频繁项集为：', freqItems


def caluExSpuuort(route, matrix_col):
    result = 1
    for i in route:
        Multiplier = matrix[i][matrix_col]
        if Multiplier != 0:
            result *= Multiplier
    if result == 1:
        return 0
    else:
        return result


def findroute(node, route):
    if node.name != 'MQTtree':
        route.append(node.name)
        findroute(node.parent, route)


def generateCom(m, n, retitems, Allitems):
    if n is 0:
        Allitems.append(copy.copy(retitems))
        return
    for i in range(m, n-1, -1):
        retitems[n-1] = i
        generateCom(i-1, n-1, retitems, Allitems)


def generateallkitems(route):
    Allitems = []
    # 产生所有的组合，这里用到组合数
    m = len(route)
    Allitems.append(range(1, m+1))

    if m == 2:
        return [[1, 2]]
    retitem = [-1] * m
    for n in range(2, m):
        retitem[n] = []
        for i in range(n):
            retitem[n].append(0)
        generateCom(m, n, retitem[n], Allitems)
    return Allitems


if __name__ == '__main__':
    # dataSet, itemSet = createInitSet()
    dataSet, itemSet = loadDataSet()
    # itemSet = frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    # 初始化数据结构
    matrix, tree, queue = initMQTdatas()

    time_start = time.time()
    # 开始读取数据流
    for i in range(len(dataSet)/w_tuple):
        # if i % 100 == 0:
        #     print i
        # 截取数据
        data = dataSet[i * w_tuple:(i+1) * w_tuple]
        # 构造数据结构
        genDataStruct(data, i)
        # print '读取成功'

        # print 'matrix: ', matrix
        # print 'queue: ', queue
        # tree.disp()

        # 进行挖掘
        # print '开始挖掘'
        mineTree()

    time_end = time.time()
    print time_end - time_start, 's'

