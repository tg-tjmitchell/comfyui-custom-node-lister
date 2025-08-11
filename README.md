ComfyUI Custom Node Lister
============================

A ComfyUI custom node that provides a utility to list only custom nodes (excluding built-in ComfyUI nodes).

## Installation

1. Clone or download this repository to your ComfyUI `custom_nodes` directory:
   ```
   cd ComfyUI/custom_nodes/
   git clone <your-repo-url> comfyui-custom-node-lister
   ```

2. Restart ComfyUI

## Usage

After installation, you'll find a new node called "List Custom Nodes Only" in the utilities category. This node will output a string containing only the custom nodes in your ComfyUI installation, filtering out built-in nodes.

## Features

- Lists only custom nodes (excludes built-in ComfyUI nodes)
- Uses module path detection to identify custom nodes
- Fallback filtering for edge cases
- Shows count of custom nodes found
- Simple utility node for debugging and exploration
- No dependencies required

## How it works

The node uses two methods to identify custom nodes:

1. **Primary method**: Checks if the node's module path contains 'custom_nodes'
2. **Fallback method**: Excludes nodes with common built-in prefixes like 'Load', 'Save', 'Preview', etc.

## Troubleshooting

If you get import errors, make sure:
1. This folder is placed in the `custom_nodes` directory of your ComfyUI installation
2. ComfyUI has been restarted after installation
3. The folder is named correctly (avoid spaces and special characters)
