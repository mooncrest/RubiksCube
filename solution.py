from rubiks import Rubiks_Cube
from typing import List, Any

class Solution(Rubiks_Cube):
    def locate_side(self, colour, side1=None):
        temp = []
        for face in self.faces.values():
            if face.grid[0][1] == colour:
                temp.append((face.colour, self.faces[face.colour].location[0]))

            if face.grid[1][0] == colour:
                temp.append((face.colour, self.faces[face.colour].location[3]))

            if face.grid[1][2] == colour:
                temp.append((face.colour, self.faces[face.colour].location[1]))

            if face.grid[2][1] == colour:
                temp.append((face.colour, self.faces[face.colour].location[2]))

        location = temp
        if side1:
            location = []
            for block in temp:
                self.faces[block[0]].set_as_top(block[1]) 
                self.faces[block[1]].set_as_top(block[0])
                if self.faces[block[0]].grid[0][1] in [colour, side1] and \
                   self.faces[block[1]].grid[0][1] in [colour, side1]:
                    location.append(block)
                    break

        return location

    def locate_corner(self, colour, side1=None, side2=None):
        temp = []
        for face in self.faces.values():
            for a, b, c in zip([0, 0, 2, 2], [0, 2, 0, 2], [(3, 0), (0, 1), (2, 3), (1, 2)]):
                if face.grid[a][b] == colour:
                    colour1 = face.colour
                    colour2 = face.location[c[0]] # set as right
                    colour3 = face.location[c[1]] # set as left
                    temp.append((colour1, colour2, colour3))

        if side1:
            cleaned = []
            for center, top, right in temp:
                self.faces[top].set_as_right(center)
                self.faces[right].set_as_left(center)
                if self.faces[top].grid[0][2] == side1:
                    cleaned.append((center, top, right))
                elif self.faces[right].grid[0][0] == side1:
                    cleaned.append((center, top, right))
            temp = cleaned

        if side2:
            cleaned = []
            for center, top, right in temp:
                self.faces[top].set_as_right(center)
                self.faces[right].set_as_left(center)
                if self.faces[top].grid[0][2] == side2:
                    cleaned.append((center, top, right))
                elif self.faces[right].grid[0][0] == side2:
                    cleaned.append((center, top, right))
            temp = cleaned

        return temp


    def right_alg(self, colour, direction):
        start = self.faces[colour]
        start.set_as_top(direction)
        sides = [i for i in start.location]
        rotation = []

        self.rotate(colour, sides[0], 2)
        rotation.append([colour,sides[0], 2])
        self.rotate(colour, sides[3], 2)
        rotation.append([colour,sides[3], 2])
        self.rotate(colour, sides[2], 0)
        rotation.append([colour,sides[2], 0])
        self.rotate(colour, sides[1], 0)
        rotation.append([colour,sides[1], 0])

        return 4, rotation


    def left_alg(self, colour, direction):
        start = self.faces[colour]
        start.set_as_top(direction)
        sides = [i for i in start.location]
        rotation = []

        self.rotate(colour, sides[0], 0)
        rotation.append([colour, sides[0], 0])
        self.rotate(colour, sides[1], 0)
        rotation.append([colour, sides[1], 0])
        self.rotate(colour, sides[2], 2)
        rotation.append([colour, sides[2], 2])
        self.rotate(colour, sides[3], 2)
        rotation.append([colour, sides[3], 2])

        return 4, rotation

    def Cross(self, colour):
        '''returns the number of steps required to solve
        
        creates a <colour> cross
        <flow chart>
        step 1: <colour> is already in correct position we are done
        step 2: <colour> is on the side not between yellow
                or opposite colour skip step 4
        step 3: a corner piece is on the yellow side but not
                between the right colour ie yellow and red piece is
                between yellow and orange
        step 4: rotate each piece to the opposite side and find a 
                colour that matches ie yellow and red is between white and red
        step 5: fix it if twisted after u turn it back to yellow fix it
        '''

        temp = self.faces[self.faces[colour].location[0]]
        opp_colour = temp.location[temp.location.index(colour) - 2]
        val = 0
        rotation = []

        for c in [i for i in self.faces[colour].location]:
            sides = self.locate_side(colour, c)[0]
            if sides == (colour, c):
                continue

            elif colour not in sides and opp_colour not in sides:
                self.faces[sides[0]].set_as_top(opp_colour)
                if self.faces[sides[0]].location[1] == sides[1]:
                    store = self.right_alg(sides[0], opp_colour)
                    val + store[0]
                    rotation.extend(store[1])

                else:
                    store = self.left_alg(sides[0], opp_colour)
                    val + store[0]
                    rotation.extend(store[1])

            elif colour in sides and c not in sides:
                store = self.rotate_face(sides[0] if sides[0] != colour else sides[1], 2)
                val + store[0]
                rotation.extend(store[1])

            if opp_colour in self.locate_side(colour, c)[0]:
                while c not in self.locate_side(colour, c)[0]:
                    store = self.rotate_face(opp_colour)
                    val + store[0]
                    rotation.extend(store[1])

                new = self.locate_side(colour, c)[0]

                store = self.rotate_face(new[0] if new[0] != opp_colour else new[1], 2)
                val + store[0]
                rotation.extend(store[1])


            if self.locate_side(colour, c)[0] == (c, colour):
                store = self.rotate_face(colour, CLC=1)
                val + store[0]
                rotation.extend(store[1])

                store = self.rotate(colour, c, 0)
                val + store[0]
                rotation.extend(store[1])

                store = self.rotate_face(colour)
                val + store[0]
                rotation.extend(store[1])

                store = self.rotate_face(c, CLC=1)
                val + store[0]
                rotation.extend(store[1])

        return val, rotation



    def Corners(self, colour):
        '''returns the number of steps required to solve
        
        fixes the correct corners of the colour
        <flow chart>
        step 1: If the twisted corner piece is currently in between 3 pieces
                that contains <colour> pop it out. If all 3 colours on the piece 
                matches are located between the 3 faces ignore step 2
        step 2: Simply rotate the face opposite of <colour> and line up 2 colours
                with whats on the cube.
        step 3: preform the left or right algorithm and pop the piece down into
                the corner
        '''
        temp = self.faces[self.faces[colour].location[0]]
        opp_colour = temp.location[temp.location.index(colour) - 2]
        val = 0
        lst1 = [i for i in self.faces[colour].location]
        lst2 = lst1[:]
        lst2.insert(0, lst2.pop(-1))
        rotation = []

        for col1, col2, in zip(lst1, lst2):
            sides = self.locate_corner(colour, col1, col2)[0]

            if colour in sides and (col1 not in sides or col2 not in sides):
                c = next(i for i in sides if i != colour)
                self.faces[c].set_as_top(opp_colour)
                if self.faces[c].location[3] in sides:
                    store =  self.left_alg(c, opp_colour)
                    val += store[0]
                    rotation.extend(store[1])
                else:
                    store = self.right_alg(c, opp_colour)
                    val += store[0]
                    rotation.extend(store[1])
                # right alg pop it and match

            sides = self.locate_corner(colour, col1, col2)[0]

            if opp_colour in sides:
                while not all(map(lambda x: x in sides, [col1, col2])):
                    store = self.rotate_face(opp_colour)
                    val += store[0]
                    rotation.extend(store[1])
                    sides = self.locate_corner(colour, col1, col2)[0]
                # match up the two colours by rotating opp

            if all(map(lambda x: x in sides, [col1, col2, colour])) or\
               all(map(lambda x: x in sides, [col1, col2, opp_colour])):
                # fixing it in correct position
                self.faces[col1].set_as_top(opp_colour)

                if self.faces[col1].grid[0][0]:
                    while sides[0] != colour:
                        store = self.left_alg(col1, opp_colour)
                        val += store[0]
                        rotation.extend(store[1])
                        sides = self.locate_corner(colour, col1, col2)[0]

                else:
                    while sides[0] != colour:
                        store = self.right_alg(col1, opp_colour)
                        val += store[0]
                        rotation.extend(store[1])
                        sides = self.locate_corner(colour, col1, col2)[0]

        return val, rotation

    def Fix_sides(self, colour):
        side1 = self.faces[colour].location.copy()
        self.faces[colour].location.rotate()
        side2 = self.faces[colour].location.copy()
        self.faces[colour].location.rotate(-1)

        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        steps, rotations = 0, []

        for colour1, colour2 in zip(side1, side2):

            a = self.locate_side(colour1, colour2)
            if a[0][0] != opposite and a[0][1] != opposite and\
               (a[0][0] != colour1 or a[0][1] != colour2):

                self.faces[a[0][0]].set_as_top(opposite)
                if self.faces[a[0][0]].location[3] == a[0][1]:
                    op = self.left_alg(a[0][0], opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]
                    op = self.right_alg(a[0][1], opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]

                else:
                    op = self.right_alg(a[0][0], opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]
                    op = self.left_alg(a[0][1], opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]

                a = self.locate_side(colour1, colour2)

            if a[0][0] == side1 and a[0][1] == side2:
                pass

            elif a[0][0] == opposite:
                # rotate the top face until colour2 until it matches face
                op = self.fix_face(colour2, colour1, opposite)
                steps, rotations = op[0] + steps, rotations + op[1]
            elif a[0][1] == opposite:
                # rotate the top face until colour1 matches face
                op = self.fix_face(colour1, colour2, opposite)
                steps, rotations = op[0] + steps, rotations + op[1]

        return steps, rotations

    def fix_face(self, c1, c2, opposite):

        steps, rotations = 0, []
        while self.locate_side(c1, c2)[0] != (c1, opposite):
            op = self.rotate_face(opposite)
            steps, rotations = op[0] + steps, rotations + op[1]

        # print(self)
        self.faces[c1].set_as_top(opposite)
        if self.faces[c1].location[3] == c2:
            op = self.rotate_face(opposite, CLC=1)
            steps, rotations = op[0] + steps, rotations + op[1]

            op = self.left_alg(c1, opposite)
            steps, rotations = op[0] + steps, rotations + op[1]
            op = self.right_alg(c2, opposite)
            steps, rotations = op[0] + steps, rotations + op[1]

        else:
            op = self.rotate_face(opposite)
            steps, rotations = op[0] + steps, rotations + op[1]

            op = self.right_alg(c1, opposite)
            steps, rotations = op[0] + steps, rotations + op[1]
            op = self.left_alg(c2, opposite)
            steps, rotations = op[0] + steps, rotations + op[1]

        # pop it in correct corner
        return steps, rotations

    def Top_cross(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        steps, rotations = 0, []
        a = [i for i in self.locate_side(opposite) if i[0] == opposite]
        if len(a) == 2:
            if self.faces[colour].location[0] in [a[1][1], a[1][0], a[0][0], a[0][1]] \
                and self.faces[colour].location[2] in [a[1][1], a[1][0], a[0][0], a[0][1]]:
                start = self.faces[self.faces[colour].location[1]]
                start.set_as_top(opposite)

                op = self.rotate(opposite, start.location[1], 2)
                steps, rotations = op[0] + steps, rotations + op[1] 

                op = self.right_alg(start.colour, opposite)
                steps, rotations = op[0] + steps, rotations + op[1] 

                start.set_as_top(opposite)

                op = self.rotate(start.location[1], opposite, 0)
                steps, rotations = op[0] + steps, rotations + op[1] 


            elif self.faces[colour].location[1] in [a[1][1], a[1][0], a[0][0], a[0][1]] \
                and self.faces[colour].location[3] in [a[1][1], a[1][0], a[0][0], a[0][1]]:
                start = self.faces[self.faces[colour].location[2]]
                start.set_as_top(opposite)

                op = self.rotate(opposite, start.location[1], 2)
                steps, rotations = op[0] + steps, rotations + op[1] 

                op = self.right_alg(start.colour, opposite)
                steps, rotations = op[0] + steps, rotations + op[1] 

                start.set_as_top(opposite)

                op = self.rotate(start.location[1], opposite, 0)
                steps, rotations = op[0] + steps, rotations + op[1] 

            else:
                if self.check_l_shape(colour, a):
                    # rotate back
                    self.faces[a[0][1]].set_as_top(opposite)
                    left = self.faces[a[0][1]].location[3]
                    op = self.rotate(opposite, left, 2)
                    steps, rotations = op[0] + steps, rotations + op[1] 

                    op = self.right_alg(a[0][1], left)
                    steps, rotations = op[0] + steps, rotations + op[1]

                else:
                    self.faces[a[1][1]].set_as_top(opposite)
                    left = self.faces[a[1][1]].location[3]
                    op = self.rotate(opposite, left, 2)
                    steps, rotations = op[0] + steps, rotations + op[1] 

                    self.faces[a[1][1]].set_as_top(opposite)
                    op = self.right_alg(a[1][1], left)
                    steps, rotations = op[0] + steps, rotations + op[1] 

                op = self.rotate(left, opposite, 0)
                steps, rotations = op[0] + steps, rotations + op[1] 

        elif len(a) == 0:
            face_c = self.faces[colour].location[1]
            self.faces[face_c].set_as_top(opposite)

            save = self.faces[face_c].location[1]
            op = self.rotate(opposite, save, 2)
            steps, rotations = op[0] + steps, rotations + op[1] 
            # print(self.faces[colour].location[1])
            # print(opposite)

            op = self.right_alg(face_c, opposite)
            steps, rotations = op[0] + steps, rotations + op[1] 
            
            op = self.rotate(save, opposite, 0)
            steps, rotations = op[0] + steps, rotations + op[1] 

            op = self.Top_cross(colour)
            steps, rotations = op[0] + steps, rotations + op[1] 

        return steps, rotations

    def check_l_shape(self, colour, location):
        spots = [(0, 1), (1, 2), (2, 3), (3, 0)]
        loc = self.faces[colour].location
        for x1, x2 in spots:
            if loc[x1] == location[0][1] and loc[x2] == location[1][1]:
                return True

        return False

    def Top_corners(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        steps, rotations = 0, []
        side1 = self.faces[opposite].location.copy()
        self.faces[opposite].location.rotate()
        side2 = self.faces[opposite].location.copy()
        self.faces[opposite].location.rotate(-1)

        num = self.count_corners(side1, side2, opposite)
        while len(num) < 2:
            op = self.rotate_face(opposite)
            steps, rotations = op[0] + steps, rotations + op[1] 
            num = self.count_corners(side1, side2, opposite)

        # print(self)
        if len(num) == 4:
            return steps, rotations

        elif len(num) == 2:
            side = ''
            for i in side1:
                if i not in num[0] and i not in num[1]:
                    side += i

            if not side:
                # print('run')
                flip = num[0][1] if num[0][1] != opposite else num[0][2]
                self.faces[flip].set_as_top(opposite)
                if self.faces[flip].location[1] not in num[0]:
                    flip = self.faces[flip].location[3]
                    # right alg swap left alg 3 times and rotate
                self.faces[flip].set_as_top(opposite)
                save = self.faces[flip].location[1]
                count = 0
                # print(flip)
                # print(opposite)
                # print(save)
                while count < 3:
                    op = self.right_alg(flip, opposite)
                    steps, rotations = op[0] + steps, rotations + op[1] 
                    count += 1

                while count > 0:
                    op = self.left_alg(save, opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]
                    count -= 1

                # print(self)
                op = self.rotate(save, flip, 2)
                steps, rotations = op[0] + steps, rotations + op[1]
                op = self.Top_corners(colour)
                steps, rotations = op[0] + steps, rotations + op[1]
                return steps, rotations


            if side:
                # print('run')
                num = self.count_corners(side1, side2, opposite)
                # print(num)
                self.faces[side].set_as_top(opposite)
                flip = self.faces[side].location[3]
                self.faces[flip].set_as_top(opposite)
                save = self.faces[flip].location[1]
                # print(flip)
                # print(save)

                count = 0
                while count < 3:
                    op = self.right_alg(flip, opposite)
                    steps, rotations = op[0] + steps, rotations + op[1] 
                    count += 1

                while count > 0:
                    # print(self.faces[flip].location[1])
                    op = self.left_alg(save, opposite)
                    steps, rotations = op[0] + steps, rotations + op[1]
                    count -= 1

                op = self.rotate(flip, save, 0)
                steps, rotations = op[0] + steps, rotations + op[1]

                # print(self)

        return steps, rotations


    def count_corners(self, side1, side2, opposite):
        count = []
        for c1, c2 in zip(side1, side2):
            if all(map(lambda x: x in {c1, c2, opposite}, \
                self.locate_corner(c1, c2, opposite)[0])): 
                count.extend(self.locate_corner(c1, c2, opposite))
        return count

    def Invert(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        sides = [i for i in self.locate_corner(opposite) if i[0] != opposite]
        steps, rotations = 0, []

        if len(sides) > 1:
            start = sides[0][0]
            self.faces[start].set_as_top(colour)
            if self.faces[start].location[1] not in sides[0]:
                start = self.faces[start].location[3]
                self.faces[start].set_as_top(colour)

            right = self.faces[start].location[1]
            # print(start)
            # print(right)
            while len(sides) != 0:
                op = self.right_alg(start, colour)
                steps, rotations = op[0] + steps, rotations + op[1]
                new = [i for i in self.locate_corner(opposite) if i[0] != opposite]
                if len(new) < len(sides):
                    # print(start)
                    # print(right)
                    # print(new)
                    if len(new) == 0:
                        break
                    if right not in new[0] and start not in new[0]:
                        # print('run')
                        # print(start)
                        # print(start in new[0])
                        op = self.rotate(right, start, 0)
                        steps, rotations = op[0] + steps, rotations + op[1]
                        op = self.rotate(right, start, 0)
                        steps, rotations = op[0] + steps, rotations + op[1]

                    elif right in new[0]:
                        op = self.rotate(right, start, 0)
                        steps, rotations = op[0] + steps, rotations + op[1]

                    else: 
                        # print('run')
                        op = self.rotate(start, right, 2)
                        steps, rotations = op[0] + steps, rotations + op[1]

                    # print(self)
                    sides = new

        return steps, rotations



    def Final_Solve(self, colour):
        steps, rotations = 0, []
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]

        if all(self._Solved_face(col) for col in self.faces[colour].location):
            return 0, []

        for col in self.faces[colour].location:
            if self._Solved_face(col):
                op = self._Solve_alg(col, opposite)
                steps, rotations = op[0] + steps, rotations + op[1]
                op = self.Final_Solve(colour)
                steps, rotations = op[0] + steps, rotations + op[1]
                return steps, rotations

        start = self.faces[colour].location[0]
        op = self._Solve_alg(start, opposite)
        steps, rotations = op[0] + steps, rotations + op[1]
        op = self.Final_Solve(colour)
        steps, rotations = op[0] + steps, rotations + op[1]
        return steps, rotations


    def _Solve_alg(self, colour, loc):
        steps, rotations = 0, []
        op = self.right_alg(colour, loc)
        steps, rotations = op[0] + steps, rotations + op[1]
        op = self.left_alg(colour, loc)
        steps, rotations = op[0] + steps, rotations + op[1]

        count = 0
        while count < 5:
            op = self.right_alg(colour, loc)
            steps, rotations = op[0] + steps, rotations + op[1]
            count += 1

        while count > 0:
            op = self.left_alg(colour, loc)
            steps, rotations = op[0] + steps, rotations + op[1]
            count -= 1

        return steps, rotations

    def _Solved_face(self, colour):
        for row in self.faces[colour].grid:
            if not all(col == colour for col in row):
                return False
        return True

    def clean_data(self, rotations: List[List[Any]]) -> List[List[Any]]:
        """turn every starting rotation point to be R, B, W"""
        pass

    def Solve(self):
        faces = self.copy()
        # print(self.faces['R'].location)
        # print(faces['R'].location)
        total = float('inf')
        rotations = []
        for colour in 'RGYOBW':
            curr_steps, curr_rot = 0, []
            steps = self.Cross(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Corners(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Fix_sides(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Top_cross(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Top_corners(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Invert(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Top_corners(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            steps = self.Final_Solve(colour)
            curr_rot += steps[1]
            curr_steps += steps[0]
            self.faces = {key: item.copy() for key, item in faces.items()}
            # print(self.faces)
            if curr_steps < total:
                total, rotations = curr_steps, curr_rot
                # print(rotations)
        return total, rotations



if __name__ == '__main__':
    import time
    start = time.time()
    a = Solution()

    # fixed_scramble = [['W', 'O', 2], ['W', 'G', 0], ['R', 'B', 0], ['B', 'Y', 0], ['W', 'G', 0], ['Y', 'O', 0], ['G', 'O', 2], ['B', 'W', 0], ['G', 'Y', 0], ['O', 'G', 2], ['B', 'O', 2], ['O', 'G', 0], ['Y', 'G', 2], ['O', 'Y', 2], ['W', 'R', 2], ['G', 'O', 2], ['O', 'W', 2], ['B', 'O', 0], ['G', 'Y', 2], ['G', 'O', 0], ['R', 'G', 0], ['G', 'R', 0], ['G', 'W', 0], ['Y', 'B', 0], ['W', 'B', 2], ['W', 'G', 0], ['B', 'O', 2], ['R', 'B', 0], ['B', 'O', 0], ['B', 'W', 2], ['B', 'W', 0], ['Y', 'G', 2], ['W', 'B', 2], ['Y', 'B', 0], ['O', 'B', 0], ['G', 'W', 0], ['B', 'Y', 0], ['R', 'Y', 0], ['O', 'G', 0], ['W', 'G', 0], ['G', 'W', 2], ['B', 'O', 2], ['O', 'W', 0], ['W', 'O', 2], ['O', 'G', 0], ['W', 'O', 0], ['G', 'Y', 2], ['Y', 'B', 2], ['O', 'G', 2], ['G', 'Y', 0], ['R', 'B', 0], ['G', 'Y', 2], ['Y', 'R', 0], ['R', 'G', 0], ['W', 'B', 2], ['Y', 'B', 2], ['Y', 'O', 0], ['Y', 'O', 0], ['Y', 'G', 0], ['B', 'W', 2], ['Y', 'G', 0], ['R', 'G', 0], ['B', 'R', 2], ['Y', 'R', 2], ['R', 'Y', 0], ['W', 'O', 0], ['R', 'Y', 0], ['Y', 'R', 2], ['B', 'O', 2], ['Y', 'B', 2], ['O', 'Y', 2], ['B', 'R', 0], ['B', 'O', 0], ['Y', 'B', 2], ['Y', 'R', 0], ['R', 'Y', 2], ['O', 'W', 0], ['B', 'R', 0], ['O', 'G', 2], ['Y', 'G', 0], ['O', 'W', 0], ['B', 'O', 2], ['G', 'Y', 0], ['B', 'R', 2], ['O', 'W', 0], ['W', 'R', 2], ['G', 'W', 0], ['W', 'B', 2], ['G', 'O', 2], ['R', 'B', 2], ['R', 'G', 0], ['G', 'R', 0], ['O', 'Y', 0], ['Y', 'B', 2], ['B', 'R', 0], ['B', 'O', 0], ['Y', 'O', 0], ['B', 'O', 2], ['G', 'R', 0], ['R', 'G', 0]]
    # for i in fixed_scramble:
    #     a.rotate(*i)
    total = 0
    for COLOUR in 'RGWYBO':
        for i in range(500):
            a.Scramble()
            total += a.Cross(COLOUR)[0]
            total += a.Corners(COLOUR)[0]
            total += a.Fix_sides(COLOUR)[0]
            # print(a)
            # print("="*100)
            total += a.Top_cross(COLOUR)[0]
            # print(a)
            total += a.Top_corners(COLOUR)[0]
            # print("="*100)
            # print(a)
            total += a.Invert(COLOUR)[0]
            # print("="*100)
            # print(a)
            total += a.Top_corners(COLOUR)[0]
            # print("="*100)
            # print(a)
            total += a.Final_Solve(COLOUR)[0]
            # print("="*100)
            # print(a)
            for c in 'RGWYBO':
                assert a._Solved_face(c)
    # highest = float('inf')
    print(total // 3000)

    # for i in 'RGBYWO':
    #     a.scramble()
    #     val = 0
    #     val += a.Cross('W')[0]
    #     val += a.Corners('W')[0]

    #     if val < highest:
    #         highest = val
    #         colour = i



    # print(f'took {time.time() - start} seconds with {colour} and {highest} steps')
    # print(a)
    # print(new)