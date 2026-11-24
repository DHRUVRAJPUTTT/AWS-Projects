# AWS Elastic Beanstalk CI/CD Deployment

## Objective
Deploy a Python Flask application using AWS CodePipeline
and AWS Elastic Beanstalk.

## Architecture
GitHub -> CodePipeline -> CodeBuild -> Elastic Beanstalk

## Features
- Managed Python application environment
- Automated deployments from GitHub
- Immutable deployment strategy
- Environment variable configuration
- Health endpoint
- Staging and production configuration simulation

## Environment Variables
- APP_ENV
- APP_VERSION
- APP_MESSAGE

## Deployment
Push changes to the main branch to trigger the pipeline.