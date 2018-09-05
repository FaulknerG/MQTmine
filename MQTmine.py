# -*- coding: utf-8 -*-

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
                {'a': 0.3, 'e': 0.8}
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


def mineTree(inTree, queue, matrix):
    pass


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

    freqItems = []
    mineTree(tree, queue, matrix)

