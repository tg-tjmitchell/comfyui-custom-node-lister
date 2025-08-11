# ComfyUI Plugin: List Custom Nodes

import comfy
import comfy.registry

def list_custom_nodes():
    nodes = set(comfy.registry.NODE_REGISTRY.keys())
    # Exclude built-in nodes
    builtin_nodes = set(getattr(comfy.registry, "BUILTIN_NODES", []))
    custom_nodes = nodes - builtin_nodes
    return sorted(custom_nodes)

# Example usage: print all custom node registry names
if __name__ == "__main__":
    print("Installed ComfyUI custom nodes:")
    for node_name in list_custom_nodes():
        print(node_name)
