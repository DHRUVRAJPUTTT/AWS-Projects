
# Assignment 5: Containerized CI/CD Pipeline using Docker, Amazon ECR & ECS

## Project Overview

This project demonstrates how to containerize a Python Flask web application using Docker and automate the Docker image build and upload process using AWS CodeBuild and Amazon Elastic Container Registry (ECR).

The project also extends the deployment workflow by running the containerized application on Amazon ECS using AWS Fargate.

Whenever application code is pushed to the GitHub repository, AWS CodeBuild automatically builds the Docker image, tags it, and pushes it to the private ECR repository.

The image is then deployed to an ECS Fargate service to make the application accessible over the internet.

## Project Objectives

- Containerize a Python Flask application using Docker.
- Understand Dockerfiles, images, containers, and port mapping.
- Create a private Docker image repository using Amazon ECR.
- Automate Docker image builds using AWS CodeBuild.
- Configure IAM permissions for secure ECR access.
- Implement automatic GitHub webhook triggers.
- Deploy containerized applications using Amazon ECS.
- Run containers without managing EC2 instances using AWS Fargate.
- Understand task definitions, ECS services, networking, and security groups.

## Architecture

```text
                 GitHub Repository
                        |
                        |
                  GitHub Webhook
                        |
                        v
                  AWS CodeBuild
                        |
                 Build Docker Image
                        |
                  Authenticate
                     with ECR
                        |
                  Tag Docker Image
                        |
                        v
                 Amazon ECR
              (Private Repository)
                        |
                        |
                 Retrieve Image
                        |
                        v
                  Amazon ECS
                 (Task Definition)
                        |
                        v
                  AWS Fargate
                (Running Container)
                        |
                        v
                 Flask Web App
                  Port 5000
                        |
                        v
                   Web Browser
```

**Note:** GitHub-to-CodeBuild-to-ECR automation was implemented using a webhook. The initial ECS deployment was configured and tested separately by creating an ECS service and triggering deployment. A fully automated ECS deployment stage using CodePipeline remains a possible extension.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Web application framework |
| Docker | Application containerization |
| Dockerfile | Defines the container image |
| Gunicorn | Python WSGI application server |
| AWS CodeBuild | Automated Docker image builds |
| Amazon ECR | Private Docker image registry |
| Amazon ECS | Container orchestration |
| AWS Fargate | Serverless container execution |
| AWS IAM | Access control and permissions |
| Amazon CloudWatch | Build and container logs |
| Git & GitHub | Version control and source management |

## Repository Structure

```text
04-docker-ecr-cicd/
│
├── app.py
│
├── requirements.txt
│
├── Dockerfile
│
├── buildspec.yml
│
├── .dockerignore
│
└── README.md
```

## 1. Application Development

A simple Flask application was developed to demonstrate containerization and deployment.

The application provides two endpoints:

### Home Endpoint

```text
GET /
```

Displays the application landing page.

### Health Check Endpoint

```text
GET /health
```

Returns the health status of the application in JSON format.

Example response:

```json
{
  "application": "Docker ECR CI/CD Demo",
  "hostname": "ip-172-31-35-127.ap-south-1.compute.internal",
  "status": "healthy"
}
```

The hostname helps identify the container instance serving the request.

## 2. Docker Containerization

A Dockerfile was created to package the Flask application and its dependencies into a Docker image.

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Dockerfile Explanation

| Instruction | Description |
|---|---|
| FROM | Uses Python 3.11 slim as the base image |
| WORKDIR | Sets the working directory inside the container |
| COPY | Copies application dependencies and source files |
| RUN | Installs required Python packages |
| EXPOSE | Documents application port 5000 |
| CMD | Starts the application using Gunicorn |

### Dependencies

The `requirements.txt` file contains:

```text
Flask==3.1.2
gunicorn==23.0.0
```

Gunicorn is used as the production WSGI server instead of Flask's development server.

## 3. Amazon ECR Repository Creation

An Amazon ECR private repository was created.

| Configuration | Value |
|---|---|
| Repository name | docker-ecr-demo |
| Region | ap-south-1 |
| Visibility | Private |
| Image tag mutability | Mutable |
| Image scanning | Enabled |

ECR stores the Docker images generated by CodeBuild.

Example repository URI:

```text
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/docker-ecr-demo
```

The actual account ID and repository URI can be obtained from the AWS ECR console.

## 4. IAM Configuration

IAM permissions were configured to allow AWS CodeBuild to authenticate with Amazon ECR and upload Docker images.

### CodeBuild Service Role

A service role was created for the CodeBuild project.

Role name:

```text
codebuild-Docker-ECR-Build-service-role
```

### Custom IAM Policy

Policy name:

```text
CodeBuild-ECR-Push-Policy
```

The policy provides permissions for:

