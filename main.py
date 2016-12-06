# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:36:30 2016

@author: Egor
"""


from formal_concepts import ConceptLattice
from tree import Tree
import csv


def loadData(file_name, train_data=True, header=True):
    context = list()
    with open(file_name, 'r+', newline='') as fn1:
        reader = csv.reader(fn1)
        row_num = 0
        for row in reader:
            if ((header) and (0 == row_num)):
                row_num += 1
                continue
            context.append(list())
            for col in range(len(row) - 1):
                if (train_data):
                    if (('x' == row[col]) or
                       (('b' == row[col]) and
                       (row[len(row) - 1] == 'negative'))):
                        context[row_num - 1].append(1)
                    else:
                        context[row_num - 1].append(0)
                else:
                    if ('x' == row[col]):
                        context[row_num - 1].append(1)
                    else:
                        context[row_num - 1].append(0)
            if ('positive' == row[len(row) - 1]):
                context[row_num - 1].append(1)
            else:
                context[row_num - 1].append(0)
            row_num += 1
    concept_lattice = ConceptLattice(matrix=context)
    return concept_lattice


def getHypothesis(objs, hyp_tree):
    res = set()
    for i in range(len(objs)):
        if (1 == hyp_tree.walkDownTheTree(objs[i])):
            res.append(i)
    return res


def checkPrediction(objs, predictions, hyp_tree):
    empiric = getHypothesis(objs, hyp_tree)
    true_negatives = len(predictions - empiric)
    false_positives = len(empiric - predictions)
    sum_of_mistakes = true_negatives + false_positives
    return tuple([sum_of_mistakes, true_negatives, false_positives])


concept_lattice = loadData('G:/hse/умвад/lazyfca15-master/train1.csv')
a = concept_lattice.findContentRules(
                                     min_supp=0.01,
                                     min_conf=0,
                                     max_conf=0.3)

concept_lattice.calcAllHemmingDists()

'''
t1 = Tree()
t1.addNode({1, 2, 3, 4, 8})
t1.addNode({5, 6, 7}, [2, 0])
t1.addNode({10, 12, 7}, [3, 1])
t1.addNode({8}, [2, 1])
# print(t1.nodes)
print(t1.walkDownTheTree(set({7})))
'''
