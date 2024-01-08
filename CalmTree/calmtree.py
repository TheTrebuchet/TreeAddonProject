import bpy
import bmesh
import os
import time
import subprocess
from .geogroup import *
from .algorithm import *
from .generative import *
from .leafmat import *
from .barkmat import *


class global_parameters:
    def __init__(self):
        tps = bpy.data.window_managers["WinMan"].calmtree_props

        l = tps.Mlength / tps.Mvres
        self.m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mtipradius, tps.Mscale, l]
        self.br_p = [
            tps.branch_levels,
            tps.branch_minangle,
            tps.branch_maxangle,
            tps.branch_height,
            tps.branch_horizontal,
            tps.branch_variety,
            tps.branch_scaling,
            tps.branch_seed,
        ]
        self.bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        self.bd_p = [
            tps.bends_amount,
            tps.bends_up,
            tps.bends_correction,
            tps.bends_scale,
            tps.bends_weight / (tps.Mlength),
            tps.bends_seed,
        ]
        self.r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]
        self.e_p = [tps.interp, tps.poisson_type, tps.poisson_qual, tps.leaffactor]
        self.d_p = [tps.Ythreshold, max(tps.Tthreshold * tps.Mlength, 2 * l)]
        self.facebool = tps.facebool

        self.lim = lambda x: 1 / (x * self.bn_p[0] + (1 - x) * self.bn_p[1])
        
        # this one is for trunk flare
        fa=tps.flare_amount
        self.scale_f1 = lambda x: 1-x+fa*(1-x)**10
        # this one is for branches scale depending on their placement on a tree
        bs = tps.branch_shift
        self.scale_f2 = lambda x: (4*x*(1-x)*((1-bs**2)**0.5+1)/(2*(bs*(2*x-1)+1)))**(0.5+0.5*abs(bs))
    
    def extract(self):
        pars = [self.m_p, self.br_p, self.bn_p, self.bd_p, self.r_p, self.e_p, self.d_p, self.facebool, self.facebool]
        for i in pars:
            print(i)

class timer():
    def __init__(self):
        self.times = {}
    def start(self, name):
        self.times[name] = time.time()
    def stop(self, name):
        self.times[name] = time.time()-self.times[name]
    def display(self):
        total = max([float(t) for t in self.times.values()])
        for i in self.times.keys():
            print(str(i)+ ' took: ' + str(self.times[i]) + ' ' + str(100*self.times[i]/total)+'%')

def checkedit(context):
    config = context.object["CalmTreeConfig"]
    for i in config.split(","):
        if "edit" in i:
            if "True" in i:
                return True
            if "False" in i:
                return False


def saveconfig():
    tps = bpy.data.window_managers["WinMan"].calmtree_props
    config = ""
    excluded = ["__", "rna", "sync"]
    for new in dir(tps):
        if not any(x in new for x in excluded):
            config += new + "=" + str(getattr(tps, new)) + ","
    return config


def geonode():
    if "CalmTree_nodegroup" not in bpy.data.node_groups:
        CalmTree_nodegroup_exec()
    ng = bpy.data.node_groups["CalmTree_nodegroup"]
    if "CalmTree" not in bpy.context.object.modifiers:
        bpy.context.object.modifiers.new(name="CalmTree", type="NODES")
    geo_mod = bpy.context.object.modifiers["CalmTree"]
    if not geo_mod.node_group:
        geo_mod.node_group = ng
    bpy.ops.object.geometry_nodes_input_attribute_toggle(
        prop_path='["Input_1_use_attribute"]', modifier_name="CalmTree"
    )
    bpy.context.object.modifiers["CalmTree"]["Input_1_attribute_name"] = "leaves"


