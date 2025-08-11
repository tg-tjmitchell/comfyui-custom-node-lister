#!/usr/bin/env python3
"""
Simple test script to verify the ComfyUI node structure
"""

def test_node_structure():
    """Test that the node is properly structured for ComfyUI"""
    try:
        # Import the module
        import __init__
        
        # Check that the required mappings exist
        assert hasattr(__init__, 'NODE_CLASS_MAPPINGS'), "NODE_CLASS_MAPPINGS not found"
        assert hasattr(__init__, 'NODE_DISPLAY_NAME_MAPPINGS'), "NODE_DISPLAY_NAME_MAPPINGS not found"
        
        # Check that the mappings are dictionaries
        assert isinstance(__init__.NODE_CLASS_MAPPINGS, dict), "NODE_CLASS_MAPPINGS is not a dict"
        assert isinstance(__init__.NODE_DISPLAY_NAME_MAPPINGS, dict), "NODE_DISPLAY_NAME_MAPPINGS is not a dict"
        
        # Check that our node is in the mappings
        assert "CustomNodeLister" in __init__.NODE_CLASS_MAPPINGS, "CustomNodeLister not in NODE_CLASS_MAPPINGS"
        assert "CustomNodeLister" in __init__.NODE_DISPLAY_NAME_MAPPINGS, "CustomNodeLister not in NODE_DISPLAY_NAME_MAPPINGS"
        
        # Check that the class exists and has required methods
        node_class = __init__.NODE_CLASS_MAPPINGS["CustomNodeLister"]
        assert hasattr(node_class, 'INPUT_TYPES'), "Node missing INPUT_TYPES"
        assert hasattr(node_class, 'RETURN_TYPES'), "Node missing RETURN_TYPES"
        assert hasattr(node_class, 'FUNCTION'), "Node missing FUNCTION"
        assert hasattr(node_class, 'CATEGORY'), "Node missing CATEGORY"
        
        # Test that INPUT_TYPES is callable
        input_types = node_class.INPUT_TYPES()
        assert isinstance(input_types, dict), "INPUT_TYPES() should return a dict"
        assert "required" in input_types, "INPUT_TYPES should have 'required' key"
        
        # Test node instantiation and function call
        node_instance = node_class()
        assert hasattr(node_instance, node_class.FUNCTION), f"Node missing function {node_class.FUNCTION}"
        
        print("✅ All tests passed! Node structure is correct for ComfyUI.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_node_structure()