- ECR authorization.
- Checking image layers.
- Initiating image uploads.
- Uploading image layers.
- Completing image uploads.
- Pushing Docker images.
- Retrieving images.

The policy was attached to the CodeBuild service role.

### ECS Task Execution Role

An ECS task execution role was configured:

```text
ecsTaskExecutionRole
```

The role uses:

```text
AmazonECSTaskExecutionRolePolicy
```

Its trust relationship allows the ECS Tasks service to assume the role.

This enables ECS to retrieve private ECR images and publish container logs to CloudWatch.

## 5. AWS CodeBuild Configuration

A CodeBuild project was created to automate Docker image creation and upload.

| Configuration | Value |
|---|---|
| Project name | Docker-ECR-Build |
| Source provider | GitHub |
| Repository | DHRUVRAJPUTTT/AWS-Projects |
| Branch | main |
| Build environment | Managed image |
| Operating system | Amazon Linux |
| Compute | EC2 |
| Provisioning | On-demand |
| Privileged mode | Enabled |
| Buildspec | 04-docker-ecr-cicd/buildspec.yml |
| Artifacts | No artifacts |
| Logs | CloudWatch Logs |

### Why Privileged Mode?

Docker builds require access to Docker daemon capabilities.

Privileged mode was enabled in the CodeBuild environment to allow Docker commands such as:

```bash
docker build
docker tag
docker push
```

## 6. GitHub Webhook Configuration

A webhook was configured to automatically trigger CodeBuild when changes are pushed to the GitHub repository.

Webhook configuration:

| Setting | Value |
|---|---|
| Event type | PUSH |
| Condition | START_BUILD |
| Filter type | HEAD_REF |
| Branch pattern | ^refs/heads/main$ |

This eliminates the need to manually start CodeBuild for every code update.

## 7. Buildspec Configuration

The `buildspec.yml` file defines the automated build process.

### Buildspec.yml

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo "Authenticating with Amazon ECR"
      - ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
      - REGION=$AWS_DEFAULT_REGION
      - REPOSITORY_URI=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/docker-ecr-demo
      - IMAGE_TAG=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - if [ -z "$IMAGE_TAG" ]; then IMAGE_TAG=$CODEBUILD_BUILD_NUMBER; fi
      - aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $REPOSITORY_URI

  build:
    commands:
      - echo "Building Docker image"
      - docker build -f 04-docker-ecr-cicd/Dockerfile -t $REPOSITORY_URI:$IMAGE_TAG 04-docker-ecr-cicd
      - docker tag $REPOSITORY_URI:$IMAGE_TAG $REPOSITORY_URI:latest

  post_build:
    commands:
      - echo "Pushing Docker images to ECR"
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - docker push $REPOSITORY_URI:latest
      - echo "Image successfully pushed to ECR"
