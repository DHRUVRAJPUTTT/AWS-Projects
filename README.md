# AWS Projects

A collection of hands-on AWS, Cloud, and DevOps projects.

## Projects

| # | Project | Services & tools | Overview |
|---|---|---|---|
| 1 | [CodeBuild Python Demo](https://github.com/DHRUVRAJPUTTT/codebuild-python-demo) | AWS CodeBuild, GitHub, Python, Flask, pytest, Amazon S3, CloudWatch Logs, IAM | GitHub-triggered CI pipeline that installs dependencies, runs pytest, and uploads a ZIP artifact to S3 when tests pass. |
| 2 | CodeDeploy EC2 Application Deployment | AWS CodePipeline, AWS CodeDeploy, Amazon EC2, IAM, Nginx | In-place deployment to EC2 using the CodeDeploy agent, an AppSpec file, and lifecycle hook scripts. Implementation pending. |

## Repository structure

```text
AWS-Projects/
├── README.md
├── 01-codebuild-python-demo/
└── 02-codedeploy-ec2/
```

Each project folder will contain its source code, configuration, scripts, and project-specific documentation. The CodeBuild project is currently maintained in its original repository; this index links to it until its files are added here.

## Planned projects

- Terraform-based AWS infrastructure
- CloudWatch monitoring and alerting
- S3 static website hosting

## Author

Dhruv Rajput · [GitHub](https://github.com/DHRUVRAJPUTTT)
