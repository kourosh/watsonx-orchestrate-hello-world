#!/usr/bin/env python3
"""
Convert Python agent configuration to YAML format for watsonx Orchestrate deployment.
"""

import yaml
import sys
from pathlib import Path

# Add the parent directory to the path to import the agent module
sys.path.insert(0, str(Path(__file__).parent))

from lendyr_bank_orchestrator import get_agent_config, validate_agent_config


def convert_to_yaml(output_file: str = "lendyr-bank-orchestrator.yaml") -> None:
    """
    Convert the Python agent configuration to YAML format.
    
    Args:
        output_file: The name of the output YAML file
    """
    # Validate configuration first
    if not validate_agent_config():
        print("✗ Agent configuration is invalid. Cannot convert to YAML.")
        sys.exit(1)
    
    # Get the configuration
    config = get_agent_config()
    
    # Write to YAML file
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✓ Successfully converted agent configuration to YAML")
    print(f"✓ Output file: {output_path}")
    print(f"✓ Agent Name: {config['name']}")
    print(f"✓ Display Name: {config['display_name']}")


if __name__ == "__main__":
    # Check if custom output filename is provided
    output_file = sys.argv[1] if len(sys.argv) > 1 else "lendyr-bank-orchestrator.yaml"
    convert_to_yaml(output_file)

# Made with Bob
