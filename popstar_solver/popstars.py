# -*- coding: utf-8 -*-
"""Popstars node class and solution algorithm class.

This module contains classes for popstars node and solution algorithm.
"""
from copy import deepcopy
from collections import defaultdict


class PopstarsNode(object):

    """This class defines the node of popstars to represent game status."""

    def __init__(self, status):
        """create new instance to represent the current status.

        self.parents shows the parent nodes of current node
        self.children is a dict which uses child node as key, 
        a tuple (score, removed_cells, directly_connected) as values

        Args:
            status (list): 2-d list represents current game status

        Deleted Parameters:
            score (int, optional): highest score in current status
            previous_move (list, optional): coordinations of previous move
            previous_score (int, optional): score of previous move
            total_score (int, optional): highest score in current status
            parent (PopstarsNode, optional): previous node
        """
        self.status = status
        self.parents = []
        self.children = defaultdict(list)

    def update_parents(self):
        """update parents to its children scores.

        recursively update parents dest_node score according to its children

        Deleted Parameters:
            neighbour (TYPE): Description
            update_source (TYPE): Description
            next_node (TYPE): Description
            dest_node (TYPE): Description
            score (TYPE): Description
            removed_cells (list): Description
        """
        for a_parent in self.parents:
            for child in self.children:
                for a_dest in self.children[child]:
                    if (a_dest[0] + a_parent.children[self][0][0],
                            a_parent.children[self][0][1]) not in a_parent.children[child]:
                        a_parent.children[child].append((a_dest[0] + a_parent.children[self][0][0],
                                                         a_parent.children[self][0][1]))
            a_parent.update_parents()

    def convert_coordinations(self, coordinations):
        """convert coordination tuples into another format.

        orgrinal result of coordinations list is counted from top to down, left
        to right. it is needed to convert from left to right, bottom to top

        Args:
            coordinations (list): coordinations list

        Returns:
            list: coordinations in new format
        """
        result = []
        game_rows = len(self.status)
        for i in coordinations:
            result.append((i[1], game_rows - i[0] - 1))
        result = sorted(result)
        return result

    def __calc_new_status0(self, removed_cells):
        """calc new status according to removed cells

        Args:
            removed_cells (list): list of tuples of removed cells in original format

        Returns:
            list: 2d list represents new game status

        Deleted Parameters:
            status (list): 2s list represents the game status
        """
        # iterate through all removed cells. move up cell down and remove empty
        # cols
        result = deepcopy(self.status)
        # if len(result) != 0:
        #     colsLen = len(result[0])
        for i in removed_cells:
            for j in range(i[0], -1, -1):
                if j == 0:
                    result[j][i[1]] = ''
                else:
                    result[j][i[1]] = result[j - 1][i[1]]

        # rotate the matrix and find empty lines, remove them and rotate back
        result = [i for i in zip(*result) if set(i) != {''}]
        result = zip(*result)
        result = [list(i) for i in result]

        #fill empty line
        # for i in range(0, len(result)):
        #     if len(result[i]) < colsLen:
        #         for j in range(0, colsLen-len(result[i])):
        #             result[i].append('')
        return result

    def __calc_new_status1(self, removed_cells):
        result = deepcopy(self.status)
        if len(result) != 0:
            colsLen = len(result[0])
        lineLen = len(result)

        for removed_cell in removed_cells:
            result[removed_cell[0]][removed_cell[1]] = ''

        #fix
        for i in  range(len(result)-1, 0, -1):
            upLine = result[i-1]
            for j in range(0, len(result[0])):
                if result[i][j] == '':
                    iH = i -1
                    while True:
                        if iH <= 0:
                            break
                        if result[iH][j] == '':
                            iH -= 1
                        else:
                            break
                    tmp = result[i][j]
                    result[i][j] = result[iH][j]
                    result[iH][j] = tmp

        # rotate the matrix and find empty lines, remove them and rotate back
        result = [i for i in zip(*result) if set(i) != {''}]
        result = zip(*result)
        result = [list(i) for i in result]

        #fill empty line
        for i in range(0, len(result)):
            if len(result[i]) < colsLen:
                for j in range(0, colsLen-len(result[i])):
                    result[i].append('')
        if len(result) == 0:
            for i in range(0, lineLen):
                line = []
                for j in range(0, colsLen):
                    line.append('')
                result.append(line)
        return result


    def calc_new_status(self, removed_cells):
        if True:
            return self.__calc_new_status0(removed_cells)
        else:
            return self.__calc_new_status1(removed_cells)

    def calc_new_status_withFix(self, removed_cells):
        return self.__calc_new_status1(removed_cells)

    def find_next_moves(self):
        """find possible next moves for a given status

        Returns:
            iterator: 3-element tuple of (list of removed stars, score, next status)

        Deleted Parameters:
            status (list): given game status
        """
        # iterate through all cells, and group them with upper cells and left
        # cells

        # generate separated cells then merge the them with same neighbours
        matrix_rows = len(self.status)
        if matrix_rows == 0:
            matrix_cols = 0
        else:
            matrix_cols = len(self.status[0])
        matrix = []
        for i in range(matrix_rows):
            matrix.append([[(i, j)] for j in range(matrix_cols)])
        # merge coordinations
        for i in range(matrix_rows):
            for j in range(matrix_cols):
                if self.status[i][j] != '':
                    # is same with right cell?
                    if j < matrix_cols - 1 and self.status[i][j] == self.status[i][j + 1]:
                        new_item = matrix[i][j] + matrix[i][j + 1]
                        matrix[i][j] = matrix[i][j + 1] = new_item
                    # is same with down cell?
                    if i < matrix_rows - 1 and self.status[i][j] == self.status[i + 1][j]:
                        new_item = matrix[i][j] + matrix[i + 1][j]
                        matrix[i][j] = matrix[i + 1][j] = new_item

        # filter out all unvalid results
        result = []
        # filter out all single-cell groups
        for i in range(matrix_rows):
            for j in range(matrix_cols):
                if (len(matrix[i][j]) > 1 and
                        matrix[i][j] not in result):
                    result.append(matrix[i][j])

        # filter sublists
        result = sorted(result, key=len, reverse=True)
        changed = True
        while changed:
            changed = False
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    if set(result[i]).issuperset(set(result[j])):
                        result.remove(result[j])
                        changed = True
                        break
                if changed:
                    break

        if result:
            for i in result:
                yield (self.convert_coordinations(i),
                       len(i) * len(i) * 5,
                       self.calc_new_status(i))
        else:
            left_cells = sum([len(i) - i.count('') for i in self.status])
            left_cells_score = 2000 - 20 * left_cells * left_cells
            if left_cells_score < 0:
                left_cells_score = 0
            for i in self.parents:
                i.children[self] = [(i.children[self][0][0] + left_cells_score,
                                     i.children[self][0][1],
                                     i.children[self][0][2])]


