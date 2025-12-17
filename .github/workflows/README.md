# GitHub Actions Workflow

This directory contains a sample GitHub Actions workflow that demonstrates how to integrate the Sentinel Classic Automation Detection Tool into your CI/CD pipeline.

## Workflow: detect-classic-automation.yml

This workflow automatically scans your Azure Sentinel workspaces for analytic rules with classic automation.

### Features:

- **Scheduled Runs**: Runs weekly on Mondays at 9 AM UTC
- **Manual Trigger**: Can be triggered manually via workflow_dispatch
- **Azure OIDC Authentication**: Uses federated credentials for secure authentication
- **Automated Reporting**: Creates/updates GitHub issues when rules are found
- **Artifact Storage**: Saves detection results as artifacts

### Setup Instructions:

#### 1. Configure Azure OIDC Authentication

Follow the [Azure OIDC guide](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure) to set up federated credentials.

#### 2. Add GitHub Secrets

Add the following secrets to your repository:

- `AZURE_CLIENT_ID`: Azure service principal client ID
- `AZURE_TENANT_ID`: Azure tenant ID
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID to scan

#### 3. Grant Permissions

Ensure the service principal has the following permissions:

- `Microsoft.SecurityInsights/alertRules/read`
- `Microsoft.SecurityInsights/alertRules/actions/read`
- `Microsoft.OperationalInsights/workspaces/read`
- `Microsoft.Resources/subscriptions/resourceGroups/read`

Recommended role: **Microsoft Sentinel Reader**

### How It Works:

1. **Checkout**: Clones the repository
2. **Setup**: Installs Python and dependencies
3. **Authentication**: Logs into Azure using OIDC
4. **Detection**: Runs the detection tool
5. **Upload**: Saves results as an artifact
6. **Issue Creation**: Creates/updates a GitHub issue if rules are found
7. **Status**: Fails the workflow if migration is required

### Customization:

You can customize the workflow to:

- Change the schedule (modify the `cron` expression)
- Scan specific workspaces (add `--resource-group` and `--workspace-name` flags)
- Adjust notification behavior (modify the issue creation logic)
- Send alerts to other systems (add steps for Slack, Teams, etc.)

### Example Issue Format:

When rules with classic automation are detected, the workflow creates an issue like:

```markdown
## ⚠️ Sentinel Classic Automation Migration Required

**Total Rules with Classic Automation:** 3
**Migration Deadline:** 2026-03-31

### Rules Requiring Migration:

**1. Suspicious Login Activity**
- Workspace: sentinel-ws
- Resource Group: sentinel-rg
- Severity: High
- Classic Automations: 2
- Playbooks:
  - /subscriptions/.../Microsoft.Logic/workflows/EnrichmentPlaybook
  - /subscriptions/.../Microsoft.Logic/workflows/NotificationPlaybook

[...]

### Action Required:

1. Review the migration guide
2. Create automation rules to replace classic automation
3. Test the new automation rules
4. Remove classic automation from analytic rules
5. Re-run this workflow to verify migration
```

### Testing:

You can test the workflow manually:

1. Go to the **Actions** tab in your GitHub repository
2. Select **Sentinel Classic Automation Detection**
3. Click **Run workflow**
4. Enter your subscription ID
5. Click **Run workflow**

### Viewing Results:

Results are available in two places:

1. **Artifacts**: Download the `detection-results.json` artifact from the workflow run
2. **Issues**: If rules are found, an issue will be created with details

### Integration Examples:

#### Send Slack Notification:

Add this step after the detection:

```yaml
- name: Send Slack notification
  if: steps.detection.outcome == 'failure'
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "⚠️ Sentinel Classic Automation Migration Required",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Found rules with classic automation requiring migration by 2026-03-31"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Send Email:

Add this step to send email notifications:

```yaml
- name: Send email notification
  if: steps.detection.outcome == 'failure'
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Sentinel Classic Automation Migration Required
    body: file://detection-results.json
    to: security-team@example.com
```

## Alternative: Azure DevOps Pipeline

If you're using Azure DevOps, here's a sample pipeline:

```yaml
trigger:
  schedules:
  - cron: "0 9 * * 1"
    displayName: Weekly Sentinel scan
    branches:
      include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    pip install -r requirements.txt
    pip install -e .
  displayName: 'Install dependencies'

- task: AzureCLI@2
  inputs:
    azureSubscription: 'YourServiceConnection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      sentinel-detect \
        --subscription-id $(AZURE_SUBSCRIPTION_ID) \
        --output-format json \
        --output-file $(Build.ArtifactStagingDirectory)/detection-results.json \
        --use-cli-credential

- task: PublishBuildArtifacts@1
  condition: always()
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/detection-results.json'
    artifactName: 'detection-results'
```

## Questions?

For more information, refer to:
- [Main README](../README.md)
- [Quick Start Guide](../QUICKSTART.md)
- [Example Usage](../example_usage.py)
