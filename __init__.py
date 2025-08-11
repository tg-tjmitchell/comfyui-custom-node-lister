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

    Notes:
    Results are filtered to packages recognized by ComfyUI-Manager. We determine
    the Manager's catalog by first attempting to run its local CLI (cm-cli.py)
    in local mode. If that's not available, we try reading its embedded
    custom-node-list.json from the ComfyUI-Manager folder.
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
            import subprocess
            import json

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

            # Helper: Find ComfyUI root and Manager paths
            def get_comfy_root_and_manager(custom_nodes_dir: str):
                if not custom_nodes_dir:
                    return None, None
                comfy_root = os.path.dirname(custom_nodes_dir)
                mgr_dir = os.path.join(custom_nodes_dir, 'ComfyUI-Manager')
                if not os.path.isdir(mgr_dir):
                    # Try to find a folder containing cm-cli.py under custom_nodes
                    try:
                        for name in os.listdir(custom_nodes_dir):
                            p = os.path.join(custom_nodes_dir, name)
                            if os.path.isdir(p) and os.path.isfile(os.path.join(p, 'cm-cli.py')):
                                mgr_dir = p
                                break
                    except Exception:
                        pass
                return comfy_root, (mgr_dir if os.path.isdir(mgr_dir) else None)

            comfy_root, manager_dir = get_comfy_root_and_manager(custom_nodes_dir)

            # Helper: Obtain Manager-recognized package names
            def get_manager_names() -> set:
                names: set = set()
                # A) Try cm-cli.py simple-show all --mode local
                try:
                    if manager_dir and comfy_root:
                        cm_cli = os.path.join(manager_dir, 'cm-cli.py')
                        if os.path.isfile(cm_cli):
                            env = os.environ.copy()
                            # Help cm-cli find ComfyUI path explicitly
                            env.setdefault('COMFYUI_PATH', comfy_root)
                            out = subprocess.check_output([
                                sys.executable, cm_cli, 'simple-show', 'all', '--mode', 'local'
                            ], cwd=comfy_root, env=env, stderr=subprocess.STDOUT, text=True, timeout=15)
                            for raw_line in out.splitlines():
                                line = raw_line.strip()
                                if not line:
                                    continue
                                if line.startswith('-=') or line.startswith('FETCH DATA') or line.startswith('python '):
                                    continue
                                # Heuristic: ignore bracketed status lines from 'show'
                                if line.startswith('[') and ']' in line:
                                    continue
                                names.add(line)
                except Exception:
                    pass

                # B) Fallback: read embedded custom-node-list.json
                if not names and manager_dir:
                    try:
                        # Search for the file by name within manager_dir
                        candidate = None
                        for root, _dirs, files in os.walk(manager_dir):
                            for f in files:
                                if f == 'custom-node-list.json':
                                    candidate = os.path.join(root, f)
                                    break
                            if candidate:
                                break
                        if candidate and os.path.isfile(candidate):
                            with open(candidate, 'r', encoding='utf-8') as fh:
                                data = json.load(fh)
                            # Try common structures: list of objects or dict of entries
                            if isinstance(data, list):
                                for item in data:
                                    # try keys commonly used: name, repo, repository
                                    if isinstance(item, dict):
                                        for key in ('name', 'repo', 'repository'):
                                            v = item.get(key)
                                            if isinstance(v, str) and v:
                                                names.add(v.strip())
                                                break
                            elif isinstance(data, dict):
                                # Flatten any string values; else, look for name fields in nested dicts
                                for k, v in data.items():
                                    if isinstance(v, str):
                                        names.add(v.strip())
                                    elif isinstance(v, dict):
                                        nm = v.get('name') if 'name' in v else None
                                        if isinstance(nm, str) and nm:
                                            names.add(nm.strip())
                    except Exception:
                        pass

                return names

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

            # Deduplicate
            packages_set = {p for p in discovered_packages}

            # Filter to ComfyUI-Manager recognized names when possible
            manager_names = get_manager_names()
            if manager_names:
                packages_set = {p for p in packages_set if p in manager_names}

            # Sort after filtering
            packages = sorted(packages_set)

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
