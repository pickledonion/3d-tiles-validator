import sys
import bpy


if __name__ == "__main__":
    args = sys.argv[sys.argv.index('--'):]
    print(args)
    bpy.ops.import_scene.gltf(filepath=args[1])
    obj = bpy.context.active_object
    mod = obj.modifiers.new("CorrectiveSmooth", 'CORRECTIVE_SMOOTH') 
    mod.factor = 0.1
    mod.scale = 1.5
    bpy.ops.object.modifier_apply(modifier="CorrectiveSmooth")
    bpy.ops.export_scene.gltf(
        filepath=args[2],
        export_normals=False,
        export_colors=False,
        use_selection=True
    )


