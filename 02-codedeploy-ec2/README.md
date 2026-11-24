
# AWS CodeDeploy - EC2 Application Deployment

## Overview
Automated deployment of a static website to an Ubuntu EC2 instance using AWS CodePipeline and AWS CodeDeploy.

## Architecture
GitHub -> AWS CodePipeline -> AWS CodeDeploy -> EC2 -> Nginx

## Technologies
- AWS EC2
- AWS CodeDeploy
- AWS CodePipeline
- AWS IAM
- Ubuntu 22.04
- Nginx
- Bash

## Deployment Strategy
In-Place Deployment

## Lifecycle Hooks
1. BeforeInstall: Installs Nginx and prepares the web directory.
2. ApplicationStart: Enables and restarts Nginx.
3. ValidateService: Checks Nginx and verifies HTTP response.

## Application
Static HTML website hosted using Nginx.

## Deployment Testing
Modify the website version, push changes to GitHub, and monitor automatic deployment through CodePipeline.

## Status
Implementation in progress.
