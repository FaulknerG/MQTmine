# -*- coding: utf-8 -*-
import random

def loadSimpleData():
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


def loadIBMDataSet():
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


def oldloadConnectData():
    fo = open("/Users/Faulkner/PycharmProjects/MLinActionCode/MQTmine/connect-4.data", "r")
    result = []
    for line in fo.readlines():
        trans = line.strip().split(',')
        retDict = {}
        for i in range(42):
            a = trans[i]
            if a == 'x':
                retDict['%d' %(i*3)] = 0.2
            elif a == 'o':
                retDict['%d' %(i*3+1)] = 0.2
            else:
                retDict['%d' %(i*3+2)] = 0.2
        result.append(retDict)
    itemSet = []
    for trans in result:
        for item in trans:
            itemSet.append(item)
    itemSet = frozenset(itemSet)
    return result, itemSet


def loadConnectData():
    # / Users / Faulkner / PycharmProjects / MLinActionCode / MQTmine / connect.dat
    fo = open("connect.dat", "r")
    result = []
    for line in fo.readlines():
        trans = line.strip().split(' ')
        retDict = {}
        for i in trans:
            retDict[i] = round(random.random(), 2)
        result.append(retDict)
    itemSet = []
    for trans in result:
        for item in trans:
            itemSet.append(item)
    itemSet = frozenset(itemSet)
    return result, itemSet

