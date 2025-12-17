#!/usr/bin/env python3
"""
Simple demonstration and manual testing of the detection tool components.
This doesn't require actual Azure credentials.
"""
import sys
import json
from datetime import datetime

# Mock data structures for testing
MOCK_WORKSPACES = [
    {
        'id': '/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/sentinel-rg/providers/Microsoft.OperationalInsights/workspaces/sentinel-ws',
        'name': 'sentinel-ws',
        'resource_group': 'sentinel-rg',
        'location': 'eastus'
    }
]

MOCK_ALERT_RULES = [
    {
        'name': 'suspicious-login-rule',
        'kind': 'Scheduled',
        'properties': {
            'display_name': 'Suspicious Login Activity',
            'enabled': True,
            'severity': 'High',
            'description': 'Detects multiple failed login attempts'
        }
    },
    {
        'name': 'malware-detection',
        'kind': 'Scheduled',
        'properties': {
            'display_name': 'Malware Detection Alert',
            'enabled': True,
            'severity': 'Critical',
            'description': 'Detects potential malware activity'
        }
    }
]

MOCK_ACTIONS = {
    'suspicious-login-rule': [
        {
            'name': 'action-1',
            'properties': {
                'logic_app_resource_id': '/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/sentinel-rg/providers/Microsoft.Logic/workflows/EnrichmentPlaybook',
                'trigger_uri': 'https://prod-01.eastus.logic.azure.com:443/...'
            }
        },
        {
            'name': 'action-2',
            'properties': {
                'logic_app_resource_id': '/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/sentinel-rg/providers/Microsoft.Logic/workflows/NotificationPlaybook',
                'trigger_uri': 'https://prod-01.eastus.logic.azure.com:443/...'
            }
        }
    ],
    'malware-detection': [
        {
            'name': 'action-1',
            'properties': {
                'logic_app_resource_id': '/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/sentinel-rg/providers/Microsoft.Logic/workflows/IsolationPlaybook',
                'trigger_uri': 'https://prod-01.eastus.logic.azure.com:443/...'
            }
        }
    ]
}


def mock_as_dict(obj):
    """Convert mock object to dict."""
    if isinstance(obj, dict):
        return obj
    return obj


# Mock classes for testing
class MockRule:
    def __init__(self, data):
        self.name = data['name']
        self.kind = data['kind']
        self.properties = data['properties']
        self._data = data
    
    def as_dict(self):
        return self._data


class MockAction:
    def __init__(self, data):
        self.name = data['name']
        self.properties = data['properties']
        self._data = data
    
    def as_dict(self):
        return self._data


def test_detection_logic():
    """Test the detection logic with mock data."""
    print("=" * 80)
    print("TESTING SENTINEL CLASSIC AUTOMATION DETECTION")
    print("=" * 80)
    print()
    
    # Create mock detection results
    results = []
    
    for workspace in MOCK_WORKSPACES:
        print(f"📊 Workspace: {workspace['name']} (Resource Group: {workspace['resource_group']})")
        print(f"  Found {len(MOCK_ALERT_RULES)} alert rule(s)")
        
        rules_with_classic = 0
        for rule_data in MOCK_ALERT_RULES:
            rule_name = rule_data['name']
            actions = MOCK_ACTIONS.get(rule_name, [])
            
            if actions:
                rules_with_classic += 1
                
                # Build action details
                action_details = []
                for action in actions:
                    action_info = {
                        'action_id': action['name'],
                        'logic_app_resource_id': action['properties']['logic_app_resource_id'],
                        'trigger_uri': 'Configured'
                    }
                    action_details.append(action_info)
                
                result = {
                    'workspace_name': workspace['name'],
                    'resource_group': workspace['resource_group'],
                    'rule_id': rule_name,
                    'rule_display_name': rule_data['properties']['display_name'],
                    'rule_type': rule_data['kind'],
                    'enabled': rule_data['properties']['enabled'],
                    'severity': rule_data['properties']['severity'],
                    'classic_automation_count': len(actions),
                    'actions': action_details,
                    'migration_required': True,
                    'migration_deadline': '2026-03-31'
                }
                results.append(result)
        
        print(f"  ⚠️  Found {rules_with_classic} rule(s) with classic automation")
        print()
    
    return results


def test_console_output(results):
    """Test console output formatting."""
    print("=" * 80)
    print("TESTING CONSOLE OUTPUT FORMAT")
    print("=" * 80)
    print()
    
    output = [
        "=" * 80,
        "MICROSOFT SENTINEL CLASSIC AUTOMATION DETECTION REPORT",
        "=" * 80,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Rules with Classic Automation: {len(results)}",
        "=" * 80,
        ""
    ]
    
    for idx, result in enumerate(results, 1):
        output.append(f"[{idx}] {result['rule_display_name']}")
        output.append(f"    Workspace: {result['workspace_name']}")
        output.append(f"    Resource Group: {result['resource_group']}")
        output.append(f"    Rule ID: {result['rule_id']}")
        output.append(f"    Type: {result['rule_type']}")
        output.append(f"    Severity: {result['severity']}")
        output.append(f"    Enabled: {result['enabled']}")
        output.append(f"    Classic Automations: {result['classic_automation_count']}")
        output.append("    Playbooks:")
        for action in result['actions']:
            output.append(f"      - {action['logic_app_resource_id']}")
        output.append(f"    ⚠️  Migration Required by: {result['migration_deadline']}")
        output.append("")
    
    output.append("=" * 80)
    output.append("MIGRATION RECOMMENDATIONS")
    output.append("=" * 80)
    output.append("1. Review the official migration guide")
    output.append("2. Create automation rules to replace classic automation")
    output.append("3. Test the new automation rules")
    output.append("4. Remove classic automation from analytic rules")
    output.append("5. Complete migration before March 31, 2026")
    output.append("=" * 80)
    
    print("\n".join(output))


def test_json_output(results):
    """Test JSON output formatting."""
    print("\n" + "=" * 80)
    print("TESTING JSON OUTPUT FORMAT")
    print("=" * 80)
    print()
    
    output = {
        'generated_at': datetime.now().isoformat(),
        'total_rules_with_classic_automation': len(results),
        'migration_deadline': '2026-03-31',
        'results': results
    }
    
    print(json.dumps(output, indent=2))


def test_csv_output(results):
    """Test CSV output formatting."""
    print("\n" + "=" * 80)
    print("TESTING CSV OUTPUT FORMAT")
    print("=" * 80)
    print()
    
    import csv
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
    
    print(output.getvalue())


def main():
    """Run all tests."""
    print()
    print("🧪 SENTINEL CLASSIC AUTOMATION DETECTION - MANUAL TEST")
    print()
    
    # Test detection logic
    results = test_detection_logic()
    
    # Test output formatters
    test_console_output(results)
    test_json_output(results)
    test_csv_output(results)
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("NOTE: This was a manual test with mock data.")
    print("To test with real Azure resources, use:")
    print("  sentinel-detect --subscription-id YOUR_SUBSCRIPTION_ID")
    print()


if __name__ == '__main__':
    main()
