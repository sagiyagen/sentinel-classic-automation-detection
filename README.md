# Microsoft Sentinel Classic Automation Detection Tool

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Azure](https://img.shields.io/badge/azure-sentinel-0078d4.svg)

A tool to detect Microsoft Sentinel analytic rules using deprecated classic automation (playbooks assigned via `alertRules/actions`) that need migration to the new automation rules model.

## 🚨 Background

Microsoft Sentinel is deprecating the classic method of triggering playbooks directly from analytic rules. The **migration deadline is March 31, 2026**.

### What's Being Deprecated?

- **Classic Automation**: Playbooks assigned directly to alert rules via the `Microsoft.SecurityInsights/alertRules/actions` resource type
- **New Approach**: Automation rules that provide centralized management, better control, and enhanced capabilities

### Why Migrate?

1. **Centralized Management**: Single pane of glass for all automation
2. **Enhanced Capabilities**: Set execution order, expiration dates, and complex conditions
3. **Future Compatibility**: Classic automation will stop working after March 2026
4. **Improved Efficiency**: Trigger playbooks across multiple rules with one automation rule

## 📋 Features

- ✅ Scans all Sentinel workspaces in an Azure subscription
- ✅ Detects analytic rules with classic automation (alertRules/actions)
- ✅ Identifies playbooks that need to be migrated
- ✅ Multiple output formats: Console, JSON, CSV
- ✅ Detailed migration guidance and recommendations
- ✅ Support for both DefaultAzureCredential and Azure CLI authentication

## 🔧 Prerequisites

- Python 3.8 or higher
- Azure subscription with Microsoft Sentinel workspace(s)
- One of the following authentication methods:
  - Azure CLI (`az login`)
  - Service Principal
  - Managed Identity
  - Other Azure Identity credential types

### Required Azure Permissions

The account/identity running this tool needs the following permissions:

- `Microsoft.SecurityInsights/alertRules/read`
- `Microsoft.SecurityInsights/alertRules/actions/read`
- `Microsoft.OperationalInsights/workspaces/read`
- `Microsoft.Resources/subscriptions/resourceGroups/read`

Recommended built-in role: **Microsoft Sentinel Reader** or higher

## 📦 Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/sagiyagen/sentinel-classic-automation-detection.git
cd sentinel-classic-automation-detection

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 2: Install dependencies only

```bash
pip install azure-identity azure-mgmt-securityinsight azure-mgmt-resource
```

## 🚀 Usage

### Basic Usage

```bash
# Scan all workspaces in a subscription
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012
```

### Scan Specific Workspace

```bash
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \
                --resource-group myResourceGroup \
                --workspace-name mySentinelWorkspace
```

### Output Formats

#### Console Output (Default)

```bash
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012
```

#### JSON Output

```bash
# Print to console
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \
                --output-format json

# Save to file
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \
                --output-format json \
                --output-file results.json
```

#### CSV Output

```bash
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \
                --output-format csv \
                --output-file results.csv
```

### Authentication Options

#### Azure CLI (Default)

```bash
# Login with Azure CLI first
az login

# Run the tool using CLI credentials
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012 \
                --use-cli-credential
```

#### DefaultAzureCredential

```bash
# Uses environment variables, managed identity, Azure CLI, etc.
sentinel-detect --subscription-id 12345678-1234-1234-1234-123456789012
```

## 📊 Sample Output

### Console Output

```
================================================================================
MICROSOFT SENTINEL CLASSIC AUTOMATION DETECTION REPORT
================================================================================
Generated: 2025-12-17 10:30:00
Total Rules with Classic Automation: 3
================================================================================

📊 Workspace: MySentinelWorkspace (MyResourceGroup)
   Rules requiring migration: 3
--------------------------------------------------------------------------------

  [1] Suspicious Login Activity
      Rule ID: suspicious-login-rule
      Type: Scheduled
      Severity: High
      Enabled: True
      Classic Automations: 2
      Playbooks:
        - /subscriptions/.../Microsoft.Logic/workflows/EnrichmentPlaybook
        - /subscriptions/.../Microsoft.Logic/workflows/NotificationPlaybook
      ⚠️  Migration Required by: 2026-03-31

  [2] Malware Detection Alert
      Rule ID: malware-detection
      Type: Scheduled
      Severity: Critical
      Enabled: True
      Classic Automations: 1
      Playbooks:
        - /subscriptions/.../Microsoft.Logic/workflows/IsolationPlaybook
      ⚠️  Migration Required by: 2026-03-31

================================================================================
MIGRATION RECOMMENDATIONS
================================================================================
1. Review the official migration guide:
   https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules
2. Create automation rules to replace classic automation
3. Test the new automation rules thoroughly
4. Remove classic automation from analytic rules
5. Complete migration before March 31, 2026
================================================================================
```

### JSON Output

```json
{
  "generated_at": "2025-12-17T10:30:00.000000",
  "total_rules_with_classic_automation": 2,
  "migration_deadline": "2026-03-31",
  "results": [
    {
      "workspace_name": "MySentinelWorkspace",
      "resource_group": "MyResourceGroup",
      "rule_id": "suspicious-login-rule",
      "rule_display_name": "Suspicious Login Activity",
      "rule_type": "Scheduled",
      "enabled": true,
      "severity": "High",
      "classic_automation_count": 2,
      "actions": [
        {
          "action_id": "action-1",
          "logic_app_resource_id": "/subscriptions/.../Microsoft.Logic/workflows/EnrichmentPlaybook",
          "trigger_uri": "Configured"
        }
      ],
      "migration_required": true,
      "migration_deadline": "2026-03-31"
    }
  ]
}
```

## 🔄 Migration Guide

After identifying rules with classic automation:

1. **Document Current State**
   - Export the detection results (JSON or CSV)
   - Document which playbooks are triggered by each rule

2. **Create Automation Rules**
   - Navigate to Microsoft Sentinel > Automation
   - Create new automation rules to replace classic automation
   - Configure the same playbooks with appropriate conditions

3. **Test New Automation**
   - Thoroughly test automation rules in a non-production environment
   - Verify playbooks trigger correctly
   - Check incident enrichment and response

4. **Remove Classic Automation**
   - Once automation rules are validated, remove classic automation from analytic rules
   - Re-run this tool to verify no classic automation remains

5. **Monitor and Validate**
   - Monitor automation rule execution
   - Validate incident response workflows

### Official Migration Resources

- [Migrate playbooks to automation rules](https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules)
- [Create and manage automation rules](https://learn.microsoft.com/azure/sentinel/create-manage-use-automation-rules)
- [Automation rules documentation](https://learn.microsoft.com/azure/sentinel/automate-incident-handling-with-automation-rules)

## 🛠️ Development

### Running from Source

```bash
# Run without installing
python -m sentinel_detector.cli --subscription-id YOUR_SUB_ID
```

### Project Structure

```
sentinel-classic-automation-detection/
├── sentinel_detector/
│   ├── __init__.py          # Package initialization
│   ├── azure_client.py      # Azure API client
│   ├── detector.py          # Detection logic
│   ├── formatter.py         # Output formatters
│   └── cli.py               # Command-line interface
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for use with Microsoft Sentinel deployments.

## ⚠️ Disclaimer

This tool is provided as-is without warranty. Always test in a non-production environment first. The tool only detects classic automation and does not perform any modifications to your Sentinel configuration.

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Review Microsoft's official Sentinel documentation
- Contact your Azure support team

## 🔗 Related Links

- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [Azure Security Insights Python SDK](https://learn.microsoft.com/python/api/overview/azure/mgmt-securityinsight-readme)
- [Azure Identity Python SDK](https://learn.microsoft.com/python/api/overview/azure/identity-readme)