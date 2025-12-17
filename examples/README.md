# Sample ARM Templates

This directory contains sample ARM templates to illustrate the difference between classic automation and the new automation rules approach.

## Files

### sample-rule-with-classic-automation.json

This template shows an analytic rule with **classic automation** (deprecated approach):
- Defines a scheduled analytic rule (`Microsoft.SecurityInsights/alertRules`)
- Includes two playbook actions (`Microsoft.SecurityInsights/alertRules/actions`)
- **This is the pattern that this tool detects and flags for migration**

Key characteristics of classic automation:
```json
{
  "type": "Microsoft.SecurityInsights/alertRules/actions",
  "properties": {
    "logicAppResourceId": "...",
    "triggerUri": "..."
  }
}
```

### sample-automation-rule-migration.json

This template shows the **modern approach** using automation rules:
- Uses `Microsoft.SecurityInsights/automationRules` resource type
- Provides centralized automation management
- Supports complex conditions and multiple actions
- Recommended migration target

Key characteristics of modern automation rules:
```json
{
  "type": "Microsoft.SecurityInsights/automationRules",
  "properties": {
    "triggeringLogic": { ... },
    "actions": [
      {
        "actionType": "RunPlaybook",
        "actionConfiguration": {
          "logicAppResourceId": "..."
        }
      }
    ]
  }
}
```

## Migration Path

1. **Identify**: Use this tool to find rules using classic automation
2. **Plan**: Review the classic automation configuration
3. **Create**: Deploy automation rules like the sample above
4. **Test**: Validate the new automation rules work correctly
5. **Remove**: Delete the classic `alertRules/actions` resources
6. **Verify**: Re-run this tool to confirm migration is complete

## Benefits of Migration

- **Centralized Management**: All automation in one place
- **Better Control**: Set execution order and conditions
- **Enhanced Features**: Expiration dates, complex logic
- **Future-Proof**: Classic automation stops working March 31, 2026

## Additional Resources

- [Official Migration Guide](https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules)
- [Automation Rules Documentation](https://learn.microsoft.com/azure/sentinel/create-manage-use-automation-rules)
