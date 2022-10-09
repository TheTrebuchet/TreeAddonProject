# TreeAddonProject

## Functions

the whole tree looks like this:

tree_gen

- trunk_gen
  - spine_gen
    - spine_init
    - spine_bend
  - bark_gen
    - bark_circle
  - bark_faces
- branch_gen
  - branch_guides
  - trunk_gen

descriptions

- `trunk_gen` uses three functions below it to create a trunk
- `spine_gen` uses two functions to create a list of vertices that resemble a spine
- `spine_init` creates a list of points controlled by perlin parameters and main parameters, it is already rotated according to the guide
- `bark_gen` creates circles along the spine. Scaling is controlled by executable file functions and rotation controlled by the spine and guide
- `bark_circle` just creates a circle
- `bark_faces` creates link between points to form faces, it only needs number of sides and number of vertices on the spine
- `branch_gen` is responsible for making sure the trunk_gen output is handled correctly by the guides, outputs semi-ready branches verts list and appends to faces
- `branch_guides` is creating vectors and additional parameters for the branches generated on the trunk or branch specified in the input

branch_gen uses tree_gen to create "trunks" on the main trunk, everything is controlled by guides outputted by the tree_gen

## config file basics

``` python
# MAIN PARAMETERS
sides = 10
length = 100
radius = 4
scale = 0.1
ratio = 2

# RANDOM PARAMETERS
perlin = True
perlin_amount = 0.01
perlin_scale = 0.05
perlin_seed = 3

bends_amount = 0.5
bends_angle = 90
bends_correction = 0.2
bends_scale = 0.1
bends_seed = 8

# BRANCH PARAMETERS
branch_levels = 2
branch_number1 = 30
branch_number2 = 5
branch_number3 = 2
branch_angle = 70
branch_height = 0.3
branch_weight = 0.5
branch_variety = 0.1
branch_seed = 1

# temporary parameters
flare_amount = 0.1
scale_lf1 = lambda x, h, r, a: (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
branch_width = 30
branch_flare = 1.2
scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #this one is for branches scale
```

there are also functions for trunk flare and branches scale
the first one is mostly a mix between y=-x and y = 1/x, the mixing is controlled by `h`, `r` and `a`
where we have height of the tree, radius and amount of the flare
the second one is based on this function
$$ \left(x-1\right)^{2}+a^{\left(x-1\right)}\cdot y^{2}=r $$
where `a` is the variable making the branches larger in the top of the tree or the bottom
TODO: you will be able to use your own functions or the blender graph thing
