from __future__ import annotations
from collections import deque
from typing import List
import numpy as np
import random

class Face(object):
    def __init__(self, top, right, bottom, left, colour, items=False):
        self.location = deque([top, right, bottom, left])
        self.colour = colour
        if items:
            self.grid = items
        else:
            self.grid = [[colour for b in range(3)] for i in range(3)]

    def set_as_bottom(self, bottom):
        while self.location[2] != bottom:
            self.location.rotate()
            self.grid = [list(a) for a in zip(*self.grid[::-1])]

    def set_as_top(self, top):
        while self.location[0] != top:
            self.location.rotate()
            self.grid = [list(a) for a in zip(*self.grid[::-1])]

    def set_as_right(self, right):
        while self.location[1] != right:
            self.location.rotate()
            self.grid = [list(a) for a in zip(*self.grid[::-1])]

    def set_as_left(self, left):
        while self.location[3] != left:
            self.location.rotate()
            self.grid = [list(a) for a in zip(*self.grid[::-1])]

    def find_line(self, pos):
        return [self.grid[i][pos] for i in range(3)]


    def replace_line(self, line, pos):
        for ind, colour in enumerate(line):
            self.grid[ind][pos] = colour 

    def rotate(self, direction, start):
        self.set_as_top(direction)
        if start == self.location[3]:
            self.location.rotate(-1)

        elif start == self.location[1]:
            self.location.rotate()

    def __str__(self):
        a = ''
        for i in self.grid:
            a += str(i) + '\n'
        return a.strip()

    def get_visualizer_string(self):
        a = ''
        for i in range(3):
            for b in reversed(range(3)):
                a += self.grid[i][b]

        return a
        
    def copy(self):
        return Face(*self.location, self.colour, [i[:] for i in self.grid])

class Rubiks_Cube(object):
    def __init__(self, items: List[Face]=None):
        if items:
            self.faces = {}
            for face in items:
                self.faces[face.colour, face]

        else:
            self.faces = {
                'R' : Face('Y', 'G', 'W', 'B', 'R'),
                'B' : Face('Y', 'R', 'W', 'O', 'B'),
                'O' : Face('Y', 'B', 'W', 'G', 'O'),
                'G' : Face('Y', 'O', 'W', 'R', 'G'),
                'Y' : Face('O', 'G', 'R', 'B', 'Y'),
                'W' : Face('R', 'G', 'O', 'B', 'W')
            }


    def rotate(self, colour, direction, pos):
        start = colour
        currcolour = colour
        face = self.faces[currcolour]
        face.set_as_top(direction)
        currline = face.find_line(pos)
        newcolour = face.location[0]

        # fix orientation of side to right or left is currcolour and top is newcolour
        # if right is currcolour flip counter clockwise
        # if left is colour flip clockwise

        if pos == 2:
            side = self.faces[face.location[1]]
            side.rotate(newcolour, currcolour)

        elif pos == 0:
            side = self.faces[face.location[3]]
            side.rotate(newcolour, currcolour)

        while newcolour != start:
            newface = self.faces[newcolour]
            newface.set_as_bottom(currcolour)
            newline = newface.find_line(pos)
            newface.replace_line(currline, pos)
            currline = newline
            currcolour = newcolour
            newcolour = newface.location[0]

        self.faces[start].replace_line(currline, pos)


        return 1, [[colour, direction, pos]]

    def rotate_face(self, colour, times=1, CLC=0) -> tuple[int, List[List[str, str, int]]]:
        rotation = []
        val = times
        a = self.faces[self.faces[colour].location[0]]
        while times != 0:
            [a.set_as_right, a.set_as_left][CLC](colour)
            self.rotate(a.colour, a.location[0], [2, 0][CLC])
            rotation.append([a.colour, a.location[0], [2, 0][CLC]])
            times -= 1

        return val, rotation


    def Scramble(self):
        rotation = []
        for i in range(100):
            colours = 'RGBYOW'
            position = [0, 2]
            colour1 = random.choice(colours)
            colour2 = random.choice(self.faces[colour1].location)
            randpos = random.choice(position)

            rotation.append([colour1, colour2, randpos])
            self.rotate(colour1, colour2, randpos)

        return rotation

    def __str__(self):
        rows = ['' for i in range(9)]
        for i in 'YBRGOW':
            if i == 'Y':
                self.faces[i].set_as_top('O')
                for ind, i in enumerate(str(self.faces[i]).split('\n')):
                    rows[ind] += (' '*15 + i + ' '*30)

            elif i in 'RGOB':
                self.faces[i].set_as_top('Y')
                for ind, i in enumerate(str(self.faces[i]).split('\n')):
                    rows[ind + 3] += i

            else:
                self.faces[i].set_as_top('R')
                for ind, i in enumerate(str(self.faces[i]).split('\n')):
                    rows[ind + 6] += (' '*15 + i + ' '*30)

        return '\n'.join(rows)

    def visualizer_string(self):
        faces = {}
        for i in 'YBRGOW':
            if i == 'Y':
                self.faces[i].set_as_top('O')
                faces[i] = self.faces[i].get_visualizer_string()

            elif i in 'RGOB':
                self.faces[i].set_as_top('Y')
                faces[i] = self.faces[i].get_visualizer_string()

            else:
                self.faces[i].set_as_top('R')
                faces[i] = self.faces[i].get_visualizer_string()

        return faces

    def copy(self):
        return {key: item.copy() for key, item in self.faces.items()}


if __name__ == '__main__':
    import time
    rubik = Rubiks_Cube()
    # print(rubik.faces['R'])
    # rubik.scramble()
    # rubik.right_alg('R', 'Y')
    rubik.rotate_face('R')
    # rubik.rotate_face('R', 1)

    print(rubik)

    # test = Face('Y', 'G', 'W', 'B', 'R')
    # test.grid = [['R', 'R', 'W'], ['R', 'R', 'W'], ['R', 'R', 'W']]
    # test.set_as_top('B')
    # print(test.grid)
    # print(test.location)


    # print(test.location)
    # print(test.grid)
    # test.location.rotate()
    # print(test.location)