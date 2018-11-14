# -*- coding: utf-8 -*-

"""
组合算法,递归实现
http://www.cnblogs.com/shuaiwhu/archive/2012/04/27/2473788.html
"""

import time
# arr 原始列表（数组）
# start 遍历起始位置
# result 保存结果
# count 结果列表的索引值，辅助变量
# NUM 要选取的元素个数
# arr_len 原始数组的长度，为定值
def combine_increase(arr, start, result, count, NUM, arr_len, returnItem):
    for i in range(start, arr_len + 1 - count):
        result[count - 1] = i
        if count == 1:
            returnItem.append(result)
            for j in range(NUM-1, -1, -1):
                # pass
                print arr[result[j]],
            print "\n"
        else:
            combine_increase(arr, i+1, result, count-1, NUM, arr_len, returnItem)


def combine_decrease(arr, start, result, count, NUM, returnItem):
    for i in range(start, count-1, -1):
        result[count-1] = i-1
        if count > 1:
            combine_decrease(arr, i-1, result, count-1, NUM, returnItem)
        else:
            returnItem.append(result)
            for j in range(NUM-1, -1, -1):
                pass
                print arr[result[j]],
            print "\n"


def combine(route, num):
    arr = route
    num = num
    result = []
    for i in range(num):
        result.append(0)
    returnItem = []
    combine_increase(arr, 0, result, num, num, len(arr), returnItem)
    print '----'
    combine_decrease(arr, len(arr), result, num, num, returnItem)
    return returnItem

# ----------------------------------------------------------
# v1.0版本的产生所有
# ----------------------------------------------------------
import copy
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


def generateCom(m, n, retitems, Allitems):
    if n is 0:
        Allitems.append(copy.copy(retitems))
        return
    for i in range(m, n-1, -1):
        retitems[n-1] = i
        generateCom(i-1, n-1, retitems, Allitems)



# ----------------------------------------------------------
# v11 产生 n 项集
# ----------------------------------------------------------
def generatekitems(route, i):
    Allitems = []
    # 产生所有的组合，这里用到组合数
    m = len(route)
    Allitems.append(range(1, i+1))

    retitem = []
    for j in range(i):
        retitem.append(0)
    generateCom(m, i, retitem, Allitems)
    return Allitems


def generateCom(m, n, retitems, Allitems):
    if n is 0:
        Allitems.append(copy.copy(retitems))
        return
    for i in range(m, n-1, -1):
        retitems[n-1] = i
        generateCom(i-1, n-1, retitems, Allitems)


if __name__ == '__main__':
    # arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    time_start = time.time()

    arr = ['1', '2', '3', '4', '5', '6']
    # num = 4  # 选取的元素个数
    result = [0, 0, 0, 0]  # num

    # combine_increase(arr, 0, result, num, num, len(arr))
    # print '-----'
    # combine_decrease(arr, len(arr), result, num, num)


    a1 = generatekitems(arr, 2)
    print a1
    print len(a1)

    time_end = time.time()
    print time_end - time_start, 's'