class CALMTREE_OT_new(bpy.types.Operator):
    """creates a tree at (0,0,0) according to user panel input"""

    bl_idname = "object.tree_create"
    bl_label = "Place a tree"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        debug = timer() #TIMER
        debug.start('whole') #TIMER
        tps = context.window_manager.calmtree_props

        pars = global_parameters()
        pars.extract()
        seeds = [pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1]]
        # generates the trunk and lists of lists of branches
        st_pack = [Vector((0, 0, 0)), Vector((0, 0, pars.m_p[1])), pars.m_p[2], 0]


        if tps.engine == "classic":
            debug.start('classic') #TIMER
            stbran = branch(st_pack, pars, True)
            stbran.generate_classic(pars)
            branchlist = [[stbran]]
            branchlist = outgrow_classic(branchlist, pars)
            verts, edges, faces, selection, info = toverts(branchlist, pars)
            debug.stop('classic') #TIMER

        elif tps.engine == "dynamic":
            debug.start('dynamic') #TIMER
            stbran = branch(st_pack, pars, True)
            stbran.generate_dynamic(pars)
            branchlist = [stbran]
            branchlist = outgrow_dynamic(branchlist, pars)
            verts, edges, faces, selection, info = toverts(branchlist, pars)
            debug.stop('dynamic') #TIMER

        # creating the tree
        debug.start('object placement') #TIMER
        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)
        bpy.context.collection.objects.link(object)
        mesh.from_pydata(verts, edges, faces)

        # name of the created object and selecting it
        bpy.ops.object.select_all(action="DESELECT")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.shade_smooth()
        object.matrix_world.translation = context.scene.cursor.location
        debug.stop('object placement') #TIMER

        debug.start('post stuff') #TIMER
        # adding vertex group for furthest branches
        if selection:
            v_group = object.vertex_groups.new(name="leaves")
            v_group.add(selection, 1.0, "ADD")

        # writing properties
        tps.treename = context.object.name
        pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1] = seeds
        context.object["CalmTreeConfig"] = saveconfig()
        context.object["CalmTreeLog"] = info

        if tps.leafbool:
            geonode()
            bpy.ops.object.tree_leaf()
            context.object.modifiers["CalmTree"].show_viewport = False
            context.object.modifiers["CalmTree"].show_viewport = True
        if tps.matbool:
            bpy.ops.object.tree_mat()
        
        debug.stop('post stuff') #TIMER
        debug.stop('whole') #TIMER
        debug.display()

        #testing implementation of binary to speed things up
        directory = os.path.dirname(os.path.realpath(__file__))
        enginepath=directory + "/engine"
        popen = subprocess.Popen(enginepath, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        print(output)
        
        return {"FINISHED"}


class CALMTREE_OT_update(bpy.types.Operator):
    """updates the tree according to user panel input"""

    bl_idname = "object.tree_update"
    bl_label = "update the tree object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        tps = context.window_manager.calmtree_props
        try:
            bpy.context.object["CalmTreeConfig"]
        except:
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {"FINISHED"}
        
        tree_obj = bpy.context.object
        custom_child = [o for o in tree_obj.children if "custom trunk" in o.name]

        if len(custom_child) > 1:
            self.report(
                {"INFO"},
                "I detected multiple viable trunks in the trees children, leave only one",
            )
            return {"FINISHED"}

        pars = global_parameters()
        seeds = [pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1]]

        # generates the trunk and lists of lists of branches
        st_pack = [Vector((0, 0, 0)), Vector((0, 0, pars.m_p[1])), pars.m_p[2], 0]

        if tps.engine == "classic":
            stbran = branch(st_pack, pars, True)
            stbran.generate_classic(pars)
            branchlist = [[stbran]]
            branchlist = outgrow_classic(branchlist, pars)
            verts, edges, faces, selection, info = toverts(branchlist, pars)
        
        elif tps.engine == "dynamic":
            stbran = branch(st_pack, pars, True)
            stbran.generate_dynamic(pars)
            branchlist = [stbran]
            branchlist = outgrow_dynamic(branchlist, pars)
            verts, edges, faces, selection, info = toverts(branchlist, pars)

        # updating mesh, tree update is a temporary object
        t_mesh = bpy.data.meshes.new("tree update")
        t_mesh.from_pydata(verts, edges, faces)

        bm = bmesh.new()
        bm.from_mesh(t_mesh)

        bm.to_mesh(tree_obj.data)
        bm.free()
        bpy.data.meshes.remove(t_mesh)
        for f in tree_obj.data.polygons:
            f.use_smooth = True

        v_group = bpy.context.object.vertex_groups["leaves"]
        v_group.remove([i for i in range(len(verts))])
        v_group.add(selection, 1.0, "REPLACE")

        pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1] = seeds
        context.object["CalmTreeConfig"] = saveconfig()
        context.object["CalmTreeLog"] = info
        return {"FINISHED"}


class CALMTREE_OT_draw(bpy.types.Operator):
    """let's the user edit the trunk"""

    bl_idname = "object.tree_draw"
    bl_label = "draw a new trunk"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.curve.primitive_bezier_curve_add(
            enter_editmode=True,
            align="WORLD",
            location=(0, 0, 0),
            rotation=(0, math.pi / 2, 0),
        )
        bpy.ops.transform.translate(value=(0, 0, 5))
        bpy.ops.transform.resize(value=(3.0, 3.0, 5.0))
        bpy.ops.object.mode_set(mode="OBJECT")
        context.active_object.matrix_world.translation = context.scene.cursor.location
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        context.object["CalmTreeConfig"] = "to be generated"
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


