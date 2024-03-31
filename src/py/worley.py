import bpy
import math
import random
from math import fabs

def smoothing(val):
    return 6 * (val ** 5) - 15 * (val ** 4) + 10 * (val ** 3)

def generate_worley(width=10, n=36, size=4.0, z=1.0, random_range=1.0,
        noise_range=0.003, sea_level = 0.2):

    resolution = width * n

    grid = [[0]*width for _ in range(width)]
    weights = [[0]*width for _ in range(width)]
    depth = [[0]*width for _ in range(width)]
    pixels = [[random.uniform(-noise_range, noise_range) for _ in range(resolution) ]
        for _ in range(resolution)]
    distances = [[0]*resolution for _ in range(resolution)]

    # initialize grid points
    for i in range(width):
        for j in range(width):
            grid[i][j] = (random.uniform(0,1)+i, random.uniform(0,1)+j)
            weights[i][j] = random.uniform(random_range*0.8, random_range)
            depth[i][j] = random.uniform(-random_range*0.2, random_range*0.6)

    for i in range(resolution):
        for j in range(resolution):
            grid_x = i//n
            grid_y = j//n
            coord_x = i*1.0/n
            coord_y = j*1.0/n
            store = []
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    x = grid_x + k
                    y = grid_y + l
                    if 0 <= x < width and 0 <= y < width:
                        store.append(depth[i][j] + weights[i][j] * 
                            math.sqrt((grid[x][y][0] - coord_x)**2 + (grid[x][y][1] - coord_y)**2))
            distances[i][j] = min(1, min(store))

    for i in range(resolution):
        for j in range(resolution):
            pixels[i][j] += smoothing(distances[i][j]) * z

    # convert height into vertices
    vertices = []
    edges = []
    faces = []

    # add vertices
    for i in range(resolution):
        for j in range(resolution):
            vertices.append((-size/2+i*size/resolution, -size/2+j*size/resolution, 
                pixels[i][j] if pixels[i][j] > sea_level else sea_level + random.uniform(-noise_range,noise_range)))                

    # add faces
    for i in range(resolution-1):
        for j in range(resolution-1):
            if fabs(pixels[i][j] - pixels[i + 1][j + 1]) > fabs(pixels[i][j + 1] - pixels[i + 1][j]):
                faces.append([i*resolution+j, i*resolution+j+1, (1+i)*resolution+j])
                faces.append([(i+1)*resolution+j+1, i*resolution+j+1, (1+i)*resolution+j])
            else:
                faces.append([i*resolution+j, i*resolution+j+1, (1+i)*resolution+(j+1)])
                faces.append([i*resolution+j, (i+1)*resolution+j, (1+i)*resolution+(j+1)])

    return vertices, edges, faces

# create 
vertices, edges, faces = generate_worley(n=70, width=6, sea_level=0.15, z=0.4)
worley_mesh = bpy.data.meshes.new("worley_mesh")
worley_mesh.from_pydata(vertices, [], faces)
worley_terrain = bpy.data.objects.new("worley_terrain", worley_mesh)
terrain_collection = bpy.data.collections.new('terrain_collection')
bpy.context.scene.collection.children.link(terrain_collection)
terrain_collection.objects.link(worley_terrain)