class PopstarsSolver(object):

    """find the best solultion for a given status"""

    def __init__(self, start_node):
        """init popstars game solver with beginning game status node

        Args:
            start_node (PopstarsNode): start node of the game

        Deleted Parameters:
            start_status (list): 2-d list represents the game status
        """
        self.start_node = start_node

    def search(self):
        """search the best solution from the beginning status node.

        search function tries to go through all possible nodes and maintains
        the best possible score to reach the node from start_node.

        Returns:
            int: the best score of the game
        """
        open_set = set()
        closed_set = set()
        open_set.add(self.start_node)

        # loop through all nodes until open set is empty to build neighbor map
        while open_set:
            current_node = open_set.pop()
            closed_set.add(current_node)
            for removed_cells, score, next_status in current_node.find_next_moves():
                open_status_set = [i.status for i in open_set]
                closed_status_set = [i.status for i in closed_set]
                if next_status in open_status_set:
                    index = open_status_set.index(next_status)
                    node = list(open_set)[index]
                elif next_status in closed_status_set:
                    index = closed_status_set.index(next_status)
                    node = list(closed_set)[index]
                else:
                    node = PopstarsNode(next_status)
                    open_set.add(node)
                node.parents.append(current_node)
                current_node.children[node].append(
                    (score, removed_cells, True))
            current_node.update_parents()
        max_score = []
        for i in self.start_node.children:
            max_score += self.start_node.children[i]
        return max(max_score)[0]

    def find_result(self):
        """find best result after searching all nodes

        Returns:
            list: step by step nodes for best score
        """
        result = []
        current_node = self.start_node
        while current_node.children:
            values = []
            for i in current_node.children:
                values += current_node.children[i]
            # find removed cells and then find the direct next move
            removed_cells = max(values)[1]
            for key, value in current_node.children.items():
                for i in value:
                    if len(i) == 3 and i[1] == removed_cells:
                        current_node = key
                        result.insert(0, (current_node, removed_cells))
                        break
                if current_node == key:
                    break
        return result
