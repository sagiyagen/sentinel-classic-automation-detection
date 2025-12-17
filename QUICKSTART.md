# Quick Start Guide

This guide will help you get started with the Sentinel Classic Automation Detection Tool.

## Prerequisites

- Python 3.8+
- Azure CLI (for authentication)
- Access to an Azure subscription with Microsoft Sentinel

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sagiyagen/sentinel-classic-automation-detection.git
cd sentinel-classic-automation-detection
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install the Tool

```bash
pip install -e .
```

## Authentication

### Option 1: Azure CLI (Recommended for Getting Started)

```bash
# Login to Azure
az login

# Set your default subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Option 2: Service Principal

```bash
# Set environment variables
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

## Basic Usage

### Scan All Workspaces

```bash
sentinel-detect --subscription-id YOUR_SUBSCRIPTION_ID --use-cli-credential
```

### Scan Specific Workspace

```bash
sentinel-detect --subscription-id YOUR_SUBSCRIPTION_ID \
                --resource-group myResourceGroup \
                --workspace-name mySentinelWorkspace \
                --use-cli-credential
```

### Save Results to JSON

```bash
sentinel-detect --subscription-id YOUR_SUBSCRIPTION_ID \
                --output-format json \
                --output-file detection-results.json \
                --use-cli-credential
```

### Save Results to CSV

```bash
sentinel-detect --subscription-id YOUR_SUBSCRIPTION_ID \
                --output-format csv \
                --output-file detection-results.csv \
                --use-cli-credential
```

## Understanding the Results

The tool will report:

1. **Total Rules with Classic Automation**: Number of analytic rules that need migration
2. **Rule Details**: For each rule:
   - Display name and ID
   - Type and severity
   - Associated playbooks (Logic Apps)
   - Migration deadline (March 31, 2026)

### Exit Codes

- `0`: No rules with classic automation found (success)
- `1`: Rules with classic automation were found (requires action)
- `2`: Error occurred during execution

## Testing Without Azure Access

You can test the tool's output formats without Azure credentials:

```bash
python test_manual.py
```

This runs with mock data to demonstrate the tool's functionality.

## What to Do If Rules Are Found

If the tool finds rules with classic automation:

1. **Document**: Export results to JSON or CSV for tracking
2. **Plan**: Review which playbooks are associated with which rules
3. **Migrate**: Follow the [migration guide](https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules)
4. **Verify**: Re-run the tool after migration to confirm

## Common Issues

### "No module named 'sentinel_detector'"

**Solution**: Install the package:
```bash
pip install -e .
```

### Authentication Errors

**Solution**: Ensure you're logged in:
```bash
az login
az account show  # Verify you're logged into the correct subscription
```

### Permission Denied

**Solution**: Ensure your account has the necessary permissions:
- Microsoft.SecurityInsights/alertRules/read
- Microsoft.SecurityInsights/alertRules/actions/read
- Microsoft.OperationalInsights/workspaces/read

## Next Steps

1. Run the detection tool on your subscription
2. Review the [full README](README.md) for detailed documentation
3. Check the [examples](examples/) directory for ARM template samples
4. Plan your migration using the official Microsoft documentation

## Need Help?

- Review the [README.md](README.md) for detailed documentation
- Check [examples/README.md](examples/README.md) for ARM template examples
- Consult [Microsoft's migration guide](https://learn.microsoft.com/azure/sentinel/automation/migrate-playbooks-to-automation-rules)