```

### Build Phases Explained

**PRE_BUILD**

- Retrieves the AWS account ID.
- Identifies the AWS region.
- Constructs the ECR repository URI.
- Generates a unique image tag using the Git commit ID.
- Authenticates Docker with Amazon ECR.

**BUILD**

- Builds the Docker image.
- Tags the image using the Git commit ID.
- Creates an additional `latest` tag.

**POST_BUILD**

- Pushes the versioned Docker image to ECR.
- Pushes the latest image tag to ECR.

### Image Tagging Strategy

Two image tags are generated:

```text
docker-ecr-demo:latest
docker-ecr-demo:<GIT_COMMIT_ID>
```

The commit-based tag helps identify which source code version produced a particular Docker image.

The `latest` tag points to the most recently pushed image.

## 8. Amazon ECS and AWS Fargate Deployment

The project was extended by deploying the Docker image using Amazon ECS and AWS Fargate.

### ECS Cluster

| Configuration | Value |
|---|---|
| Cluster name | Docker-ECR-Cluster |
| Infrastructure | AWS Fargate |
| Region | ap-south-1 |

### ECS Task Definition

The task definition specifies how the container should run.

| Configuration | Value |
|---|---|
| Task definition family | docker-ecr-task |
| Launch environment | Fargate |
| Operating system | Linux |
| Architecture | X86_64 |
| Network mode | awsvpc |
| Container name | docker-ecr-demo |
| Container image | Amazon ECR image |
| Container port | 5000 |
| Task execution role | ecsTaskExecutionRole |

### ECS Service

| Configuration | Value |
|---|---|
| Service name | docker-ecr-service |
| Cluster | Docker-ECR-Cluster |
| Launch type | Fargate |
| Desired tasks | 1 |
| Deployment strategy | Rolling update |

The ECS service maintains the desired number of running container tasks.

### Networking Configuration

The following networking settings were configured:

- Default VPC.
- Public subnet.
- Public IP assignment.
- Security group for application access.
- Inbound TCP traffic on port 5000.

The application was accessed through the public IP assigned to the Fargate task.

## 9. Deployment and Testing

The application was successfully deployed on AWS Fargate.

### Application URL

```text
http://PUBLIC_IP:5000
```

### Health Check URL

```text
http://PUBLIC_IP:5000/health
```

### Expected Health Check Response

```json
{
  "application": "Docker ECR CI/CD Demo",
  "hostname": "ip-172-31-35-127.ap-south-1.compute.internal",
  "status": "healthy"
}
```

### Verification Results

| Component | Result |
|---|---|
| GitHub webhook | Successful |
| CodeBuild execution | Successful |
| Docker image build | Successful |
| ECR authentication | Successful |
| Docker image push | Successful |
| ECS task definition | Created successfully |
| ECS service | Active |
| Fargate task | Running |
| Flask application | Accessible |
| Health endpoint | Healthy |

## 10. Troubleshooting and Issues Resolved

Several configuration issues were encountered and resolved during implementation.

### Issue 1: Docker Desktop Engine Not Running

**Error:**

```text
The system cannot find the file specified:
dockerDesktopLinuxEngine
```

**Cause:**

Docker CLI could not connect to the Docker Desktop Linux engine.

**Resolution:**

Docker Desktop and its WSL2 backend required troubleshooting.

The AWS CodeBuild environment was used for the cloud-based Docker build, so local Docker Desktop was not required for the remote build process.

### Issue 2: IAM Policy Creation Error

**Cause:**

The IAM policy JSON contained an invalid or incorrectly configured resource ARN.

**Resolution:**

The policy JSON and ECR repository ARN were corrected, including the AWS account ID and region.

### Issue 3: ECS Task Execution Role Error

**Error:**

```text
ECS was unable to assume the role
ecsTaskExecutionRole
```

**Cause:**

The ECS task execution role had an incorrect or missing trust relationship.

**Resolution:**

The trust relationship was configured to allow:

```text
ecs-tasks.amazonaws.com
```

The managed policy `AmazonECSTaskExecutionRolePolicy` was also attached.

### Issue 4: Gunicorn Executable Not Found

**Error:**

```text
exec: "gunicorn": executable file not found in $PATH
```

**Cause:**

Gunicorn was missing from the Docker image.

**Resolution:**

The following dependency was added to `requirements.txt`:

```text
gunicorn==23.0.0
```

The Docker image was rebuilt through CodeBuild and pushed to ECR.

ECS was then updated to run the corrected image.

## 11. Important Learning Outcomes

Through this project, I gained practical experience with:

1. Docker image creation and containerization.
2. Writing and understanding Dockerfiles.
3. Managing Python dependencies inside containers.
4. Using Gunicorn to serve Flask applications.
5. Creating and managing private Amazon ECR repositories.
6. Configuring IAM policies and service roles.
7. Automating Docker builds through AWS CodeBuild.
8. Configuring GitHub webhooks for automatic build triggers.
9. Implementing Docker image tagging strategies.
10. Deploying containers through Amazon ECS.
11. Running containers using AWS Fargate.
12. Configuring task definitions, ECS services, and networking.
13. Troubleshooting IAM, Docker, and container startup failures.
14. Monitoring container logs through CloudWatch.

## 12. Future Improvements

Possible enhancements include:

- Integrate AWS CodePipeline with an ECS deployment stage.
- Automate ECS deployments after every successful ECR image push.
- Use immutable image tags for safer releases.
- Add automated unit tests to the CodeBuild workflow.
- Add Docker image vulnerability scanning.
- Introduce an Application Load Balancer.
- Configure HTTPS using AWS Certificate Manager.
- Implement container health checks.
- Add CloudWatch alarms and monitoring.
- Use least-privilege IAM policies throughout the architecture.

## 13. Cost Management and Cleanup

AWS services used in this project may incur charges.

To avoid unnecessary costs after testing:

- Set the ECS service desired task count to zero or delete the service.
- Delete the ECS cluster if it is no longer required.
- Delete unused ECR images and repositories.
- Remove unnecessary CloudWatch log groups.
- Delete unused IAM roles and policies when no longer needed.
- Review CodeBuild and other AWS resource usage.

**Important:** Stopping or deleting the ECS service does not automatically delete the ECR repository or all associated resources.

## Conclusion

This project provided hands-on experience in building a containerized application and implementing a cloud-based Docker image pipeline using AWS.

By integrating GitHub, AWS CodeBuild, Amazon ECR, Amazon ECS, and AWS Fargate, I developed a practical understanding of containerization, image management, CI automation, IAM permissions, and serverless container deployment.

The project demonstrates how applications can be packaged into Docker images, automatically built in the cloud, stored in a private container registry, and deployed as running services without directly managing EC2 instances.

---

**Project:** Assignment 5 - Containerized CI/CD Pipeline  
**Platform:** Amazon Web Services  
**Region:** ap-south-1 (Mumbai)  
**Repository:** AWS-Projects
