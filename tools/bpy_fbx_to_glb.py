import sys
import bpy

if __name__ == "__main__":
    args = sys.argv[sys.argv.index('--'):]
    bpy.ops.import_scene.fbx(filepath=args[1])
    obj = bpy.context.active_object

    bpy.ops.export_scene.gltf(
        filepath=args[2],
        export_normals=False,
        export_colors=False,
        use_selection=True
    )