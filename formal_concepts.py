# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:43:16 2016

@author: Egor
"""


import copy as cp
from itertools import combinations


class Concept:
    def __init__(self, objects=[], attributes=[]):
        self.objects = cp.deepcopy(objects)
        self.attributes = cp.deepcopy(attributes)

    def __str__(self):
        return("{" + str(self.objects) + ", " + str(self.attributes) + "}")

    def __eq__(self, concept):
        if ((self.objects == concept.objects) or
                (self.attributes == concept.attributes)):
            return True
        else:
            return False

    def __ne__(self, concept):
        return(not (self == concept))


class ConceptLattice:
    class ConceptMatrix:
        def __init__(self, matrix):
            self.matrix = cp.deepcopy(matrix)
            self.num_of_objs = len(self.matrix)
            if (self.num_of_objs > 0):
                self.num_of_atts = len(self.matrix[0])
            self.objects = list([])
            self.attributes = list([])
            for i in range(self.num_of_objs):
                self.objects.append(
                    set({
                         j for j in range(self.num_of_atts)
                         if (1 == matrix[i][j])
                    }))
            for i in range(self.num_of_atts):
                self.attributes.append(
                    set({
                         j for j in range(self.num_of_objs)
                         if (1 == matrix[j][i])
                    }))

        def __str__(self):
            return(str(self.matrix))

        def dashObjects(self, objects_nums):
            attributes = set({i for i in range(self.num_of_atts)})
            for i in objects_nums:
                attributes &= self.objects[i]
            return attributes

        def dashAttributes(self, attributes_nums):
            objects = set({i for i in range(self.num_of_objs)})
            for i in attributes_nums:
                objects &= self.attributes[i]
            return objects

    def __init__(self, matrix=[]):
        self.num_of_concepts = 0
        self.concepts = []
        self.concept_matrix = self.ConceptMatrix(matrix)

    def __str__(self):
        res_str = ''
        for i in self.concepts:
            res_str += i.__str__() + '\n'
        return(res_str)

    def __add__(self, concept):
        for i in self.concepts:
            if (i == concept):
                break
        else:
            self.concepts.append(concept)

    def supp(self, attributes_nums):
        s = (len(self.concept_matrix.dashAttributes(list(attributes_nums))) /
             self.concept_matrix.num_of_objs)
        return s

    def conf(self, attributes_nums, l_attributes_nums):
        c = (len(self.concept_matrix.dashAttributes(list(attributes_nums))) /
             len(self.concept_matrix.dashAttributes(list(l_attributes_nums))))
        return c

    def calculateFormalConcepts(self):
        def process(set_of_objs, cur_obj, concept):
            for i in range(cur_obj):
                if (i in (set_of_objs - set(concept.objects))):
                    break
            else:
                self.__add__(concept)
                for i in range(cur_obj + 1, self.concept_matrix.num_of_objs):
                    if (i not in set(concept.objects)):
                        set_of_objs = set(concept.objects) | set({i})
                        cur_obj_atts = set(
                            concept.attributes
                            ) & self.concept_matrix.dashObjects([i])
                        cur_obj_dbl_dash = self.concept_matrix.dashAttributes(
                            list(cur_obj_atts)
                            )
                        new_concept = Concept(cur_obj_dbl_dash, cur_obj_atts)
                        process(set_of_objs, i, new_concept)

        cur_obj_set = set({})
        cur_obj = -1
        cur_obj_atts = self.concept_matrix.dashObjects([])
        cur_obj_dbl_dash = self.concept_matrix.dashAttributes(
                                list(cur_obj_atts))
        concept = Concept(cur_obj_dbl_dash, cur_obj_atts)
        process(cur_obj_set, cur_obj, concept)

        for i in range(self.concept_matrix.num_of_objs):
            cur_obj_set = set({i})
            cur_obj = i
            cur_obj_atts = self.concept_matrix.dashObjects([i])
            cur_obj_dbl_dash = self.concept_matrix.dashAttributes(
                                    list(cur_obj_atts))
            concept = Concept(cur_obj_dbl_dash, cur_obj_atts)
            process(cur_obj_set, cur_obj, concept)

    def findContentRules(self,
                         min_supp=0.1,
                         max_supp=1,
                         min_conf=0.5,
                         max_conf=1):
        def checkPotentialRules(vertices, min_conf, max_conf):
            res = list([])
            for i in range(1, len(vertices)):
                for j in combinations(vertices, i):
                    list_j = list(j)
                    conf = self.conf(list(vertices), list_j)
                    if ((conf >= min_conf) and (conf <= max_conf)):
                        supp = self.supp(list(vertices))
                        res.append(list([
                                         set(list_j),
                                         vertices - set(list_j),
                                         supp,
                                         conf]))
            return res

        v_queue = [-1]
        chain_queue = [set({})]
        for (v, c) in zip(v_queue, chain_queue):
            continue_search = False
            for i in range(v + 1, self.concept_matrix.num_of_atts):
                intersection = c | set({i})
                supp = self.supp(list(intersection))
                if (supp >= min_supp):
                    if (supp <= max_supp):
                        v_queue.append(i)
                        chain_queue.append(intersection)
                    continue_search = True
            if ((not continue_search) and (len(c) > 1)):
                new_rules = checkPotentialRules(c, min_conf, max_conf)
                if (len(new_rules) > 0):
                    yield new_rules

    def findHemmingDist(self, a1, a2):
        if (type(a1) == int):
            a1 = self.concept_matrix.attributes[a1]
        if (type(a2) == int):
            a2 = self.concept_matrix.attributes[a2]
        diff = len(a1 & a2)
        order = 1
        if (diff > self.concept_matrix.num_of_objs / 2):
            diff = self.concept_matrix.num_of_objs - diff
            order = -1
        dist = tuple([diff, order])
        return dist

    def calcAllHemmingDists(self):
        self.hemm_dist = list()
        for i in range(self.concept_matrix.num_of_atts):
            for j in range(i + 1, self.concept_matrix.num_of_atts):
                dist = self.findHemmingDist(i, j)
                self.hemm_dist.append(list([i, j, dist[0], dist[1]]))
            self.hemm_dist = sorted(self.hemm_dist, key=lambda x: x[2])

    def getHemmingDist(self, a1, a2):
        if (a1 > a2):
            a1, a2 = a2, a1
        # search can be done in O(log(n))
        for i in self.hemm_dist:
            if ((i[0] == a1) and (i[1] == a2)):
                found = True
                break
        else:
            found = False
        if (found):
            dist = tuple([i[2], i[3]])
        else:
            dist = tuple([-1, 0])
        return dist
