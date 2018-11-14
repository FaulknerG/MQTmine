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
    if i < w:
        loc = i * w_tuple
        for trans in dataSet:
            for item in trans:
                matrix[item][loc] = trans[item]
            loc += 1

    if i >= w:
        for trans in matrix:
            for col in range((w-1) * w_tuple):
                matrix[trans][col] = matrix[trans][col + w_tuple]
            for col in range(2, 2+ w_tuple):
                matrix[trans][-col] = 0
        j = w_tuple + 1
        for trans in dataSet:
            for item in trans:
                matrix[item][-j] = trans[item]
            j -= 1
        deleteOverTransInTree(i)

    freqItem = []
    for item in matrix:
        matrix[item][-1] = sum(matrix[item][0:-1])
        if matrix[item][-1] >= minSup:
            freqItem.append(item)

    if i >= w:
        deleteNFPNodeInTree(freqItem, tree)

    index = i * w_tuple -1
    for trans in dataSet:
        fpInTrans = []
        index += 1
        for item in trans:
            if item in freqItem:
                fpInTrans.append(item)
        if len(fpInTrans) > 0:
            orderedItems = sorted(fpInTrans)
            updateTree(orderedItems, tree, queue, index)


# 删除树中过时信息
def deleteOverTransInTree(i):
    for index in range((i-2)*w_tuple, (i-1)*w_tuple):
        nodename, node = queue[index]
        if node.children != {}:
            del queue[index]
            node.TID.remove(index)
        else:
            if len(node.TID) > 1:
                del queue[index]
                node.TID.remove(index)
            elif len(node.TID) == 1:
                nparent = node.parent
                nparentname = node.parent.name
                del node.parent.children[nodename]
                del queue[index]
                ascendDeleteFromTree(nparent, nparentname)


def ascendDeleteFromTree(node, nodename):
    if node.name != 'MQTtree':
        if len(node.TID) == 0 and len(node.children) == 0:
            nparent = node.parent
            nparentname = node.parent.name
            del node.parent.children[nodename]
            ascendDeleteFromTree(nparent, nparentname)


def deleteNFPNodeInTree(freqItem, intree):
    for nodename in intree.children.keys():
        node = intree.children[nodename]
        if node is None:
            return
        if nodename not in freqItem:
            if len(node.TID) >= 1:
                for index in node.TID:
                    queue[index] = [intree.name, intree]
                intree.TID = node.TID
            for cpykey in node.children.keys():
                intree.children[cpykey] = node.children[cpykey]
                node.children[cpykey].parent = intree
            del node.parent.children[nodename]
            deleteNFPNodeInTree(freqItem, intree)
        else:
            deleteNFPNodeInTree(freqItem, node)


def updateTree(items, inTree, inqueue, index):
    if items[0] not in inTree.children:
        inTree.children[items[0]] = MQTtree(items[0], inTree)
    if len(items) == 1:
        inTree.children[items[0]].TID.append(index)
        inqueue[index] = [items[0], inTree.children[items[0]]]
    else:
        updateTree(items[1::], inTree.children[items[0]], queue, index)


if __name__ == '__main__':
    dataSet, itemSet = createInitSet()
    matrix, tree, queue = initMQTdatas()

    for i in range(len(dataSet) / w_tuple):
        print '读取第 ', i+1, ' 批数据'
        data = dataSet[i * w_tuple : (i+1) * w_tuple]
        genDataStruct(data, i)
        print 'matrix: ', matrix
        print 'queue: ', queue
        tree.disp()









