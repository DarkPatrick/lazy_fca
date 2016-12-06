# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 18:20:07 2016

@author: Egor
"""


class Tree:
    def __init__(self):
        self.nodes = list()
        # negative result
        self.nodes.append(dict({0: None, 1: None, 2: None}))
        # positive result
        self.nodes.append(dict({0: None, 1: None, 2: None}))

    def addNode(self, rules, pred=[], succ=1):
        if (type(rules) == set):
            rules = list([rules])
        self.nodes.append(dict({0: 1 - succ, 1: succ, 2: rules}))
        if (len(pred) > 0):
            self.nodes[pred[0]][pred[1]] = len(self.nodes) - 1

    def walkDownTheTree(self, attribute, start_with=2):
        if (start_with < 2):
            return start_with
        for i in self.nodes[start_with][2]:
            if (len(attribute - (attribute & i)) == 0):
                result = 1
                break
        else:
            result = 0
        return self.walkDownTheTree(attribute, self.nodes[start_with][result])