class CALMTREE_OT_regrow(bpy.types.Operator):
    """regrows tree from line of points"""

    bl_idname = "object.tree_regrow"
    bl_label = "regrow from existing curve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        tps = context.window_manager.calmtree_props
        tps.ops_complete = False
        try:
            bpy.context.object["CalmTreeConfig"]
        except:
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {"FINISHED"}
        curve = []

        curve_obj = context.active_object
        bpy.ops.object.mode_set(mode="OBJECT")
        obj = bpy.context.active_object
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        obj.data.vertices[0].select = True
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_linked(delimit=set())
        bpy.ops.object.mode_set(mode="OBJECT")
        curve = [v.co for v in obj.data.vertices if v.select]

        if curve[-1].length < curve[0].length:
            curve.reverse()

        context.scene.cursor.location = curve[0] + curve_obj.location
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        curve_obj.location = (0, 0, 0)

        tps.Mlength = sum(
            [(curve[i + 1] - curve[i]).length for i in range(len(curve) - 1)]
        )
        tps.Mscale = 1
        tps.Mvres = len(curve)
        pars = global_parameters()
        seeds = [pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1]]

        # generates the trunk and lists of lists of stuff
        branchlist = branchinit(curve, pars.m_p, pars.bd_p, pars.br_p, pars.r_p)
        branchlist = outgrow_classic(branchlist, pars)
        verts, edges, faces, selection, info =  toverts(branchlist, pars)

        # creating the tree
        mesh = bpy.data.meshes.new("tree")
        tree = bpy.data.objects.new("tree", mesh)
        bpy.context.collection.objects.link(tree)
        mesh.from_pydata(verts, edges, faces)
        bpy.ops.object.select_all(action="DESELECT")
        tree.select_set(True)
        bpy.context.view_layer.objects.active = tree
        bpy.ops.object.shade_smooth()

        # renaming and parenting
        curve_obj.parent = tree
        tree.matrix_world.translation = context.scene.cursor.location
        ext = ""
        if len(tree.name.split(".")) > 1:
            ext = "." + tree.name.split(".")[1]
        curve_obj.name = "custom trunk" + ext
        for m in bpy.data.meshes:
            if m.users == 0 and m.name == str("trunk curve" + ext):
                bpy.data.meshes.remove(m)
        curve_obj.data.name = "trunk curve" + ext

        # writing properties
        pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1] = seeds

        # adding vertex group for furthest branches
        if selection:
            v_group = tree.vertex_groups.new(name="leaves")
            v_group.add(selection, 1.0, "ADD")

        # adding geometry nodes for leaves
        if "CalmTree_nodegroup" not in bpy.data.node_groups:
            CalmTree_nodegroup_exec()
        ng = bpy.data.node_groups["CalmTree_nodegroup"]
        if "CalmTree" not in bpy.context.object.modifiers:
            bpy.context.object.modifiers.new(name="CalmTree", type="NODES")
        geo_mod = bpy.context.object.modifiers["CalmTree"]
        if not geo_mod.node_group:
            geo_mod.node_group = ng
        bpy.ops.object.geometry_nodes_input_attribute_toggle(
            prop_path='["Input_1_use_attribute"]', modifier_name="CalmTree"
        )
        bpy.context.object.modifiers["CalmTree"]["Input_1_attribute_name"] = "leaves"
        tps.treename = context.object.name

        context.object["CalmTreeConfig"] = saveconfig()
        tps.ops_complete = True

        return {"FINISHED"}


class CALMTREE_OT_sync(bpy.types.Operator):
    """syncs tps property group with custom properties"""

    bl_idname = "object.tree_sync"
    bl_label = "sync tree object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            bpy.context.object["CalmTreeConfig"]
        except:
            self.report({"INFO"}, "I can't sync an object that isn't a tree")
            return {"FINISHED"}

        config = context.object["CalmTreeConfig"]

        tps = bpy.data.window_managers["WinMan"].calmtree_props
        config = [i.split("=") for i in config.split(",")]
        excluded = ["__", "rna", "sync"]
        tps.ops_complete = False
        for old in dir(tps):
            if not any(x in old for x in excluded):
                new = [i for i in config if old in i][0][1]
                try:
                    int(new)
                except:
                    pass
                else:
                    setattr(tps, old, int(new))
                    continue
                try:
                    float(new)
                except:
                    pass
                else:
                    setattr(tps, old, float(new))
                    continue
                if new == "True":
                    setattr(tps, old, True)
                elif new == "False":
                    setattr(tps, old, False)
                else:
                    setattr(tps, old, new)
        tps.ops_complete = True

        return {"FINISHED"}


