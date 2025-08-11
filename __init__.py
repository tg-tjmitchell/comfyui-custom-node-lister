# ComfyUI Custom Node: List Custom Nodes

# ComfyUI custom nodes should define NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
# This is what ComfyUI looks for when loading custom nodes

# Import the required ComfyUI modules
import sys
import os

class CustomNodeLister:
    """
    A ComfyUI node that lists all available custom nodes
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {}
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("node_list",)
    FUNCTION = "list_nodes"
    CATEGORY = "utilities"
    
    def list_nodes(self):
        try:
            # Import ComfyUI's node registry
            from nodes import NODE_CLASS_MAPPINGS
            
            # Get all registered nodes
            all_nodes = list(NODE_CLASS_MAPPINGS.keys())
            
            # Format the output
            node_list = "\n".join(sorted(all_nodes))
            return (node_list,)
        except Exception as e:
            return (f"Error listing nodes: {str(e)}",)

# Required mappings for ComfyUI to recognize this as a custom node
NODE_CLASS_MAPPINGS = {
    "CustomNodeLister": CustomNodeLister
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomNodeLister": "List Custom Nodes"
}

# This will be called when the module is imported
print("ComfyUI Custom Node Lister loaded successfully!")
