
# AWS Elastic Beanstalk CI/CD Deployment

A Python Flask web application deployed using AWS Elastic Beanstalk with an automated CI/CD pipeline powered by GitHub, AWS CodePipeline, and AWS CodeBuild.

## 1. Project Overview

**Objective:** Implement automated application deployment using AWS Elastic Beanstalk (PaaS).

This project demonstrates how developers can push application changes to GitHub and automatically build and deploy those changes to an AWS Elastic Beanstalk environment.

### Key Features

- Python Flask web application.
- Automated CI/CD using AWS CodePipeline.
- Application packaging using AWS CodeBuild.
- Managed application deployment using Elastic Beanstalk.
- Environment-specific configuration using environment variables.
- Application health monitoring endpoint.
- GitHub push-based pipeline triggering.

## 2. Architecture

```text
Developer
   |
   | Git Push
   v
GitHub Repository
(AWS-Projects)
   |
   v
AWS CodePipeline
   |
   v
AWS CodeBuild
   |
   | Build and Package Application
   v
Build Artifact
   |
   v
AWS Elastic Beanstalk
   |
   v
Python Flask Application
```

**AWS Region:** Asia Pacific (Mumbai) - `ap-south-1`

## 3. Repository Structure

```text
AWS-Projects/
│
└── 03-elastic-beanstalk/
    │
    ├── application.py
    ├── requirements.txt
    ├── buildspec.yml
    └── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `application.py` | Main Flask application containing routes, HTML interface, and environment configuration. |
| `requirements.txt` | Contains Python dependencies required by the application. |
| `buildspec.yml` | Defines AWS CodeBuild instructions, build phases, validation, and artifact packaging. |
| `README.md` | Project documentation and implementation details. |

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web application framework |
| Gunicorn | Python WSGI application server |
| GitHub | Source code management |
| AWS CodePipeline | CI/CD workflow orchestration |
| AWS CodeBuild | Application build and packaging |
| AWS Elastic Beanstalk | Managed application hosting |
| Amazon EC2 | Underlying compute infrastructure |
| Amazon S3 | Pipeline artifact storage |
| Amazon CloudWatch | Build and application logs |

## 5. Application Implementation

### application.py

The application is developed using Flask.

It provides two main endpoints:

**1. Home Page - `/`**

Displays:
- Welcome message.
- Deployment pipeline visualization.
- Application environment.
- Application version.
- Custom application message.
- Platform information.

**2. Health Check - `/health`**

Returns application health information in JSON format.

Example response:

```json
{
    "status": "healthy",
    "environment": "development",
    "version": "1.0"
}
```

### Environment Variables

The application uses environment variables to manage configuration without modifying source code.

| Variable | Default Value | Purpose |
|---|---|---|
| `APP_ENV` | `development` | Identifies the application environment. |
| `APP_VERSION` | `1.0` | Defines the application version. |
| `APP_MESSAGE` | `Hello from AWS Elastic Beanstalk!` | Custom message displayed on the home page. |

This approach allows the same application code to run with different configurations in development, staging, and production environments.

## 6. AWS CodeBuild Configuration

The `buildspec.yml` file defines the build process.

### Build Phases

| Phase | Description |
|---|---|
| Install | Configures Python 3.11 runtime. |
| Pre-build | Installs application dependencies using requirements.txt. |
| Build | Validates Python syntax and prepares deployment files. |
| Post-build | Confirms successful completion of the build. |

### Artifact Configuration

CodeBuild packages the application directory:

```yaml
artifacts:
  base-directory: 03-elastic-beanstalk
  files:
    - '**/*'
  discard-paths: no
