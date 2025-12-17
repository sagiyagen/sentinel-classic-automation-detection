# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-17

### Added
- Initial release of Sentinel Classic Automation Detection Tool
- Detection of analytic rules using deprecated classic automation (alertRules/actions)
- Support for scanning all workspaces in a subscription
- Support for scanning specific workspace
- Multiple output formats: Console, JSON, CSV
- Azure authentication via DefaultAzureCredential and Azure CLI
- Comprehensive documentation and examples
- Sample ARM templates showing classic automation and migration approach
- Quick start guide for getting started
- Manual testing script with mock data

### Features
- Scans Microsoft Sentinel workspaces for analytic rules with classic automation
- Identifies playbooks that need migration to automation rules
- Provides detailed migration guidance and recommendations
- Supports filtering by resource group and workspace
- Exit codes for CI/CD integration (0=no issues, 1=migration needed, 2=error)

### Documentation
- Comprehensive README with usage examples
- Quick start guide
- Example ARM templates
- Migration recommendations
- API reference for Python package

### Context
This tool was created in response to Microsoft's announcement that classic automation for Sentinel analytic rules will be deprecated on March 31, 2026. Organizations need to migrate their playbook triggers from analytic rules to the new automation rules model.
