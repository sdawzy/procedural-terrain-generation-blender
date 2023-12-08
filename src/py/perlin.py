import bpy
import random

def interpolate(point_0, point_1, weight):
    return point_0 + (point_1 - point_0) * weight

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


def randomGradient(grad_range):
    return Vector(random.uniform(-grad_range, grad_range),
                  random.uniform(-grad_range, grad_range))


def smoothing(val):
    return 6 * (val ** 5) - 15 * (val ** 4) + 10 * (val ** 3)


def generate_perlin_noise(iterations=3, n_row=10, n_col=10, grad_range=1.0, rand_range=1.0,
                          dec_rate=0.35, size=20.0, sea_level=0.2, std_height=True):
    heights = [[0] * n_col for _ in range(n_row)]

    for _ in range(iterations):
        n_row *= 2
        n_col *= 2
        rand_range *= dec_rate
        grad_range *= dec_rate
        vertex_vectors = [[randomGradient(grad_range) for _ in range(n_col + 1)] for _ in range(n_row + 1)]
        block_vectors = [[randomGradient(0.5) + Vector(i + 0.5, j + 0.5) for j in range(n_col)] for i in range(n_row)]
        noise_scalars = [[random.uniform(-rand_range, rand_range) for _ in range(n_col + 1)] for _ in range(n_row + 1)]

        new_heights = [[0] * n_col for _ in range(n_row)]
        heights = [[heights[i // 2][j // 2] for j in range(n_col)] for i in range(n_row)]

        for i in range(n_row):
            for j in range(n_col):
                temp_val = 0
                n_div = 0
                for k in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        x = i + k
                        y = j + l
                        if 0 <= x < n_row and 0 <= y < n_col:
                            n_div += 1
                            temp_val += heights[x][y]
                new_heights[i][j] = temp_val / n_div

        heights = new_heights

        for i in range(n_row):
            for j in range(n_col):
                noise = 0
                for layer in range(iterations):
                    noise += interpolate(
                        interpolate(((block_vectors[i][j] - Vector(i, j)) * vertex_vectors[i][j]) +
                                    noise_scalars[i][j],
                                    ((block_vectors[i][j] - Vector(i, j + 1)) * vertex_vectors[i][j + 1]) +
                                    noise_scalars[i][j + 1],
                                    smoothing((block_vectors[i][j] - Vector(i, j)).y)),
                        interpolate(((block_vectors[i][j] - Vector(i + 1, j)) * vertex_vectors[i + 1][j]) +
                                    noise_scalars[i + 1][j],
                                    ((block_vectors[i][j] - Vector(i + 1, j + 1)) * vertex_vectors[i + 1][j + 1]) +
                                    noise_scalars[i + 1][j + 1],
                                    smoothing((block_vectors[i][j] - Vector(i, j)).y)),
                        smoothing((block_vectors[i][j] - Vector(i, j)).x)
                    )
                heights[i][j] += noise


    # Generate faces based on the Delaunay triangulation
    if std_height:
        min_height = 19260817
        max_height = -19260817
        for i in range(n_row):
            for j in range(n_col):
                min_height = min(min_height, heights[i][j])
                max_height = max(max_height, heights[i][j])

        heights = [[(heights[i][j] - min_height) / (max_height - min_height)
                    for j in range(n_col)] for i in range(n_row)]

    vertices = [(-size / 2 + i / n_row * size, -size / 2 + j / n_col * size,
                 heights[i][j] if heights[i][j] > sea_level else sea_level+random.uniform(-rand_range, rand_range))
                for j in range(n_col) for i in range(n_row)]

    faces = []
    for j in range(n_col - 1):
        for i in range(n_row - 1):
            faces.extend([[i + j * n_col, i + (j + 1) * n_col, (i + 1) + j * n_col],
                          [(i + 1) + j * n_col, i + (j + 1) * n_col, (i + 1) + (j + 1) * n_col]])

    return vertices, faces


vertices, faces = generate_perlin_noise(iterations=6, n_row=6, n_col=6, grad_range=1, rand_range=1,
                                        size=4.0, sea_level=0.2)
perlin_mesh = bpy.data.meshes.new("perlin_mesh")
perlin_mesh.from_pydata(vertices, [], faces)

perlin_terrain = bpy.data.objects.new("perlin_terrain", perlin_mesh)
terrain_collection = bpy.data.collections.new('terrain_collection')
bpy.context.scene.collection.children.link(terrain_collection)
terrain_collection.objects.link(perlin_terrain)