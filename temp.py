# -*- coding: utf-8 -*-
# 读取txt文本， 数据预处理
# import random


# # [Error] 141 行
# # 矩阵最后一列
# for item in matrix.keys():
#     matrix[item][-1] = sum(matrix[item][0:-1])
#     if matrix[item][-1] >= minSup:
#         freqItem.append(item)
#
#
#         # [Error]144 line
#         if matrix[item][-1] >= minSup and item not in freqItem:
# # [Error] 294 line
#     for trans in dataSet:
#         for item in trans:
#             if matrix[item][-1] >= minSup and item not in freqItems:
#                 freqItems.append(item)
#
# # [OK] 316 line
# def caluExSpuuort(route, matrix_col):
#
#     result = 1
#     for i in route:
#         Multiplier = matrix[i][matrix_col]
#         if Multiplier != 0:
#             result *= Multiplier
#     if result == 1:
#         return 0
#     else:
#         return result
# 两种方案：
# 1 代码206--210 删除结点时直接删除该节点的引用
# 2 判断是否父节点已失去对子节点的链接。



# class MQTtree:
#     def __init__(self, nameValue, parentNode):
#         self.name = nameValue
#         self.TID = []
#         self.parent = parentNode
#         self.children = {}
#
#     def disp(self, ind=1):
#         print '  '*ind, self.name, ' ', self.TID
#         for child in self.children.values():
#             child.disp(ind+1)
#
#
# tree = MQTtree('MQTtree',None)
# tree.children['829'] = MQTtree('829', tree)
#
# node = tree.children['829']
# node.TID = [1,2,3]
#
# del node  # 这种删除方法并不会删除 tree 中的 node 结点
# # del node.parent.children[node.name]  # 这种删除方法可以改变 tree
#
# tree.disp()


import psutil
import os


# info = psutil.virtual_memory()
# print u'内存使用：',psutil.Process(os.getpid()).memory_info().rss
# print u'总内存：',info.total
# print u'内存占比：',info.percent
# print u'cpu个数：',psutil.cpu_count()



"""
195 批次出现 KeyError 错误
代码在 234 line
请加条状态监控语句查看错误信息

错误原因：
node 的父亲的子节点没有 node
但是 node 的父节点链接存在
说明删除的时候仅从父节点向下删除，子节点没有删除对父节点的链接
即，有时父节点会失效。失效会导致什么后果？影响挖掘吗？

应该是有影响的，这是一个类似双向链表的数据结构。
在删除等操作时要注意双向操作
"""

# python -m memory_profiler aa.py



"""
1。其实只要产生4项集的组合就够了，5项集及以上都不会有频繁项集了，故可以节省大量时间
2。产生项集时间消耗远小于对项集对判断和计算。
"""

def minetest():
    freqItems = []
    ExSupport = {}
    index_route = {}
    matrix_col = 0
    NotFPI = []  # 非频繁项集列表，即剪枝掉的项集，不需计算该项集的拓展项集
    # length1 = []
    for index in queue.keys():
        print '队列 ',index
        route = []
        node = queue[index][1]
        findroute(node, route)
        print '当前路径长度', len(route)
        # length1.append(len(route))
    # print max(length1)
        # 组合一组一组的产生
        # 产生一组后，对下一组起到剪枝作用. '12' in '123' == True
        for k in range(2,len(route)):
            print '产生 ',k,' 项集',
            k_itemCombined = Combine.generatekitems(route, k)
            print '  --OK'
            for item in k_itemCombined:
                temp_item = []
                temp_item_hash = ''
                for num in item:
                    temp_item.append(route[num - 1])
                    temp_item_hash += route[num - 1]
                NeedCalSup_flag = True  # 需要计算的标志位。如果该项包含非频繁项，则该标志位赋False
                for NFP in NotFPI:
                    if NFP in temp_item_hash:
                        NeedCalSup_flag = False
                if NeedCalSup_flag:
                    if temp_item_hash not in ExSupport.keys():
                        ExSupport[temp_item_hash] = 0
                    ExSupport[temp_item_hash] += caluExSpuuort(temp_item, matrix_col)
                    if ExSupport[temp_item_hash] < minSup:
                        NotFPI.append(temp_item_hash)
            print '非频繁项集 NFP： ',NotFPI
        matrix_col += 1

    # 树按照队列索引完毕，下一步保存频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    print '频繁项集为：', freqItems


# ----------
# 10-11 v1.1
# ----------
def minetest():
    freqItems = []
    ExSupport = {}
    NotFPI = []
    handledRoute = []  # 已经处理过的矩阵列
    for index in queue.keys():
        if index in handledRoute:
            continue
        route = []
        node = queue[index][1]
        needCalTID = []
        for handledTID in node.TID:
            needCalTID.append(handledTID)  # 当前需要处理的矩阵列
            handledRoute.append(handledTID)
        findroute(node, route)

        stopLoopFlag = False
        for k in range(2, 5):
            if stopLoopFlag:
                break
            k_itemCombined = Combine.generatekitems(route, k)

            for item in k_itemCombined:
                real_item = []
                item_hash = ''
                for num in item:
                    real_item.append(route[num-1])
                    item_hash += route[num-1]
                if item_hash not in ExSupport.keys():
                    ExSupport[item_hash] = 0
                ExSupport[item_hash] += caluExSpuuort(temp_item, needCalTID)
                """
                此处：
                需要修改 caluExSpuuort 函数，当传入的参数，即 matrix_col 有多个时，要多个处理
                """
    # 所有 TID 遍历完
    # 筛选频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    print '频繁项集为：', freqItems


