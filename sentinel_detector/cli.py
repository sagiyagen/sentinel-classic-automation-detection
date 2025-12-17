#!/usr/bin/env python3
"""
Command-line interface for the Sentinel Classic Automation Detection Tool.
"""
import argparse
import sys
from .azure_client import SentinelClient
from .detector import ClassicAutomationDetector
from .formatter import OutputFormatter


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Detect Microsoft Sentinel analytic rules using classic automation that need migration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all workspaces in a subscription
  sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012

  # Scan specific workspace
  sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \\
                  --resource-group myRG --workspace-name mySentinelWorkspace

  # Save results to JSON file
  sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \\
                  --output-format json --output-file results.json

  # Save results to CSV file
  sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \\
                  --output-format csv --output-file results.csv

  # Use Azure CLI credentials
  sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \\
                  --use-cli-credential
"""
    )
    
    parser.add_argument(
        '--subscription-id',
        required=True,
        help='Azure subscription ID'
    )
    
    parser.add_argument(
        '--resource-group',
        help='Specific resource group to scan (optional)'
    )
    
    parser.add_argument(
        '--workspace-name',
        help='Specific Sentinel workspace to scan (optional, requires --resource-group)'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['console', 'json', 'csv'],
        default='console',
        help='Output format (default: console)'
    )
    
    parser.add_argument(
        '--output-file',
        help='Output file path (if not specified, prints to stdout)'
    )
    
    parser.add_argument(
        '--use-cli-credential',
        action='store_true',
        help='Use Azure CLI credentials instead of DefaultAzureCredential'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.workspace_name and not args.resource_group:
        parser.error("--workspace-name requires --resource-group")
    
    try:
        # Initialize client
        print("Initializing Azure connection...")
        client = SentinelClient(
            subscription_id=args.subscription_id,
            use_cli_credential=args.use_cli_credential
        )
        
        # Initialize detector
        detector = ClassicAutomationDetector(client)
        
        # Run detection
        if args.resource_group and args.workspace_name:
            # Scan specific workspace
            results = detector.detect_workspace(args.resource_group, args.workspace_name)
        else:
            # Scan all workspaces
            results = detector.detect_all_workspaces()
        
        # Format output
        formatter = OutputFormatter()
        
        if args.output_format == 'json':
            output = formatter.format_json(results)
        elif args.output_format == 'csv':
            output = formatter.format_csv(results)
        else:
            output = formatter.format_console(results)
        
        # Save or print output
        if args.output_file:
            formatter.save_to_file(output, args.output_file)
        else:
            print(output)
        
        # Exit with appropriate code
        if results:
            sys.exit(1)  # Rules found that need migration
        else:
            sys.exit(0)  # No rules found with classic automation
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
