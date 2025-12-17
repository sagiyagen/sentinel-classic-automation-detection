"""
Output formatters for detection results.
"""
import json
import csv
from typing import List, Dict, Any
from datetime import datetime


class OutputFormatter:
    """Formats detection results for various output formats."""
    
    @staticmethod
    def format_console(results: List[Dict[str, Any]]) -> str:
        """
        Format results for console output.
        
        Args:
            results: List of detection results
            
        Returns:
            Formatted string for console display
        """
        if not results:
            return "\n✅ No analytic rules with classic automation found.\n"
        
        output = ["\n" + "="*80]
        output.append("MICROSOFT SENTINEL CLASSIC AUTOMATION DETECTION REPORT")
        output.append("="*80)
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Total Rules with Classic Automation: {len(results)}")
        output.append("="*80 + "\n")
        
        # Group by workspace
        workspaces = {}
        for result in results:
            ws_key = f"{result['workspace_name']} ({result['resource_group']})"
            if ws_key not in workspaces:
                workspaces[ws_key] = []
            workspaces[ws_key].append(result)
        
        for ws_key, ws_results in workspaces.items():
            output.append(f"\n📊 Workspace: {ws_key}")
            output.append(f"   Rules requiring migration: {len(ws_results)}")
            output.append("-" * 80)
            
            for idx, result in enumerate(ws_results, 1):
                output.append(f"\n  [{idx}] {result['rule_display_name']}")
                output.append(f"      Rule ID: {result['rule_id']}")
                output.append(f"      Type: {result['rule_type']}")
                output.append(f"      Severity: {result['severity']}")
                output.append(f"      Enabled: {result['enabled']}")
                output.append(f"      Classic Automations: {result['classic_automation_count']}")
                
                if result['actions']:
                    output.append("      Playbooks:")
                    for action in result['actions']:
                        output.append(f"        - {action['logic_app_resource_id']}")
                
                output.append(f"      ⚠️  Migration Required by: {result['migration_deadline']}")
        
        output.append("\n" + "="*80)
        output.append("MIGRATION RECOMMENDATIONS")
        output.append("="*80)
        output.append("1. Review the official migration guide:")
        output.append("   https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules")
        output.append("2. Create automation rules to replace classic automation")
        output.append("3. Test the new automation rules thoroughly")
        output.append("4. Remove classic automation from analytic rules")
        output.append("5. Complete migration before March 31, 2026")
        output.append("="*80 + "\n")
        
        return "\n".join(output)
    
    @staticmethod
    def format_json(results: List[Dict[str, Any]], pretty: bool = True) -> str:
        """
        Format results as JSON.
        
        Args:
            results: List of detection results
            pretty: If True, format with indentation
            
        Returns:
            JSON string
        """
        output = {
            'generated_at': datetime.now().isoformat(),
            'total_rules_with_classic_automation': len(results),
            'migration_deadline': '2026-03-31',
            'results': results
        }
        
        if pretty:
            return json.dumps(output, indent=2)
        return json.dumps(output)
    
    @staticmethod
    def format_csv(results: List[Dict[str, Any]]) -> str:
        """
        Format results as CSV.
        
        Args:
            results: List of detection results
            
        Returns:
            CSV string
        """
        if not results:
            return "No results found"
        
        # Prepare CSV data
        import io
        output = io.StringIO()
        
        fieldnames = [
            'workspace_name',
            'resource_group',
            'rule_id',
            'rule_display_name',
            'rule_type',
            'enabled',
            'severity',
            'classic_automation_count',
            'playbook_resource_ids',
            'migration_required',
            'migration_deadline'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            # Flatten the actions into a comma-separated list
            playbook_ids = ', '.join([
                action['logic_app_resource_id'] 
                for action in result.get('actions', [])
            ])
            
            row = {
                'workspace_name': result['workspace_name'],
                'resource_group': result['resource_group'],
                'rule_id': result['rule_id'],
                'rule_display_name': result['rule_display_name'],
                'rule_type': result['rule_type'],
                'enabled': result['enabled'],
                'severity': result['severity'],
                'classic_automation_count': result['classic_automation_count'],
                'playbook_resource_ids': playbook_ids,
                'migration_required': result['migration_required'],
                'migration_deadline': result['migration_deadline']
            }
            
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def save_to_file(content: str, filename: str) -> None:
        """
        Save content to a file.
        
        Args:
            content: Content to save
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Results saved to: {filename}")
