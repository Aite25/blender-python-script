render_layers_node = node_tree.nodes.get("Render Layers")
node_tree.links.new(render_layers_node.outputs["Image"], file_output.inputs["Image"])
