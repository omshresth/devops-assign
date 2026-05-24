Candidate name:OM SHRESTH  
Email:shresthk02@gmail.com  
Date submitted: 2026-05-24  
Hours spent (approximate): ~22-26 hours 
---
Deliverables checklist

-  Part A: Terraform code under /terraform applies cleanly on LocalStack
-  Part A: terraform validate and terraform fmt -check both pass
-  Part B: Janitor script runs in --dry-run mode and produces report.json
-  Part B: GitHub Actions workflow runs green on a fresh PR
-  Part B: --delete mode respects Protected=true tag
-  Part C: DESIGN.md is present and within 2 pages
-  Walkthrough video link below is accessible (unlisted is fine)
---
Walkthrough video

Link (Loom / YouTube unlisted / Google Drive):  
ADD_VIDEO_LINK_HERE

Length: max 5 minutes

---

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

One of the issue with AI-generated suggestions:
- Like in setting up Local Stack it has told to use latest image but in real latest image was in paid or pro version so i use the older version
-----
Known limitations:
Some Terraform lifecycle features required LocalStack compatibility adjustments
Multi-region support is not implemented