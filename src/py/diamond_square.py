import bpy
import random
from math import fabs

# generate a diamond square terrain
# Param:
#   n:                  Exponential of the number of vertices. Number of vertices is (2^n+1)^2
#   height_range:       Range of height
#   random_range:       Range of initial random noise
#   random_range_dec:   Decrease rate of random_range in each iteration
#   size:               Output size 
#   fixed_corner:       Whether the initial four corners have the same height
def generate_diamond_square(n=5, height_range=1.0, random_range=1.0, random_range_dec=0.5,
                            size=20.0, fixed_corner = False):

    HeightMapWidth = (1 << n)+1
    # list of heights of vertices
    heights = [[0]*HeightMapWidth for i in range(HeightMapWidth)]
    # initialize 4 corners
    if (fixed_corner):
        heights[0][0] = 0
        heights[0][HeightMapWidth - 1] = 0
        heights[HeightMapWidth - 1][0] = 0
        heights[HeightMapWidth - 1][HeightMapWidth - 1] = 0
    else:
        heights[0][0] = random.uniform(-height_range,height_range)
        heights[0][HeightMapWidth-1] = random.uniform(-height_range, height_range)
        heights[HeightMapWidth-1][0] = random.uniform(-height_range, height_range)
        heights[HeightMapWidth-1][HeightMapWidth-1] = random.uniform(-height_range, height_range)

    # average for each diamond point
    def diamond_average(x_cor, y_cor, step_width):
        return (heights[x_cor-step_width][y_cor-step_width] +
            heights[x_cor-step_width][y_cor+step_width] +
            heights[x_cor+step_width][y_cor-step_width] +
            heights[x_cor+step_width][y_cor+step_width]) / 4.0

    # average for each square point
    def square_average(x_cor, y_cor, step_width):
        # special case in boundaries
        if x_cor == 0:
            return (heights[x_cor][y_cor+step_width] +
                    heights[x_cor][y_cor-step_width] +
                    heights[x_cor+step_width][y_cor]) / 3
        if x_cor == HeightMapWidth-1:
            return (heights[x_cor][y_cor+step_width] +
                    heights[x_cor][y_cor-step_width] +
                    heights[x_cor-step_width][y_cor]) / 3
        if y_cor == 0:
            return (heights[x_cor][y_cor+step_width] +
                    heights[x_cor-step_width][y_cor] +
                    heights[x_cor+step_width][y_cor]) / 3
        if y_cor == HeightMapWidth-1:
            return (heights[x_cor][y_cor-step_width] +
                    heights[x_cor-step_width][y_cor] +
                    heights[x_cor+step_width][y_cor]) / 3
        # normal case
        return (heights[x_cor][y_cor-step_width] +
                heights[x_cor][y_cor+step_width] +
                heights[x_cor-step_width][y_cor] +
                heights[x_cor+step_width][y_cor]) / 4

    for i in range(n):
        step_width = 1 << (n-i-1)
        # diamond phase
        for j in range(1 << i):
            for k in range(1 << i):
                x_cor = step_width * (2*j+1)
                y_cor = step_width * (2*k+1)
                heights[x_cor][y_cor] = diamond_average(x_cor,y_cor,step_width) + \
                    random.uniform(-random_range, random_range)

        # square phase
        for j in range(1 << i):
            for k in range(1 << i):
                x_cor = step_width * (2*j+1)
                y_cor = step_width * (2*k)
                heights[x_cor][y_cor] = square_average(x_cor,y_cor,step_width) + \
                    random.uniform(-random_range, random_range)
                heights[y_cor][x_cor] = square_average(y_cor,x_cor,step_width) + \
                    random.uniform(-random_range, random_range)

        # boundaries of square phase
        for j in range(1 << i):
            x_cor = step_width * (2 * j + 1)
            y_cor = HeightMapWidth-1
            heights[x_cor][y_cor] = square_average(x_cor, y_cor, step_width) + \
                random.uniform(-random_range, random_range)
            heights[y_cor][x_cor] = square_average(y_cor, x_cor, step_width) + \
                random.uniform(-random_range, random_range)

        # decrease random range
        random_range *= random_range_dec

    # convert height into vertices
    vertices = []
    edges = []
    faces = []

    # add vertices
    for i in range(HeightMapWidth):
        for j in range(HeightMapWidth):
            vertices.append((-size/2+i*size/HeightMapWidth, -size/2+j*size/HeightMapWidth, heights[i][j]))

    # add faces
    for i in range(1 << n):
        for j in range(1 << n):
            if fabs(heights[i][j] - heights[i + 1][j + 1]) > fabs(heights[i][j + 1] - heights[i + 1][j]):
                faces.append([i*HeightMapWidth+j, i*HeightMapWidth+j+1, (1+i)*HeightMapWidth+j])
                faces.append([(i+1)*HeightMapWidth+j+1, i*HeightMapWidth+j+1, (1+i)*HeightMapWidth+j])
            else:
                faces.append([i*HeightMapWidth+j, i*HeightMapWidth+j+1, (1+i)*HeightMapWidth+(j+1)])
                faces.append([i*HeightMapWidth+j, (i+1)*HeightMapWidth+j, (1+i)*HeightMapWidth+(j+1)])

    return vertices, edges, faces

# create 
vertices, edges, faces = generate_diamond_square(n=8, size=8.0, fixed_corner=True)
diamond_square_mesh = bpy.data.meshes.new("diamond_square_mesh")
diamond_square_mesh.from_pydata(vertices, [], faces)
diamond_terrain = bpy.data.objects.new("diamond_square_terrain", diamond_square_mesh)
terrain_collection = bpy.data.collections.new('terrain_collection')
bpy.context.scene.collection.children.link(terrain_collection)
terrain_collection.objects.link(diamond_terrain)