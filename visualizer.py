from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.patches as patches
from rubiks import *
from solution import Solution

# default face for red
col_con = {'R': 'red', 'G': 'green', 'B': 'blue', 'O': 'orange', \
           'Y': 'yellow', 'W': 'white'}

# x axis is the red face pointing at you
X = [*[1]*16]
Y = [*[1, 1/3, -1/3, -1]*4]
Z = [*[1] * 4, *[1/3]*4, *[-1/3]*4, *[-1]*4]

def rotate(x, y, z, axis='Z', times=1):
    '''return a copy of rotated variables default rotation is 90 degrees
    if times is a multiplier of the rotation angle can be any real number'''
    New_X = []
    New_Y = []
    New_Z = []
    if axis == 'Z':
        for a, b, c in zip(x, y, z):
            New_X.append(np.cos(np.pi * times / 2) * a - np.sin(np.pi * times / 2) * b)
            New_Y.append(np.sin(np.pi * times / 2) * a + np.cos(np.pi * times / 2) * b)
            New_Z.append(c)

    elif axis == 'Y':
        for a, b, c in zip(x, y, z):
            New_X.append(np.cos(np.pi * times / 2) * a + np.sin(np.pi * times / 2) * c)
            New_Y.append(b)
            New_Z.append(- np.sin(np.pi * times / 2) * a + np.cos(np.pi * times / 2) * c)

    return New_X, New_Y, New_Z

def generate(colour_grid, center, x, y, z):
    '''generates the faces'''
    faces = {}
    a = [np.array([c, d, e]) for c, d, e in zip(x, y, z)]

    verts = []
    for i in [0, 1, 2, 4, 5, 6, 8, 9, 10]:
        verts.append([a[i], a[i + 1], a[i + 5], a[i + 4]])

    for ind, c, v in zip(range(9), colour_grid, verts):
        if f'{center}{ind}' not in faces:
            faces[f'{center}{ind}'] = Poly3DCollection([v], 
         facecolors=col_con[c], linewidths=1, edgecolors='black', alpha=1)
        ax.add_collection3d(faces[f'{center}{ind}'])

    return faces

def plot(rubiks):
    a = [1, 1, 1, 1, -1, -1, -1, -1]
    b = [1, 1, -1, -1, 1, 1, -1, -1]
    c = [1, -1, 1, -1, 1, -1, 1, -1]
    poly3Dobjects = {}
    colours = rubiks.visualizer_string()
    ax.scatter(a, b, c, c='black', marker= ' ')
    poly3Dobjects.update(generate(colours['G'], 'G', *rotate(X, Y, Z, times=1)))
    poly3Dobjects.update(generate(colours['O'], 'O', *rotate(X, Y, Z, times=2)))
    poly3Dobjects.update(generate(colours['B'], 'B', *rotate(X, Y, Z, times=3)))
    poly3Dobjects.update(generate(colours['Y'], 'Y', *rotate(X, Y, Z, axis = 'Y', times=-1)))
    poly3Dobjects.update(generate(colours['W'], 'W', *rotate(X, Y, Z, axis = 'Y', times=1)))
    poly3Dobjects.update(generate(colours['R'], 'R', X, Y, Z))
    # fig.canvas.draw_idle()
    return poly3Dobjects

def update_3d_plot():
    colours = b.visualizer_string()
    for center in colours:
        for ind, c in zip(range(9), colours[center]):
            poly3Dobjects[f'{center}{ind}'].set_facecolor(col_con[c])
    fig.canvas.draw_idle()

def rotate1():
    global COLOURS
    global INDEX 

    a.rotate('R', *COLOURS[INDEX % 4])
    INDEX = (INDEX + 1) % 4
    update_3d_plot()

def Solve():
    try:
        b.rotate(*SOLUTION_ORDER.pop())
        update_3d_plot()

    except IndexError:
        pass


# def top(event):

# def top_prime(event):

# def left(event):

# def left_prime(event):

# def right(event):

# def right_prime(event):

# def bottom(event):

# def bottom_prime(event):

if __name__ == '__main__':
    import time
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt.axis('off')
    ax.grid(False)
    ax.set_aspect('equal')
    INDEX = 0
    COLOURS = [('Y', 2), ('B', 2), ('W', 0), ('G', 0)]
    # plt.show()
    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.set_zticks([])
    # ax.set_xlabel('x axis')
    # ax.set_ylabel('y axis')
    # ax.set_zlabel('z axis')
    lowest = float('inf')
    a = Solution(Rubiks_Cube().faces)
    scramble = a.scramble()
    # print(scramble)
    for COLOUR in 'RGWYBO':
        total = 0

        op, ROTATION_ORDER = a.Cross('Y')
        total += op

        op, rotation = a.Corners('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Fix_sides('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Top_cross('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Top_corners('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Invert('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Top_corners('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        op, rotation = a.Final_Solve('Y')
        ROTATION_ORDER.extend(rotation)
        total += op

        ROTATION_ORDER = ROTATION_ORDER[::-1]
        COPY = ROTATION_ORDER[:]

        for i in scramble:
            a.rotate(*i)

        if total < lowest:
            lowest = total
            SOLUTION_ORDER = ROTATION_ORDER
        
    # print(a)
    # print(ROTATION_ORDER)
    b = Solution(Rubiks_Cube().faces)

    for i in scramble:
        b.rotate(*i)

    print(lowest)

    # a.scramble()
    # a.Cross('G')
    # a.Corners('G')
    poly3Dobjects = plot(b)

    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(Solve)
    timer.start()

    # button_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
    # color_button = Button(button_ax, "L'", hovercolor='0.975')
    # color_button.on_clicked(left_prime)



    plt.show()
    # ax.scatter(*rotate(X, Y, Z, times=1), c='black', marker= ' ')
    # ax.scatter(*rotate(X, Y, Z, axis = 'Y', times=1), c='black', marker=' ')

    # print(colours)
    # generate(colours['G'], 'G', *rotate(X, Y, Z, times=1))
    # generate(colours['O'], 'O', *rotate(X, Y, Z, times=2))
    # generate(colours['B'], 'B', *rotate(X, Y, Z, times=3))
    # generate(colours['Y'], 'Y', *rotate(X, Y, Z, axis = 'Y', times=-1))
    # generate(colours['W'], 'W', *rotate(X, Y, Z, axis = 'Y', times=1))
    # generate(colours['R'], 'R', X, Y, Z)
    # plt.yscale('linear')
    # plt.show()