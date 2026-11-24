# AWS Projects

A collection of hands-on AWS, Cloud, and DevOps projects.

## Projects

| # | Project | Services & tools | Overview |
|---|---|---|---|
| 1 | [CodeBuild Python CI Demo](01-codebuild-python-demo/) | AWS CodeBuild, GitHub, Python, Flask, pytest, Amazon S3, CloudWatch Logs, IAM | GitHub-triggered CI pipeline that installs dependencies, runs pytest, and publishes a ZIP artifact to S3 when tests pass. |
| 2 | CodeDeploy EC2 Application Deployment | AWS CodePipeline, AWS CodeDeploy, Amazon EC2, IAM, Nginx | In-place deployment to EC2 using the CodeDeploy agent, an AppSpec file, and lifecycle hook scripts. Implementation pending. |

## Repository structure

```text
AWS-Projects/
├── README.md
├── 01-codebuild-python-demo/
│   ├── app.py
│   ├── buildspec.yml
│   ├── requirements.txt
│   ├── test_app.py
│   └── README.md
└── 02-codedeploy-ec2/   (planned)
```

## Planned projects

- AWS CodeDeploy application deployment to EC2
- Terraform-based AWS infrastructure
- CloudWatch monitoring and alerting
- S3 static website hosting

## Notes

The CodeBuild demo is included here as a portfolio copy. Its original repository remains available at [codebuild-python-demo](https://github.com/DHRUVRAJPUTTT/codebuild-python-demo). The original AWS CodeBuild project and webhook are not automatically redirected to this portfolio copy.

## Author

Dhruv Rajput · [GitHub](https://github.com/DHRUVRAJPUTTT)
