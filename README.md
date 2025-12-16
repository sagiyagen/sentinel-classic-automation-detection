# Classic Automation Detection Tool for Microsoft Sentinel

> **⚠️ Community Solution:** This is a community-contributed tool designed to assist with the migration from classic automation to automation rules. While created to help Microsoft Sentinel customers, this is not an official Microsoft product. Use at your own discretion and test in a non-production environment first.

## Overview

As Microsoft Sentinel approaches the deprecation of classic automation, this tool helps you quickly identify analytic rules that still use classic alert-trigger playbooks and need to be migrated to automation rules.

This repository contains two ARM template-based Logic Apps that scan your environment and provide a complete list of impacted analytic rules requiring migration.

> **Learn more:** [Migrate your Microsoft Sentinel alert-trigger playbooks to automation rules](https://learn.microsoft.com/en-us/azure/sentinel/automation/migrate-playbooks-to-automation-rules)

---

## 📦 Available Solutions

### 1. Subscription-Level Detection (Recommended)
**File:** `Classic Automation Detect - Subscription Deployment (Prod).json`

**Best for:**
- Multi-workspace environments
- Enterprise deployments
- Customers who want a comprehensive scan across all workspaces

**What it does:**
- Scans **all** Microsoft Sentinel workspaces within a subscription
- Identifies any analytic rule using classic alert-trigger playbooks
- Provides a consolidated report across your entire subscription

**Permissions granted to the Logic App:**
- `Reader` (subscription scope)
- `Sentinel Reader` (subscription scope)

**Deployment requirements:**
- User must have `Owner` role on the subscription (required for role assignments during deployment)

**Parameters:**
- `workflows_classic_automation_detect_name`: Name for the Logic App (default: `classic-automation-detect`)
- `location`: Azure region for deployment (default: `eastus`)
- `resourceGroupName`: Resource group where the Logic App will be deployed
- `subscriptionId`: Target subscription (default: current subscription)

---

### 2. Workspace-Level Detection
**File:** `Classic Automation Detect - Workspace level (Prod).json`

**Best for:**
- Single-workspace customers
- Scenarios where you don't have subscription-level Owner permissions
- Granular, workspace-specific scanning

**What it does:**
- Scans a **specific** Microsoft Sentinel workspace
- Identifies analytic rules using classic alert-trigger playbooks within that workspace

**Permissions granted to the Logic App:**
- `Sentinel Reader` (workspace scope)

**Deployment requirements:**
- User must have `Owner` role on the workspace (required for role assignments during deployment)

**Parameters:**
- `workflows_classic_automation_detect_name`: Name for the Logic App (default: `classic-automation-detect-workspace`)
- `location`: Azure region for deployment (default: workspace location)
- `workspaceName`: **Required** - Name of the Log Analytics workspace hosting Microsoft Sentinel
- `workspaceResourceGroup`: Resource group of the Sentinel workspace (default: current resource group)
- `subscriptionId`: Target subscription (default: current subscription)

---

## 🚀 Deployment Guide

### Quick Deploy

Click the button below to deploy directly to Azure:

**Subscription-Level Detection:**

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fyour-repo%2Fclassic-automation-migration%2Fmain%2FClassic%20Automation%20Detect%20-%20Subscription%20Deployment%20(Prod).json)

**Workspace-Level Detection:**

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fyour-repo%2Fclassic-automation-migration%2Fmain%2FClassic%20Automation%20Detect%20-%20Workspace%20level%20(Prod).json)

> **Note:** Update the URLs above with your actual GitHub repository path once you host these templates.

---

### Manual Deployment Steps

If you prefer to deploy manually or need to customize the template:

