# ComfyUI Custom Node: List Custom Nodes

# ComfyUI custom nodes should define NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
# This is what ComfyUI looks for when loading custom nodes

# Import the required ComfyUI modules
import sys
import os

# Global variables to export - ComfyUI looks for these
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class CustomNodeLister:
    """
    A ComfyUI node that lists ComfyUI Manager compatible package names with:
    - Output 1: Full list including install commands and brief node summaries
    - Output 2: Names-only CSV (package names only, no commands or icons)
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {}
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("package_list", "package_names")
    FUNCTION = "list_nodes"
    CATEGORY = "utilities"
    
    def list_nodes(self):
        try:
            import os
            import sys

            # 1) Find the custom_nodes directory robustly based on this file's location
            def find_custom_nodes_dir(start_path: str):
                cur = os.path.abspath(start_path)
                # Walk up a few levels to find a folder literally named 'custom_nodes'
                for _ in range(6):
                    base = os.path.basename(cur)
                    if base == 'custom_nodes':
                        return cur
                    parent = os.path.dirname(cur)
                    if parent == cur:
                        break
                    cur = parent
                # Try sibling search one level up from this file
                root = os.path.dirname(os.path.abspath(start_path))
                for entry in os.listdir(root):
                    p = os.path.join(root, entry)
                    if os.path.isdir(p) and os.path.basename(p) == 'custom_nodes':
                        return p
                return None

            this_file = os.path.abspath(__file__)
            custom_nodes_dir = find_custom_nodes_dir(this_file)

            # 2) Enumerate all package folders under custom_nodes (folder names are the package names)
            discovered_packages = []
            if custom_nodes_dir and os.path.isdir(custom_nodes_dir):
                try:
                    for name in os.listdir(custom_nodes_dir):
                        full = os.path.join(custom_nodes_dir, name)
                        if not os.path.isdir(full):
                            continue
                        if name.startswith('.') or name in {'__pycache__'}:
                            continue
                        discovered_packages.append(name)
                except Exception:
                    pass

            # 3) Optionally, enrich with node names using ComfyUI's registry if available
            package_to_nodes = {}
            try:
                from nodes import NODE_CLASS_MAPPINGS as ALL_NODE_MAPPINGS  # type: ignore
                for node_name, node_class in ALL_NODE_MAPPINGS.items():
                    try:
                        module_name = getattr(node_class, '__module__', '') or ''
                        module = sys.modules.get(module_name)
                        file_path = getattr(module, '__file__', None) if module else None

                        # Prefer extracting package from file path inside custom_nodes
                        pkg_name = None
                        src_hint = file_path or module_name
                        if src_hint:
                            hint = str(src_hint).replace('\\', '/').split('/')
                            for i, part in enumerate(hint):
                                if part == 'custom_nodes' and i + 1 < len(hint):
                                    pkg_name = hint[i + 1]
                                    break

                        if pkg_name:
                            package_to_nodes.setdefault(pkg_name, []).append(node_name)
                            if pkg_name not in discovered_packages:
                                discovered_packages.append(pkg_name)
                    except Exception:
                        continue
            except Exception:
                # Registry not available; proceed with directory discovery only
                pass

            # Deduplicate and sort
            packages = sorted({p for p in discovered_packages})

            # 4) Format output
            if packages:
                result_lines = [f"ComfyUI Manager Compatible Packages ({len(packages)} found):", "=" * 50]
                for package_name in packages:
                    # Full details lines
                    result_lines.append(f"\n📦 {package_name}")
                    result_lines.append(f"   Install: comfy-cli install {package_name}")
                    nodes_list = package_to_nodes.get(package_name)
                    if nodes_list:
                        if len(nodes_list) <= 3:
                            result_lines.append(f"   Provides: {', '.join(nodes_list)}")
                        else:
                            result_lines.append(f"   Provides: {', '.join(nodes_list[:3])} + {len(nodes_list)-3} more")

                node_list = "\n".join(result_lines)
                # CSV of package names (no icon, no extra spaces)
                names_only = ",".join(packages)
            else:
                node_list = "No custom packages found in custom_nodes directory."
                names_only = ""

            return (node_list, names_only)
        except Exception as e:
            err = f"Error listing packages: {str(e)}"
            return (err, err)

# Required mappings for ComfyUI to recognize this as a custom node
NODE_CLASS_MAPPINGS["CustomNodeLister"] = CustomNodeLister

NODE_DISPLAY_NAME_MAPPINGS["CustomNodeLister"] = "List ComfyUI Manager Packages"

# This will be called when the module is imported
print("ComfyUI Custom Node Lister loaded successfully!")
