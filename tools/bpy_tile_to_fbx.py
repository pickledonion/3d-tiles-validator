import sys
import bpy


if __name__ == "__main__":
    args = sys.argv[sys.argv.index('--'):]
    bpy.ops.import_scene.gltf(filepath=args[1])
    obj = bpy.context.active_object

    bpy.ops.export_scene.fbx(
        filepath=args[2],
        path_mode='COPY',
        embed_textures=True,
        object_types=set({'MESH'}),
        use_selection=True
    )


