import sys
import bpy


if __name__ == "__main__":
    args = sys.argv[sys.argv.index('--'):]

    bpy.context.scene.render.engine = 'CYCLES'

    bpy.ops.import_scene.gltf(filepath=args[1])
    obj = bpy.context.active_object

    print("Duplicating object")
    bpy.ops.object.duplicate()
    new_obj = bpy.context.active_object

    print("UV Unwrapping")
    bpy.ops.object.editmode_toggle() 
    bpy.ops.mesh.select_all(action='SELECT') 
    bpy.ops.uv.smart_project() 
    bpy.ops.object.editmode_toggle()

    print("Clearing material slots")
    for i in range(len(new_obj.material_slots)):
        bpy.ops.object.material_slot_remove({'object': new_obj})

    print("Creating new material and image")
    mat = bpy.data.materials.new(name="Baked")
    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes
    img = bpy.data.images.new('bakedImage',2048,2048)
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf = nodes.get("Principled BSDF")
    node_tree.links.new(tex.outputs['Color'], bsdf.inputs[0])
    new_obj.data.materials.append(mat)

    print("Baking")
    bpy.ops.object.select_all(action = 'DESELECT')
    obj.select_set(True)
    new_obj.select_set(True)
    bpy.context.view_layer.objects.active = new_obj
    bpy.ops.object.bake(
            type='DIFFUSE',
            use_selected_to_active=True,
            pass_filter=set({'COLOR'})
    )

    obj.select_set(False)
    bpy.ops.export_scene.gltf(
        filepath=args[2],
        export_normals=False,
        export_colors=False,
        use_selection=True
    )