### Step 1: Build Your Own Template
1. Navigate to [Deploy a custom template](https://portal.azure.com/#create/Microsoft.Template) in Azure Portal
2. Click on **"Build your own template in the editor"**

![Build your own template in the editor](./images/build-template.png)

---

### Step 2: Paste the Template Content
1. **Delete** any existing content in the editor
2. Copy the contents of either:
   - `Classic Automation Detect - Subscription Deployment (Prod).json`, or
   - `Classic Automation Detect - Workspace level (Prod).json`
3. **Paste** the content into the editor
4. Click **Save**

![Template editor with ARM template JSON](./images/template-editor.png)

---

### Step 3: Configure Parameters

#### For Subscription-Level Deployment:
- **Subscription**: Select the target subscription
- **Resource Group**: Choose or create a resource group for the Logic App
- **Workflows Classic Automation Detect Name**: (Optional) Customize the Logic App name
- **Location**: (Optional) Specify deployment region
- **Resource Group Name**: Resource group where Logic App will be created

#### For Workspace-Level Deployment:
- **Subscription**: Select the target subscription
- **Resource Group**: Choose the resource group (typically where your workspace exists)
- **Workspace Name**: **Required** - Enter your Sentinel workspace name
- **Workspace Resource Group**: (Optional) Specify if workspace is in a different resource group
- **Workflows Classic Automation Detect Name**: (Optional) Customize the Logic App name

![Configure deployment parameters](./images/configure-parameters.png)

---

### Step 4: Review and Create
1. Click **Review + create**
2. Review the parameters and permissions
3. Click **Create**

The deployment will:
- Create the Logic App with a system-assigned managed identity
- Assign necessary role permissions automatically
- Configure the Logic App to run on a 3-week recurrence (can be triggered manually)

---

## ▶️ Running the Detection

### Step 1: Locate the Logic App
After deployment completes, locate your Logic App by:
- Navigating to the resource group
- Checking **Deployment details** in the deployment output
- Searching for the Logic App name in the Azure Portal

---

### Step 2: Run the Logic App Manually
1. Open the Logic App
2. Go to **Overview**
3. Click **Run Trigger** → **Run**

![Run the Logic App manually](./images/run-logic-app.png)

---

### Step 3: Review the Results
1. Navigate to **Run history**
2. Click on the most recent run
3. Expand the workflow to view all actions
4. Locate the final action: **"Impacted_Analytic_Rules_List_"**

This output contains a JSON array of all analytic rules that still use classic automation and require migration.

![Logic App run history showing impacted rules output](./images/run-output.png)

---

## 📊 Understanding the Output

The **"Impacted_Analytic_Rules_List_"** action returns an array of objects with the following structure:

```json
[
  {
    "WorkspaceName": "YourSentinelWorkspace",
    "AnalyticRuleName": "Suspicious Login Activity",
    "RuleId": "12345678-1234-1234-1234-123456789abc",
    "Enabled": true
  },
  {
    "WorkspaceName": "YourSentinelWorkspace",
    "AnalyticRuleName": "Malware Detection Alert",
    "RuleId": "87654321-4321-4321-4321-cba987654321",
    "Enabled": false
  }
]
```

### Fields:
- **WorkspaceName**: The Microsoft Sentinel workspace containing the analytic rule
- **AnalyticRuleName**: Display name of the analytic rule
- **RuleId**: Unique identifier for the analytic rule
- **Enabled**: Whether the rule is currently active

---

## 🔄 What to Do Next

For each analytic rule listed in the output, follow Microsoft's official migration guide:

👉 [Migrate your Microsoft Sentinel alert-trigger playbooks to automation rules](https://learn.microsoft.com/en-us/azure/sentinel/automation/migrate-playbooks-to-automation-rules)

### Migration Overview (2-3 steps per rule):

1. **Create an automation rule**
   - From the analytic rule (if used by a single rule), or
   - From the Automation page (if used by multiple rules)

2. **Re-bind the playbook**
   - Connect the playbook to the new automation rule

3. **Remove the classic binding**
   - Disable or remove the old alert-trigger automation

---

## 🔍 When to Use Each Version

| Scenario | Recommended Version |
|----------|---------------------|
| Multiple workspaces across a subscription | **Subscription-Level** |
| Enterprise-wide scan | **Subscription-Level** |
| Single workspace environment | **Workspace-Level** |
| No subscription Owner permissions | **Workspace-Level** |
| Want minimal permission scope | **Workspace-Level** |
| Need to scan multiple workspaces without subscription permissions | **Workspace-Level** (deploy per workspace) |

---

## 🛠️ Technical Details

### Logic App Behavior

Both versions:
- Run on a **3-week recurrence** by default (configurable)
- Use **Managed Identity** for authentication
- Query Microsoft Sentinel APIs to retrieve analytic rules and their associated actions
- Filter rules that have classic automation (alert-trigger actions) configured
- Return results in a structured JSON format

### API Calls Made

1. **List Workspaces** (Subscription-Level only)
   - Retrieves all Log Analytics workspaces in the subscription

2. **List Analytic Rules**
   - Gets all analytic rules from each workspace

3. **Get Analytic Rule Actions**
   - Retrieves configured actions (playbooks) for each rule
   - Identifies rules with classic automation bindings

### Expected Failures

The Logic App may encounter expected failures when:
- A Log Analytics workspace is not onboarded to Microsoft Sentinel
- Permissions are insufficient for specific workspaces

These failures are **gracefully handled** and won't cause the overall workflow to fail.

---

## 🔐 Permissions Reference

### Subscription-Level Version
- **Reader** (`acdd72a7-3385-48ef-bd42-f606fba81ae7`) - Subscription scope
- **Sentinel Reader** (`8d289c81-5878-46d4-8554-54e1e3d8b5cb`) - Subscription scope

### Workspace-Level Version
- **Sentinel Reader** (`8d289c81-5878-46d4-8554-54e1e3d8b5cb`) - Workspace scope

---

## ❓ FAQ

### Can I run this multiple times?
Yes! The Logic App is non-destructive and only reads configuration data. You can run it as many times as needed.

### Will this modify my analytic rules?
No. This tool only **detects** and **reports** on analytic rules. It does not make any changes to your environment.

### What if I have hundreds of analytic rules?
The Logic App is designed to handle large environments. It processes workspaces and rules iteratively and returns all results in a single output.

### Can I customize the recurrence schedule?
Yes. After deployment, you can modify the Logic App trigger to run on any schedule you prefer, or disable the recurrence entirely and run it manually only.

### Do I need to keep the Logic App after migration?
Once you've completed all migrations, you can safely delete the Logic App. However, you may want to keep it to periodically verify that no new classic automations are added.

---

## 📚 Additional Resources

- [Microsoft Sentinel Automation Documentation](https://learn.microsoft.com/en-us/azure/sentinel/automation/)
- [Automation Rules Overview](https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-incident-handling-with-automation-rules)
- [Logic Apps Documentation](https://learn.microsoft.com/en-us/azure/logic-apps/)
- [Managed Identities in Azure](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)

---

## 📝 License

These ARM templates are provided as-is for use with Microsoft Sentinel environments.

---

## 🤝 Support

For issues or questions:
- Review the [official migration guide](https://learn.microsoft.com/en-us/azure/sentinel/automation/migrate-playbooks-to-automation-rules)
- Check the Logic App run history for detailed error messages
- Ensure you have the required permissions for deployment

---

**Last Updated:** December 2025  
**Version:** 1.0 (Production)  
**Type:** Community Solution
