PROJECT OVERVIEW:
This project implements a multi-cloud cost hygiene and automation workflow for the fictional client NimbusKart .The solution provisions AWS infrastructure locally using Terraform and LocalStack, scans resources, detects unnecessary cloud cost usage, and generates reports in JSON and Markdown format using a custom Cost Janitor automation script, and integrates the workflow into CI/CD using GitHub Actions.
------------------------------------------------
HOW TO RUN LOCALLY: 

git clone https://github.com/omshresth/devops-assign.git

cd ./devops-assign

docker run --rm -d -p 4566:4566 \
--name localstack \
localstack/localstack:3

pip install terraform-local

cd terraform

tflocal init

tflocal apply -auto-approve

cd ..

python janitor/janitor.py --dry-run
----------------------------------------------------
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

--------------------------------------------------------
Decisions & Deviations:
- SSH access from 0.0.0.0/0 is insecure and would normally be restricted to trusted IP ranges or VPN access, but was kept to align with assignment requirements.
- Public subnets were used for simplicity in LocalStack, though production workloads should use private subnets behind a load balancer.
- Cost estimates use static pricing constants instead of live AWS Pricing APIs to keep the project fully offline and reproducible.
- Automatic deletion is disabled by default to reduce risk of accidental destructive actions.

---------------------------------------------------------

