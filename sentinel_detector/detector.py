"""
Detector for identifying analytic rules with classic automation.
"""
from typing import List, Dict, Any
from .azure_client import SentinelClient


class ClassicAutomationDetector:
    """Detects analytic rules using deprecated classic automation."""
    
    def __init__(self, client: SentinelClient):
        """
        Initialize the detector.
        
        Args:
            client: SentinelClient instance
        """
        self.client = client
    
    def detect_all_workspaces(self) -> List[Dict[str, Any]]:
        """
        Detect all rules with classic automation across all workspaces.
        
        Returns:
            List of detection results
        """
        results = []
        
        print("Discovering Sentinel workspaces...")
        workspaces = self.client.list_sentinel_workspaces()
        print(f"Found {len(workspaces)} workspace(s) to scan\n")
        
        for workspace in workspaces:
            workspace_results = self.detect_workspace(
                workspace['resource_group'],
                workspace['name']
            )
            results.extend(workspace_results)
        
        return results
    
    def detect_workspace(self, resource_group: str, workspace_name: str) -> List[Dict[str, Any]]:
        """
        Detect rules with classic automation in a specific workspace.
        
        Args:
            resource_group: Resource group name
            workspace_name: Workspace name
            
        Returns:
            List of detection results for this workspace
        """
        results = []
        
        print(f"Scanning workspace: {workspace_name} (Resource Group: {resource_group})")
        
        # Get all alert rules
        alert_rules = self.client.get_alert_rules(resource_group, workspace_name)
        print(f"  Found {len(alert_rules)} alert rule(s)")
        
        # Check each rule for classic automation
        rules_with_classic_automation = 0
        for rule in alert_rules:
            # Extract rule name from the rule object
            rule_name = rule.name
            
            # Get actions for this rule
            actions = self.client.get_alert_rule_actions(
                resource_group,
                workspace_name,
                rule_name
            )
            
            if actions:
                rules_with_classic_automation += 1
                result = self._create_detection_result(
                    workspace_name,
                    resource_group,
                    rule,
                    actions
                )
                results.append(result)
        
        print(f"  ⚠️  Found {rules_with_classic_automation} rule(s) with classic automation\n")
        
        return results
    
    def _create_detection_result(self, workspace_name: str, resource_group: str,
                                 rule: Any, actions: List[Any]) -> Dict[str, Any]:
        """
        Create a detection result dictionary.
        
        Args:
            workspace_name: Workspace name
            resource_group: Resource group name
            rule: Alert rule object
            actions: List of actions
            
        Returns:
            Detection result dictionary
        """
        # Extract rule properties
        rule_props = rule.as_dict()
        
        # Build action details
        action_details = []
        for action in actions:
            action_dict = action.as_dict()
            action_info = {
                'action_id': action_dict.get('name', 'Unknown'),
                'logic_app_resource_id': action_dict.get('properties', {}).get('logic_app_resource_id', 'Unknown'),
                'trigger_uri': 'Configured' if action_dict.get('properties', {}).get('trigger_uri') else 'Not configured'
            }
            action_details.append(action_info)
        
        result = {
            'workspace_name': workspace_name,
            'resource_group': resource_group,
            'rule_id': rule_props.get('name', 'Unknown'),
            'rule_display_name': rule_props.get('properties', {}).get('display_name', 'Unknown'),
            'rule_type': rule_props.get('kind', 'Unknown'),
            'enabled': rule_props.get('properties', {}).get('enabled', False),
            'severity': rule_props.get('properties', {}).get('severity', 'Unknown'),
            'classic_automation_count': len(actions),
            'actions': action_details,
            'migration_required': True,
            'migration_deadline': '2026-03-31'
        }
        
        return result
