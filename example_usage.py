#!/usr/bin/env python3
"""
Example usage script demonstrating how to use the Sentinel detector programmatically.
This shows how to integrate the detection tool into your own Python scripts.
"""

from sentinel_detector.azure_client import SentinelClient
from sentinel_detector.detector import ClassicAutomationDetector
from sentinel_detector.formatter import OutputFormatter
import sys


def main():
    """Example of using the detector programmatically."""
    
    # Configuration
    subscription_id = "12345678-1234-1234-1234-123456789012"  # Replace with your subscription ID
    resource_group = None  # Optional: specify to scan only one resource group
    workspace_name = None  # Optional: specify to scan only one workspace (requires resource_group)
    
    print("=" * 80)
    print("PROGRAMMATIC USAGE EXAMPLE")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Create Azure client
        print("1. Initializing Azure client...")
        client = SentinelClient(
            subscription_id=subscription_id,
            use_cli_credential=True  # Use Azure CLI credentials
        )
        print("   ✓ Client initialized\n")
        
        # Step 2: Create detector
        print("2. Creating detector...")
        detector = ClassicAutomationDetector(client)
        print("   ✓ Detector created\n")
        
        # Step 3: Run detection
        print("3. Running detection...")
        if resource_group and workspace_name:
            # Scan specific workspace
            results = detector.detect_workspace(resource_group, workspace_name)
        else:
            # Scan all workspaces
            results = detector.detect_all_workspaces()
        print(f"   ✓ Detection complete\n")
        
        # Step 4: Process results
        print("4. Processing results...")
        formatter = OutputFormatter()
        
        # You can format in different ways:
        
        # Console output
        console_output = formatter.format_console(results)
        print(console_output)
        
        # Or save to JSON
        json_output = formatter.format_json(results)
        formatter.save_to_file(json_output, "results.json")
        
        # Or save to CSV
        csv_output = formatter.format_csv(results)
        formatter.save_to_file(csv_output, "results.csv")
        
        print("\n" + "=" * 80)
        print("PROGRAMMATIC EXAMPLE COMPLETE")
        print("=" * 80)
        print()
        
        # Custom processing example
        if results:
            print("Custom Processing Example:")
            print(f"Total rules requiring migration: {len(results)}")
            
            # Group by severity
            by_severity = {}
            for result in results:
                severity = result['severity']
                by_severity[severity] = by_severity.get(severity, 0) + 1
            
            print("\nBreakdown by severity:")
            for severity, count in sorted(by_severity.items()):
                print(f"  {severity}: {count} rule(s)")
            
            # List all unique playbooks
            playbooks = set()
            for result in results:
                for action in result['actions']:
                    playbooks.add(action['logic_app_resource_id'])
            
            print(f"\nUnique playbooks requiring migration: {len(playbooks)}")
            for playbook in sorted(playbooks):
                print(f"  - {playbook}")
        
        # Return appropriate exit code
        return 1 if results else 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 2


if __name__ == '__main__':
    sys.exit(main())
