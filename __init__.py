# ComfyUI Custom Node: List Custom Nodes

# ComfyUI custom nodes should define NONODE_DISPLAY_NAME_MAPPINGS = {
    "CustomNodeLister": "List ComfyUI Manager Packages"
}CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
# This is what ComfyUI looks for when loading custom nodes

# Import the required ComfyUI modules
import sys
import os

class CustomNodeLister:
    """
    A ComfyUI node that lists ComfyUI Manager compatible package names for installed custom nodes
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
            import nodes
            
            # Get all registered nodes
            all_nodes = set(NODE_CLASS_MAPPINGS.keys())
            
            # Try to extract ComfyUI Manager compatible names (folder/repo names)
            custom_node_packages = set()
            
            # Method: Extract the custom_nodes folder name from module paths
            for node_name, node_class in NODE_CLASS_MAPPINGS.items():
                try:
                    # Get the module where this node class is defined
                    module = node_class.__module__
                    
                    # If the module contains 'custom_nodes' in its path, it's a custom node
                    if 'custom_nodes' in module:
                        # Extract the package name from the module path
                        # Example: custom_nodes.ComfyUI-Manager.__init__ -> ComfyUI-Manager
                        # Example: custom_nodes.was_node_suite.was_node_suite -> was_node_suite
                        parts = module.split('.')
                        if len(parts) >= 2 and parts[0] == 'custom_nodes':
                            package_name = parts[1]  # The folder name in custom_nodes
                            custom_node_packages.add(package_name)
                    # Also check if it's not from the main 'nodes' module
                    elif not module.startswith('nodes') and module != '__main__':
                        # For modules not in custom_nodes but still custom
                        # Extract the top-level module name
                        package_name = module.split('.')[0]
                        if package_name not in ['nodes', 'comfy', '__main__']:
                            custom_node_packages.add(package_name)
                except:
                    # If we can't determine, skip it
                    continue
            
            # If no custom nodes found using the above method, fall back to a message
            if not custom_node_packages:
                return ("No ComfyUI Manager compatible custom node packages found.",)
            
            # Format the output with ComfyUI Manager compatible names
            package_list = sorted(custom_node_packages)
            node_list = f"ComfyUI Manager Compatible Packages ({len(package_list)} found):\n"
            node_list += "\n".join(package_list)
            node_list += f"\n\nTo install any of these with comfy-cli:\ncomfy-cli install <package_name>"
            
            return (node_list,)
        except Exception as e:
            return (f"Error listing nodes: {str(e)}",)

# Required mappings for ComfyUI to recognize this as a custom node
NODE_CLASS_MAPPINGS = {
    "CustomNodeLister": CustomNodeLister
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomNodeLister": "List Custom Nodes Only"
}

# This will be called when the module is imported
print("ComfyUI Custom Node Lister loaded successfully!")
