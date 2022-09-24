# TreeAddonProject

## Functions

let's start from the beginning

### spine_gen

`spine_gen` is depending on `spine_init` and `spine_bend`
`spine_init` creates a basic line of points, it takes n, length, perlin noise attributes and jiggles the points a bit
`spine_bend` actually displaces the spine, takes spine, perlin noise attributes and length. It works as follows:

- generates random `xrot` and `zrot`, uses many matrices to bend the whole tree above a certain point by an `xrot` angle along an axis determined by `zrot`
- if the angle is such that a tree starts bending too much towards earth, a correction to `zrot` is applied.

The angle should be adjustable in the future, and it doesn't seem to work with large bends
then it returns spine
The function should take a starting vector and go vaguely in its direction, maybe changing it over time towards "sun"

### bark_gen

creates bark, understandably, takes the spine and creates points around it.
There is a function `f` for scale of circles inside, should be an adjustable curve in the future.
It gets the vector from one spine point to another, generates a circle, scales it and rotates to that vector
should be a vector as a median between three points, so that it works better with large bends.

### branch_guides

now it creates a vector, which size should be a scale of the vector, placed on the bark, where a branch should be generated

### tree_gen

should create a tree as a whole
`spine_gen` and `bark_gen` should work in a loop while `branch_guides` creates places for them to work on, that's what tree_Gen does, it tackles this loop

## Parameters

config file basics:

### MAIN PARAMETERS

sides
length
radius
scale

### RANDOM PARAMETERS

perlin = True
perlin_amount
perlin_scale
perlin_seed

bends = True
bends_amount
bends_scale
bends_seed

### SIDE PARAMETERS

angle = 4.7
d = 5

m_p = [sides, length, radius, scale]
s_p = [angle, d]
r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_scale, bends_seed]
