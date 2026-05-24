
The system automatically provisions infrastructure, 


Architecture Design:

GitHub Actions
        ↓
Start LocalStack Container
        ↓
Terraform Infrastructure Deployment
        ↓
Python Cost Janitor Scanner
        ↓
Resource Analysis
        ↓
JSON + Markdown Reports
        ↓
Upload Artifacts

Components Used:
1. Terraform = is used as the Infrastructure as Code (IaC) tool.

Purpose:
Provision mock AWS infrastructure
Create EC2 instances
Create EBS volumes
Create S3 buckets
Simulate real cloud resources

Why Terraform?
Industry standard IaC tool
Reproducible infrastructure
Easy automation
CI/CD friendly

2. LocalStack = is used to simulate AWS services locally.

Purpose:
Avoid using real AWS resources
Run the project without AWS billing
Safe testing environment

Why LocalStack?
Faster development
No real cloud cost
Works well with Terraform and boto3
Good for CI/CD testing

3. Python Janitor Script = performs cloud resource scanning and cost analysis.

Main responsibilities:
Detect unattached EBS volumes
Detect stopped EC2 instances
Detect unused Elastic IPs
Detect missing tags
Generate reports

Libraries used:
boto3
json
argparse
rich
tabulate

Dry Run vs Delete Mode:

1)Dry Run
python janitor.py --dry-run

Purpose:
Scan resources only
No deletion performed
Safe inspection mode

2)Delete Mode
python janitor.py --delete

Purpose:
Automatically delete safe orphan resources
Simulate cleanup automation

Protected Resource Logic
A protection mechanism was implemented using tags.

Example:
Protected=true

If a resource contains this tag:
automatic deletion is skipped
resource is treated as protected

Purpose:
prevent accidental deletion
simulate real production guardrails

Reporting System:-
Two report formats are generated:

JSON Report
Machine-readable report for automation.

Contains:
resource details
estimated cost
tags
suggested actions

Markdown Summary
Human-readable summary.

Purpose:
easy viewing
GitHub artifact usage
quick inspection

CI/CD Workflow
GitHub Actions is used for automation.

Workflow responsibilities:
Checkout repository
Setup Python
Install dependencies
Start LocalStack
Initialize Terraform
Apply infrastructure
Run Cost Janitor
Upload reports as artifacts

Why GitHub Actions?
Fully automated pipeline
Industry standard CI/CD platform
Easy integration with GitHub repositories
Supports containerized workflows
Safety Design Decisions

The project includes several safety mechanisms:

Dry-run mode enabled by default
Protected tag support
Manual delete flag
LocalStack instead of real AWS
Cost estimation before deletion

These decisions help simulate real-world production safety practices.

Future Improvements

Slack notifications
Email alerts
Multi-region scanning
CloudWatch integration
Kubernetes cost analysis
Real AWS account integration
Dashboard visualization