# ComfyUI Custom Node: List Custom Nodes

# ComfyUI custom nodes should define NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
# This is what ComfyUI looks for when loading custom nodes

# Import the required ComfyUI modules
import sys
import os

class CustomNodeLister:
    """
    A ComfyUI node that lists ComfyUI Manager compatible package names with install commands
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {}
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("package_list",)
    FUNCTION = "list_nodes"
    CATEGORY = "utilities"
    
    def list_nodes(self):
        try:
            # Import ComfyUI's node registry
            from nodes import NODE_CLASS_MAPPINGS
            import os
            import sys
            
            # Get all registered nodes
            all_nodes = NODE_CLASS_MAPPINGS
            
            # Try to extract ComfyUI Manager compatible package names
            custom_packages = set()
            pax`ckage_to_nodes = {}
            
            for node_name, node_class in all_nodes.items():
                try:
                    # Get the module where this node class is defined
                    module_name = node_class.__module__
                    
                    # Skip built-in nodes (from main 'nodes' module)
                    if module_name.startswith('nodes') or module_name == '__main__':
                        continue
                    
                    # Check if it's from custom_nodes directory
                    if 'custom_nodes' in module_name:
                        # Extract the package name from the module path
                        # e.g., "custom_nodes.ComfyUI-Manager.__init__" -> "ComfyUI-Manager"
                        parts = module_name.split('.')
                        if len(parts) >= 2 and parts[0] == 'custom_nodes':
                            package_name = parts[1]
                            custom_packages.add(package_name)
                            
                            # Track which nodes belong to which package
                            if package_name not in package_to_nodes:
                                package_to_nodes[package_name] = []
                            package_to_nodes[package_name].append(node_name)
                    
                    # Also try to get the actual module file path
                    elif hasattr(node_class, '__module__'):
                        try:
                            module = sys.modules.get(module_name)
                            if module and hasattr(module, '__file__') and module.__file__:
                                file_path = module.__file__
                                # Check if it's in a custom_nodes directory
                                if 'custom_nodes' in file_path:
                                    # Extract package name from file path
                                    path_parts = file_path.replace('\\', '/').split('/')
                                    custom_nodes_idx = -1
                                    for i, part in enumerate(path_parts):
                                        if part == 'custom_nodes':
                                            custom_nodes_idx = i
                                            break
                                    
                                    if custom_nodes_idx >= 0 and custom_nodes_idx + 1 < len(path_parts):
                                        package_name = path_parts[custom_nodes_idx + 1]
                                        custom_packages.add(package_name)
                                        
                                        if package_name not in package_to_nodes:
                                            package_to_nodes[package_name] = []
                                        package_to_nodes[package_name].append(node_name)
                        except:
                            pass
                            
                except Exception:
                    # Skip nodes we can't analyze
                    continue
            
            # Format the output for ComfyUI Manager compatibility
            if custom_packages:
                result_lines = [f"ComfyUI Manager Compatible Packages ({len(custom_packages)} found):"]
                result_lines.append("=" * 50)
                
                for package_name in sorted(custom_packages):
                    result_lines.append(f"\n📦 {package_name}")
                    result_lines.append(f"   Install: comfy-cli install {package_name}")
                    
                    # Show the nodes provided by this package
                    if package_name in package_to_nodes:
                        nodes_list = package_to_nodes[package_name]
                        if len(nodes_list) <= 3:
                            result_lines.append(f"   Provides: {', '.join(nodes_list)}")
                        else:
                            result_lines.append(f"   Provides: {', '.join(nodes_list[:3])} + {len(nodes_list)-3} more")
                
                node_list = "\n".join(result_lines)
            else:
                node_list = "No custom packages found that are ComfyUI Manager compatible."
            
            return (node_list,)
        except Exception as e:
            return (f"Error listing packages: {str(e)}",)

# Required mappings for ComfyUI to recognize this as a custom node
NODE_CLASS_MAPPINGS = {
    "CustomNodeLister": CustomNodeLister
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomNodeLister": "List ComfyUI Manager Packages"
}

# This will be called when the module is imported
print("ComfyUI Custom Node Lister loaded successfully!")
