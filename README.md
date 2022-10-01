# TreeAddonProject

## Functions

the whole tree looks like this:

tree_gen
- spine_gen
    - spine_init
    - spine_bend
- bark_gen
    - bark_circle
- bark_faces

- tree_gen uses three functions below it to create a trunk
- spine_gen uses two functions to create a list of vertices that resemble a spine
- spine_init creates a list of points controlled by perlin parameters and main parameters, it is already rotated according to the guide
- bark_gen creates circles along the spine. Scaling is controlled by executable file functions and rotation controlled by the spine and guide
- bark_circle just creates a circle 
- bark_faces creates link between points to form faces, it only needs number of sides and number of vertices on the spine


branch_gen
- tree_gen

- branch_gen uses tree_gen to create "trunks" on the main trunk, everything is controlled by guides outputted by the tree_gen

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