class CALMTREE_OT_default(bpy.types.Operator):
    """returns all values to default"""

    bl_idname = "object.tree_default"
    bl_label = "return to defaults"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        tps = bpy.data.window_managers["WinMan"].calmtree_props
        tps.treename = context.object.name
        tps.ops_complete = False
        excluded = ["__", "rna", "sync"]
        for i in dir(tps):
            if not any(x in i for x in excluded):
                tps.property_unset(i)
        tps.ops_complete = True
        bpy.ops.object.tree_update()
        return {"FINISHED"}


class CALMTREE_OT_leaf(bpy.types.Operator):
    """handles leaves"""

    bl_idname = "object.tree_leaf"
    bl_label = "attach leaves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        tps = context.window_manager.calmtree_props
        script_file = os.path.realpath(__file__)
        directory = os.path.dirname(script_file)
        treeob = bpy.context.object
        colname = "CalmTreeLeaves"
        leafname = tps.leafchoice

        bpy.ops.object.select_all(action="DESELECT")
        if colname not in [i.name for i in bpy.data.collections]:
            col = bpy.data.collections.new(colname)
            bpy.context.scene.collection.children.link(col)
        else:
            col = bpy.data.collections[colname]

        if leafname not in [o.name for o in bpy.data.objects]:
            bpy.ops.import_scene.fbx(
                filepath=directory + "/assets/" + leafname + ".fbx"
            )
        ob = bpy.data.objects[leafname]
        if leafname not in [o.name for o in bpy.data.collections[colname].objects]:
            if ob.users_collection:
                ob.users_collection[0].objects.unlink(ob)
            col.objects.link(ob)

        if "CalmTree" not in [m.name for m in treeob.modifiers]:
            geonode()

        treeob.modifiers["CalmTree"]["Input_2"] = bpy.data.objects[leafname]
        bpy.ops.object.select_all(action="DESELECT")
        treeob.select_set(True)
        bpy.context.view_layer.objects.active = treeob

        return {"FINISHED"}


class CALMTREE_OT_mat(bpy.types.Operator):
    """handles stock materials"""

    bl_idname = "object.tree_mat"
    bl_label = "add stock materials if checked"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            context.object["CalmTreeConfig"]
        except:
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {"FINISHED"}
        treeob = bpy.context.object

        if "barknode" not in [n.name for n in bpy.data.node_groups]:
            barkgroup_node_group()

        if "CalmTreeBark" not in [m.name for m in bpy.data.materials]:
            barkmat = bpy.data.materials.new("CalmTreeBark")
            barkmat.use_nodes = True
            calmtree_bark_node_group(barkmat)
        else:
            barkmat = bpy.data.materials["CalmTreeBark"]

        if treeob.data.materials:
            treeob.data.materials[0] = barkmat
        else:
            treeob.data.materials.append(barkmat)

        if "CalmTree" not in treeob.modifiers:
            return {"FINISHED"}

        rgb = {
            "basic": (
                0.1369853913784027,
                0.1911628544330597,
                0.009205194190144539,
                1.0,
            ),
            "birch": (
                0.11697068810462952,
                0.2422812283039093,
                0.0024282161612063646,
                1.0,
            ),
            "elm": (0.12477181106805801, 0.27049776911735535, 0.16202937066555023, 1.0),
            "magnolia": (0.03954625129699707, 0.1499597728252411, 0.0, 1.0),
            "oak": (0.17144110798835754, 0.32314327359199524, 0.0, 1.0),
            "redalder": (
                0.10424429923295975,
                0.19119800627231598,
                0.055753905326128006,
                1.0,
            ),
            "sycamore": (
                0.09305897355079651,
                0.17464742064476013,
                0.005181516520678997,
                1.0,
            ),
            "tuliptree": (
                0.16826941072940826,
                0.3049874007701874,
                0.03433980047702789,
                1.0,
            ),
            "willow": (
                0.27049776911735535,
                0.45641112327575684,
                0.014443845488131046,
                1.0,
            ),
        }

        if "leafnode" not in [n.name for n in bpy.data.node_groups]:
            leafnode_node_group()

        leafob = treeob.modifiers["CalmTree"]["Input_2"]
        leafname = leafob.name

        if leafname not in [m.name for m in bpy.data.materials]:
            mat = bpy.data.materials.new(leafname)
            mat.use_nodes = True
            leaf_node_group(mat, rgb[leafname])
        else:
            mat = bpy.data.materials[leafname]

        if leafob.data.materials:
            leafob.data.materials[0] = mat
        else:
            leafob.data.materials.append(mat)

        bpy.ops.object.select_all(action="DESELECT")
        treeob.select_set(True)
        bpy.context.view_layer.objects.active = treeob

        return {"FINISHED"}