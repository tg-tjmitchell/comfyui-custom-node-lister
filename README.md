ComfyUI Custom Node Lister
============================

A simple ComfyUI custom node that provides a utility to list all available nodes in the ComfyUI interface.

## Installation

1. Clone or download this repository to your ComfyUI `custom_nodes` directory:
   ```
   cd ComfyUI/custom_nodes/
   git clone <your-repo-url> comfyui-custom-node-lister
   ```

2. Restart ComfyUI

## Usage

After installation, you'll find a new node called "List Custom Nodes" in the utilities category. This node will output a string containing all available nodes in your ComfyUI installation.

## Features

- Lists all registered nodes in ComfyUI
- Simple utility node for debugging and exploration
- No dependencies required

## Troubleshooting

If you get import errors, make sure:
1. This folder is placed in the `custom_nodes` directory of your ComfyUI installation
2. ComfyUI has been restarted after installation
3. The folder is named correctly (avoid spaces and special characters)
