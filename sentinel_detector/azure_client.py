"""
Azure client for interacting with Microsoft Sentinel.
"""
from typing import List, Dict, Any, Optional
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.mgmt.securityinsight import SecurityInsights
from azure.mgmt.resource import ResourceManagementClient


class SentinelClient:
    """Client for interacting with Microsoft Sentinel API."""
    
    def __init__(self, subscription_id: str, use_cli_credential: bool = False):
        """
        Initialize the Sentinel client.
        
        Args:
            subscription_id: Azure subscription ID
            use_cli_credential: If True, use Azure CLI credentials only
        """
        self.subscription_id = subscription_id
        if use_cli_credential:
            self.credential = AzureCliCredential()
        else:
            self.credential = DefaultAzureCredential()
        
        self.security_insights_client = SecurityInsights(
            credential=self.credential,
            subscription_id=subscription_id
        )
        self.resource_client = ResourceManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )
    
    def list_sentinel_workspaces(self) -> List[Dict[str, Any]]:
        """
        List all Log Analytics workspaces with Sentinel enabled.
        
        Returns:
            List of workspace dictionaries with id, name, and resource_group
        """
        workspaces = []
        
        # Get all Log Analytics workspaces
        for resource in self.resource_client.resources.list(
            filter="resourceType eq 'Microsoft.OperationalInsights/workspaces'"
        ):
            workspace_info = {
                'id': resource.id,
                'name': resource.name,
                'resource_group': resource.id.split('/')[4],  # Extract RG from resource ID
                'location': resource.location
            }
            workspaces.append(workspace_info)
        
        return workspaces
    
    def get_alert_rules(self, resource_group: str, workspace_name: str) -> List[Any]:
        """
        Get all alert rules from a Sentinel workspace.
        
        Args:
            resource_group: Resource group name
            workspace_name: Log Analytics workspace name
            
        Returns:
            List of alert rules
        """
        alert_rules = []
        
        try:
            rules_list = self.security_insights_client.alert_rules.list(
                resource_group_name=resource_group,
                workspace_name=workspace_name
            )
            alert_rules = list(rules_list)
        except Exception as e:
            print(f"Error retrieving alert rules for workspace {workspace_name}: {str(e)}")
        
        return alert_rules
    
    def get_alert_rule_actions(self, resource_group: str, workspace_name: str, 
                               rule_id: str) -> List[Any]:
        """
        Get actions (classic automation) associated with an alert rule.
        
        Args:
            resource_group: Resource group name
            workspace_name: Log Analytics workspace name
            rule_id: Alert rule ID
            
        Returns:
            List of actions associated with the alert rule
        """
        actions = []
        
        try:
            actions_list = self.security_insights_client.actions.list_by_alert_rule(
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                rule_id=rule_id
            )
            actions = list(actions_list)
        except Exception as e:
            # It's expected that many rules won't have actions
            # Only log if it's not a 404
            if "NotFound" not in str(e):
                print(f"Error retrieving actions for rule {rule_id}: {str(e)}")
        
        return actions
