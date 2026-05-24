Overview:
This project implements a multi-cloud cost hygiene and automation workflow for the fictional client NimbusKart using Terraform, LocalStack, Python, and GitHub Actions.
The solution provisions AWS infrastructure locally using Terraform and LocalStack, scans for orphaned or misconfigured resources using a custom Cost Janitor automation script, and integrates the workflow into CI/CD using GitHub Actions.

How To Run Locally:

Add Commands=>  

git clone <repo-url>

cd devops-cost-janitor

docker run --rm -d -p 4566:4566 \
--name localstack \
localstack/localstack

pip install terraform-local

cd terraform

tflocal init

tflocal apply -auto-approve

cd ..

python janitor/janitor.py --dry-run


Architecture Section:

                GitHub Pull Request
                         |
                         v
                GitHub Actions CI
                         |
          --------------------------------
          |                              |
          v                              v
     LocalStack                    Python Janitor
          |                              |
          v                              v
 Terraform Infrastructure         report.json / summary.md
          |
          v
 AWS-like Resources
(VPC, EC2, S3, EBS, EIP)


Decisions & Deviations:
- SSH access from 0.0.0.0/0 is insecure and would normally be restricted to trusted IP ranges or VPN access, but was kept to align with assignment requirements.
- Public subnets were used for simplicity in LocalStack, though production workloads should use private subnets behind a load balancer.
- Cost estimates use static pricing constants instead of live AWS Pricing APIs to keep the project fully offline and reproducible.
- Automatic deletion is disabled by default to reduce risk of accidental destructive actions.

Trade-offs:
With one additional week, I would:

AI Usage Disclosure:
AI tools (primarily ChatGPT) were used during the development of this project for:
- Understanding DevOps concepts
- Learning Terraform and LocalStack
- Designing the project structure
- Writing and improving Python scripts
- Debugging GitHub Actions workflows
- Fixing YAML indentation and CI/CD issues
- Understanding Git and GitHub workflows
- Learning boto3 integration
- Understanding cloud cost optimization logic
- Improving documentation and report formatting

The project was built as a learning-focused implementation where AI was used as a learning assistant and debugging companion throughout the development process.

All setup, testing, integration, troubleshooting, execution, and final verification were performed manually by me.

One issue with AI-generated suggestions:
- Like in setting up Local Stack it has told to use latest image but in real latest image was in paid or pro version so i use the older version

Code written manually:
- The orphan resource detection logic and report generation flow were implemented manually to better understand the automation and safety logic.
