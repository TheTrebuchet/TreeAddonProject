# TreeAddonProject

I assume that if you wandered into the files of this addon, you would like to know more or less how it works. Below I will try to explain to you a bit of the code.
If you have any suggestions for improvement contact me at jan.kulczycki1@gmail.com, I will be happy to improve on anything.

## Functions

the whole 'tree' of functions looks like this:

`tree_gen`

- `trunk_gen`
  - `spine_gen`
    - `spine_init`
    - `spine_bend`
  - `bark_gen`
    - `bark_circle`
  - `bark_faces`
- `branch_gen`
  - `branch_guides`
  - `trunk_gen`

descriptions

- `trunk_gen` uses three functions below it to create a trunk
- `spine_gen` uses two functions to create a list of vertices that resemble a spine
- `spine_init` creates a list of points controlled by perlin parameters and main parameters, it is already rotated according to the guide
- `spine bend` is truly the core of this algorithm, see comments in treegen.py for specifics. It creates the spine step by step in a maybe-physically-accurate manner.
- `bark_gen` creates circles along the spine. Scaling is controlled some functions and rotation controlled by the spine and guide
- `bark_circle` just creates a circle at 000
- `bark_faces` creates links between points to form faces, it only needs number of sides and number of vertices on the spine
- `branch_gen` is responsible for making sure the trunk_gen output is handled correctly by the guides, outputs semi-ready branches verts list and appends to faces
- `branch_guides` is creating vectors and additional parameters for the branches generated on the trunk or branch specified in the input

I am registering quite a few classes. Respectively, three operators to create a tree, update it when you change a parameter and sync the panel with selected tree. 
Then you have the panel itself and a property group of all the properties.

`[treegen.TreeGen_new, treegen.TreeGen_update, treegen.TreeGen_sync, property_group.TreeGen_PG, treegen.OBJECT_PT_TreeGenerator]`
