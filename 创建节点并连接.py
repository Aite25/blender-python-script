import bpy

node_tree = bpy.context.scene.node_tree
file_output = node_tree.nodes.new("CompositorNodeOutputFile")
render_layers = node_tree.nodes.get("Render Layers")
node_tree.links.new(render_layers.outputs["Image"], file_output.inputs["Image"])
