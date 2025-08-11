ComfyUI Manager Package Lister
================================

A ComfyUI custom node that lists installed custom node packages in ComfyUI Manager compatible format, providing the exact package names and install commands for sharing or reinstalling.

## Installation

1. Clone or download this repository to your ComfyUI `custom_nodes` directory:
   ```
   cd ComfyUI/custom_nodes/
   git clone <your-repo-url> comfyui-custom-node-lister
   ```

2. Restart ComfyUI

## Usage

After installation, you'll find a new node called "List ComfyUI Manager Packages" in the utilities category. This node will output:

- Package names compatible with ComfyUI Manager
- Ready-to-use `comfy-cli install` commands
- Which nodes each package provides
- Total count of installed custom packages

## Example Output

```
ComfyUI Manager Compatible Packages (3 found):
==================================================

📦 ComfyUI-AnimateDiff-Evolved
   Install: comfy-cli install ComfyUI-AnimateDiff-Evolved
   Provides: AnimateDiffLoader, AnimateDiffSampler, AnimateDiffCombine

📦 ComfyUI-Manager
   Install: comfy-cli install ComfyUI-Manager
   Provides: ManagerUpdate, ManagerInstall + 5 more

📦 comfyui-custom-node-lister
   Install: comfy-cli install comfyui-custom-node-lister
   Provides: CustomNodeLister
```

## Features

- **ComfyUI Manager Compatible**: Shows actual package names that work with `comfy-cli install`
- **Ready-to-use Commands**: Copy-paste install commands for easy sharing
- **Package Mapping**: Shows which nodes each package provides
- **Clean Output**: Groups nodes by their source packages
- **Installation Ready**: Perfect for recreating setups on new ComfyUI installations

## Use Cases

- **Backup/Restore**: Get a list of all your custom packages for easy reinstallation
- **Sharing Setups**: Share your custom node configuration with others
- **Documentation**: Keep track of what custom nodes you have installed
- **Migration**: Move your custom node setup to a new ComfyUI installation

## How it works

The node analyzes the module paths of installed custom nodes to:

1. **Extract Package Names**: Identifies the original package/repository name from the module structure
2. **Filter Built-ins**: Excludes ComfyUI's built-in nodes
3. **Group by Package**: Organizes nodes by their source package
4. **Generate Commands**: Provides ready-to-use `comfy-cli install` commands

## Troubleshooting

If you get import errors, make sure:
1. This folder is placed in the `custom_nodes` directory of your ComfyUI installation
2. ComfyUI has been restarted after installation
3. The folder is named correctly (avoid spaces and special characters)

If some packages don't appear, they may not follow standard ComfyUI Manager naming conventions.