```

This ensures that the deployment artifact contains the application files rather than the entire monorepo.

## 7. AWS CodePipeline Configuration

The pipeline consists of three stages.

### Stage 1: Source

- Provider: GitHub via GitHub App.
- Repository: `DHRUVRAJPUTTT/AWS-Projects`.
- Branch: `main`.
- Webhook-based change detection.
- File path filter: `03-elastic-beanstalk/**`.

The file path filter ensures that changes to unrelated projects do not trigger this pipeline.

### Stage 2: Build

- Provider: AWS CodeBuild.
- Project: `ElasticBeanstalk-Build`.
- Build specification: `03-elastic-beanstalk/buildspec.yml`.

CodeBuild installs dependencies, validates the application, and creates the deployment artifact.

### Stage 3: Deploy

- Provider: AWS Elastic Beanstalk.
- Application: `ElasticBeanstalkApp`.
- Environment: `ElasticBeanstalk-Dev`.

The deployment stage takes the build artifact and deploys the application to Elastic Beanstalk.

## 8. CI/CD Workflow

The automated deployment workflow:

1. Developer modifies application code.
2. Changes are committed and pushed to GitHub.
3. GitHub triggers AWS CodePipeline.
4. CodePipeline retrieves the latest source revision.
5. CodeBuild executes the buildspec file.
6. Dependencies are installed and application syntax is validated.
7. CodeBuild generates the deployment artifact.
8. CodePipeline sends the artifact to Elastic Beanstalk.
9. Elastic Beanstalk deploys the new application version.
10. Application availability is verified through the browser and health endpoint.

### Git Commands

Run from the repository root:

```powershell
git add 03-elastic-beanstalk/
git commit -m "Update Elastic Beanstalk application"
git push origin main
```

## 9. Local Application Setup

Clone the repository:

```powershell
git clone https://github.com/DHRUVRAJPUTTT/AWS-Projects.git
cd AWS-Projects/03-elastic-beanstalk
```

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the application:

```powershell
python application.py
```

Open the application:

```text
http://127.0.0.1:5000/
```

Health endpoint:

```text
http://127.0.0.1:5000/health
```

## 10. IAM Permissions

The project requires appropriate IAM roles and permissions for communication between AWS services.

- CodePipeline service role: Access to CodeBuild and Elastic Beanstalk deployment actions.
- CodeBuild service role: Access to source artifacts, build artifacts, and CloudWatch Logs.
- Elastic Beanstalk service role: Permissions required for environment management.
- EC2 instance profile: Permissions required by the Elastic Beanstalk EC2 instances.

IAM permissions should follow the principle of least privilege.

## 11. Deployment Results

The project was successfully deployed through AWS CodePipeline.

| Component | Result |
|---|---|
| GitHub Source Stage | Successful |
| AWS CodeBuild Stage | Successful |
| Elastic Beanstalk Deploy Stage | Successful |
| Flask Application | Successfully deployed |
| Health Endpoint | Implemented and verified |
| Automatic Deployment | Tested using GitHub pushes |

The deployed application displayed the environment name, application version, custom message, and deployment platform.

## 12. Cost Management and Cleanup

After successfully completing and verifying the deployment, the Elastic Beanstalk application and environment were deleted to avoid ongoing infrastructure charges.

The GitHub source code and project documentation remain available.

AWS resources such as CodePipeline, CodeBuild, S3 artifacts, CloudWatch Logs, and IAM roles should be reviewed independently for unused resources and potential charges.

## 13. Learning Outcomes

Through this project, I gained practical experience with:

- Platform-as-a-Service (PaaS) deployment.
- AWS Elastic Beanstalk environment management.
- CI/CD pipeline implementation.
- GitHub integration with AWS services.
- Automated application builds using CodeBuild.
- Buildspec configuration and artifact packaging.
- Environment variable injection.
- IAM roles and service permissions.
- Application health checks.
- Automated deployment and version management.
- AWS resource cleanup and cost optimization.

---

**Project:** AWS Elastic Beanstalk Zero-Downtime Deployment

**Developer:** Dhruv Rajput

**Repository:** [AWS-Projects](https://github.com/DHRUVRAJPUTTT/AWS-Projects)

**Technologies:** Python, Flask, GitHub, AWS CodePipeline, AWS CodeBuild, AWS Elastic Beanstalk, Amazon EC2, Amazon S3, CloudWatch.
