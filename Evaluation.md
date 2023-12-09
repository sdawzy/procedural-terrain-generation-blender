## Evaluation of the Algorithms
Here is the evaluation of our algorithms.

## Perlin Noise
The key features of the Perlin Noise include gradient vectors, smoothing, linear interpolation, and blending different octaves (higher octave has higher subdivision of the grid 
that we generate the noise on). Perlin Noise is highly adaptable and can generate detailed patterns, which menas that local changes are supported. However, the iteration in our 
code that supports the octaves/subdivisions runs exponentially as we recursively subdivide each original cell into four in every subsequent round.  

## Diamond-Square
The Diamond-Square algorithm relies on random values, especially the four corners where the algorithm begins with. In both the "diamond" and "square" part of the algorithm, a random displacement is added to the mean value of the four neighboring values. Since we are computing the mean, the height of the terrain at each point depends very much on the random displacement added. The algorithm runs much faster than the Perlin Noise because it only depends on how many cells we subdivide the grid upon initialization and there is no recursion going on.

## Worley (Voronoi) Noise
We relied on the built-in geometry node and textures for generatingthe Worley noise. The terrain generated tend to have the "cell" look of a 2D Voronoi diagram if viewed from the top orthographic direction but is less easy to tell when the "detail" parameter increases in number.
Due to the nature of the voronoi diagram, the terrain generated looks much different to the other two noises, mostly in terms of shape.

## Something Else That We Wanna Say...
All the algorithms above achieve the goal of generating a terrain that imitates a landscape: there are heights and by using different colors we create different meanings for different levels of height. Mostly we color the terrain (from low to high) in terms of sea, land, mountain, and snow on the mountain, but we are also able to generate different kinds of landscapes, such as desert or volcano. 
However, perhaps due to the nature of these algorithms, so far we are unable to mimic a river without using non-algorithmic tools from blender itself to generate rivers, or anything that have a more "global feature" that we can tell by just looking at the terrain generated. We are able to generate mass portion of sea with blobs of islands and we are able to genereate vast grassland with a few ponds. We hope to be able to achieve this in the near future with algorithms.
