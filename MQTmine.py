# -*- coding: utf-8 -*-


"""
Ver 1.0
该版本已经实现了部分基本功能
1. 创建数据结构
2. 挖掘频繁项集
缺陷：
1. 当新的数据流到来，原来非频繁项集变为频繁项集，没有对原来的事务在树中做相应修改
思考后，应当不需要每次数据流来临时对树进行修改维护。
可以在数据流到达后，直接对新对矩阵建立新树。
这样可以将剪枝、更新树 合并为一个简单的操作，符合奥卡姆剃刀原则。

2. 挖掘频繁项集时，未能显示 1- 和 全项集。
未能根据 Apriori 原则剪枝不需要计算支持度的项集。
"""





import copy

# 全局变量
w = 2  # 窗口数量
w_tuple = 3  # 每个窗口包含 3 条元组
siga = 0.2
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
    retDict = [{'a': 0.9, 'd': 0.8, 'e': 0.7, 'f': 0.2},
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
    for trans in retDict:
        for item in trans:
            itemSet.append(item)
    itemSet = frozenset(itemSet)
    # frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    return retDict, itemSet


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
        # 矩阵后三排清0
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
    for item in matrix:
        matrix[item][-1] = sum(matrix[item][0:-1])
        if matrix[item][-1] >= minSup:
            freqItem.append(item)
    # print matrix, freqItem
    # 对树中剪枝非频繁项集
    if i >= w:
        deleteNFPNodeInTree(freqItem, tree)


    #
    index = i * w_tuple - 1
    for trans in dataSet:
        # 获取当前事务的频繁项集，并更新树结构
        fpInTrans = []
        index += 1
        for item in trans:
            if item in freqItem:
                fpInTrans.append(item)
        if len(fpInTrans) > 0:
            # 字典序排序
            orderedItems = sorted(fpInTrans)
            updateTree(orderedItems, tree, queue, index)


# 删除树中过时信息
def deleteOverTransInTree(i):
    for index in range((i-2) * w_tuple, (i-1) * w_tuple):
        nodename, node = queue[index]
        if node.children != {}:  # 若不是叶子节点，直接删除 TID 标示即可
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
                nparentname = node.parent.name
                del node.parent.children[nodename]
                del queue[index]
                ascendDeleteFromTree(nparent, nparentname)


def ascendDeleteFromTree(node, nodename):
    if node.name != 'MQTtree':
        if len(node.TID) == 0 and len(node.children) == 0:
            # 只有树中节点只有一个孩子
            nparent = node.parent
            nparentname = node.parent.name
            del node.parent.children[nodename]
            ascendDeleteFromTree(nparent, nparentname)


# 剪枝树中非频繁项目
# 从上到下遍历树中的节点，删除不在频繁项集中的节点。
# 如果该节点不是末项频繁项集，则直接删除。将孩子节与自己父节点链接。
# 如果该节点是末项，则应将该节点的 TID 标示上传给父节点，并更新 queue 中数据
# 删除该节点的空间。
def deleteNFPNodeInTree(freqItem, intree):
    for nodename in intree.children.keys():
        node = intree.children[nodename]
        if node is None:
            return
        if nodename not in freqItem:
            # 末项频繁项集，TID 上传
            if len(node.TID) >= 1:
                for index in node.TID:
                    queue[index] = [intree.name, intree]
                intree.TID = node.TID
            # 孩子节点与父节点链接
            for cpykey in node.children.keys():
                intree.children[cpykey] = node.children[cpykey]
                node.children[cpykey].parent = intree
            del node.parent.children[nodename]
            # 扫描删除节点的孩子节点。
            deleteNFPNodeInTree(freqItem, intree)
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


def mineTree():
    freqItems = []
    ExSupport = {}
    matrix_col = 0
    for index in queue.keys():
        route = []
        node = queue[index][1]
        findroute(node, route)
        print '路径： ', route
        # 先将 全路径 ，计算支持度，存入 ExSupport[route] 中
        route_item = ''
        for i in route:
            route_item += i
        ExSupport[route_item] = caluExSpuuort(route_item, matrix_col)  # matrix_col 控制计算时的TID号，对应矩阵中的每一列
        Allitems = generateallkitems(route)
        # print '产生全组合的序号', Allitems
        print '其项集组合为： '
        for item in Allitems:  # item: [1,2]
            temp_item = ''
            for num in item:    # num: 1
                temp_item += route[num-1]
            print temp_item
            if temp_item not in ExSupport.keys():
                ExSupport[temp_item] = 0
            ExSupport[temp_item] += caluExSpuuort(temp_item, matrix_col)
        matrix_col += 1

    print '期望支持度',ExSupport
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    # 加入 1- 项集
    for item in matrix.keys():
        if matrix[item][-1] >= minSup:
           pass
            # freqItems.append(item)

    print freqItems


# 计算期望支持度，对与String类型对项集，以及当前数据流在矩阵中的列号
def caluExSpuuort(str_item, TID):
    # 当前列中，对项目概率 累乘，返回结果
    # 首先要对字符串进行操作，取出其中对每一个项目。
    result = 1
    for i in range(len(str_item)):
        Multiplier = matrix[str_item[i]][TID]
        if Multiplier != 0:
            result *= Multiplier
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
    dataSet, itemSet = createInitSet()
    # itemSet = frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    # 初始化数据结构
    matrix, tree, queue = initMQTdatas()

    # 开始读取数据流
    for i in range(len(dataSet)/w_tuple):
        print '读取第 ', i+1, ' 批数据'
        # 截取数据
        data = dataSet[i * w_tuple:(i+1) * w_tuple]
        # 构造数据结构
        genDataStruct(data, i)
        print '读取成功'

        # print '第 ', i+1, ' 个窗口读取事务'
        print 'matrix: ', matrix
        print 'queue: ', queue
        tree.disp()

        # 进行挖掘
        mineTree()