def caluExSpuuort(route, needCalTID):
    result = 1
    Sumresult = 0
    for matrix_col in needCalTID:
        for i in route:
            Multiplier = matrix[i][matrix_col]
            if Multiplier != 0:
                result *= Multiplier
        Sumresult += result
    if Sumresult == len(needCalTID):
        return 0
    else:
        return Sumresult



# ----------
# 10-11 v1.0
# ----------
def minetest():
    freqItems = []
    ExSupport = {}
    index_route = {}
    matrix_col = 0
    NotFPI = []  # 非频繁项集列表，即剪枝掉的项集，不需计算该项集的拓展项集
    # length1 = []
    for index in queue.keys():
        print '队列 ',index
        route = []
        node = queue[index][1]
        findroute(node, route)
        print '当前路径长度', len(route)
        # length1.append(len(route))
    # print max(length1)
        # 组合一组一组的产生
        # 产生一组后，对下一组起到剪枝作用. '12' in '123' == True
        for k in range(2,len(route)):
            print '产生 ',k,' 项集',
            k_itemCombined = Combine.generatekitems(route, k)
            print '  --OK'
            for item in k_itemCombined:
                temp_item = []
                temp_item_hash = ''
                for num in item:
                    temp_item.append(route[num - 1])
                    temp_item_hash += route[num - 1]
                NeedCalSup_flag = True  # 需要计算的标志位。如果该项包含非频繁项，则该标志位赋False
                for NFP in NotFPI:
                    if NFP in temp_item_hash:
                        NeedCalSup_flag = False
                if NeedCalSup_flag:
                    if temp_item_hash not in ExSupport.keys():
                        ExSupport[temp_item_hash] = 0
                    ExSupport[temp_item_hash] += caluExSpuuort(real_item, matrix_col)
                    if ExSupport[temp_item_hash] < minSup:
                        NotFPI.append(temp_item_hash)
            print '非频繁项集 NFP： ',NotFPI
        matrix_col += 1

    # 树按照队列索引完毕，下一步保存频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    print '频繁项集为：', freqItems


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

# ----------
# 10-12 v1.2
# ----------
def minetest(mine_i):
    freqItems = []
    ExSupport = {}
    NotFPI = []
    handledRoute = []  # 已经处理过的矩阵列
    for index in queue.keys():
        if index in handledRoute:
            continue
        route = []
        node = queue[index][1]
        needCalCol = []  # 需要计算的矩阵列
        for handledTID in node.TID:
            # handledTID --> matrix_col
            needCalCol.append(handledTID - ((mine_i-w+1) if mine_i>= w else 0) * w_tuple )  # 当前需要处理的矩阵列
            handledRoute.append(handledTID)
        findroute(node, route)

        stopLoopFlag = False
        for k in range(2, 5 if 5<len(route) else len(route)):
            if stopLoopFlag:
                break
            k_itemCombined = Combine.generatekitems(route, k)

            for item in k_itemCombined:
                real_item = []
                item_hash = ''
                for num in item:
                    real_item.append(route[num-1])
                    item_hash += route[num-1]
                if item_hash not in ExSupport.keys():
                    ExSupport[item_hash] = 0
                ExSupport[item_hash] += caluExSpuuort(real_item, needCalCol)
    # 所有 TID 遍历完
    # 筛选频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    if len(freqItems) > 1:
        print freqItems



# ----------
# 10-* v1.3
# ----------
def minetest(mine_i):
    freqItems = []
    ExSupport = {}
    NotFPI = []
    handledRoute = []  # 已经处理过的矩阵列
    for index in queue.keys():
        # print 'index in queue.keys():',index
        if index in handledRoute:
            continue
        route = []
        node = queue[index][1]
        needCalCol = []  # 需要计算的矩阵列
        for handledTID in node.TID:
            # handledTID --> matrix_col
            needCalCol.append(handledTID - ((mine_i-w+1) if mine_i>= w else 0) * w_tuple )  # 当前需要处理的矩阵列
            handledRoute.append(handledTID)
        findroute(node, route)
        # print 'route: ',route

        stopLoopFlag = False
        for k in range(2, 5 if 5<len(route) else len(route)):
            # print k, ' combine',
            if stopLoopFlag:
                break
            k_itemCombined = Combine.generatekitems(route, k)
            # print 'OK, Callen=',

            for item in k_itemCombined:
                real_item = []
                item_hash = ''
                for num in item:
                    item_hash += route[num - 1]
                    real_item.append(route[num-1])
                if hasNotFPIset(real_item, NotFPI):
                    continue
                if item_hash not in ExSupport.keys():
                    ExSupport[item_hash] = 0
                ExSupport[item_hash] += caluExSpuuort(real_item, needCalCol)
                if ExSupport[item_hash] < minSup:
                    NotFPI.append(real_item)
            # print 'OK.'
    # 所有 TID 遍历完
    # 筛选频繁项集
    for item in ExSupport.keys():
        if ExSupport[item] >= minSup:
            freqItems.append(item)
    # if len(freqItems) > 1:
    print freqItems


def hasNotFPIset(NowI, NotFPI):
    # NotFPI 中是否有 NowI 的子集
    for NI in NotFPI:   # [1,4]
        if set(NI).issubset(NowI):
            return True
    return False


