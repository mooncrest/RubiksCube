import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# from matplotlib.widgets import Slider, Button, RadioButtons
from solution import Solution
STEPS = 4

def X_rotation_matrix(steps):
    steps = steps * 2
    rotation_matrix = np.array([1, 0, 0, 0, np.cos(np.pi/steps), np.sin(np.pi/steps), \
                                0, -np.sin(np.pi/steps), np.cos(np.pi/steps)])
    return rotation_matrix.reshape((3, 3))

def Y_rotation_matrix(steps):
    steps = steps * 2
    rotation_matrix = np.array([np.cos(np.pi/steps), 0, np.sin(np.pi/steps), 0, 1, 0, -np.sin(np.pi/steps), 0, np.cos(np.pi/steps)])
    return rotation_matrix.reshape((3, 3))

def Z_rotation_matrix(steps):
    steps = steps * 2
    rotation_matrix = np.array([np.cos(np.pi/steps), -np.sin(np.pi/steps), 0, np.sin(np.pi/steps), np.cos(np.pi/steps), 0, 0, 0, 1])
    return rotation_matrix.reshape((3, 3))

translations = [np.array([a, b, c]) for a in (2, 0, -2) for b in (2, 0, -2) for c in (2, 0, -2)]
points = [np.array([a, b, c]) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
verticies = [points[0:4], points[4:8], points[0:2] + points[4:6], points[2: 4] + points[6: 8], points[0:8:2], points[1:8:2]] 
verticies = [i[0: 2] + i[3: 1: -1] for i in verticies]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
poly3d_objects = []

for translation in translations:
    translated = [[vert + translation for vert in face] for face in verticies]
    cube = []
    for col, vert in zip(['red', 'orange', 'blue', 'green', 'white', 'yellow'], translated):   
        # print(np.array([np.array(i) for i in vert] ))
        # print([vert])
        poly3d = Poly3DCollection([np.array([np.array(i) for i in vert])], facecolor=col, linewidths=1)
        poly3d.set_edgecolor('black')
        ax.add_collection3d(poly3d)
        cube.append((poly3d, vert))
    poly3d_objects.append(cube)

def rotation():
    if ROTATION_ORDER == []:
        return False
    rotation = ROTATION_ORDER.pop()
    if rotation[0] == 'X':
        rot = X_rotation_matrix(rotation[3])
    elif rotation[0] == 'Y':
        rot = Y_rotation_matrix(rotation[3])
    else:
        rot = Z_rotation_matrix(rotation[3])

    for cube in poly3d_objects:
        if any(rotation[2] == round(vert[rotation[1]]) for poly in cube for vert in poly[1]):
            for poly in cube:
                for ind, vert in enumerate(poly[1]):
                    poly[1][ind] = np.matmul(vert, rot) 
                poly[0].set_verts([poly[1]])

    fig.canvas.draw_idle()    
    return True


ax.set_aspect('equal')
ax.set_xlim3d(-3, 3)
ax.set_ylim3d(-3, 3)
ax.set_zlim3d(-3, 3)
plt.axis('off')
# RIGHT_ALG = [['R', 'Y', 2], ['R', 'B', 2], ['R', 'W', 0], ['R', 'G', 0]] # test1
# RIGHT_ALG = [['W', 'R', 2], ['W', 'B', 2], ['W', 'O', 0], ['W', 'G', 0]]
CUBE = Solution()
SCRAMBLE = CUBE.Scramble()
SCRAMBLE = CUBE.parse_rotation(SCRAMBLE, 1)
ROTATIONS = CUBE.Solve()
print(len(ROTATIONS))
ROTATION_ORDER = CUBE.parse_rotation(ROTATIONS, STEPS) + SCRAMBLE
timer = fig.canvas.new_timer(interval=50)
timer.add_callback(rotation)
timer.start()
plt.show()           






































































































































































































