# AWS CodeBuild Python CI Demo

A Flask application with an automated continuous integration pipeline using AWS CodeBuild. A push to the configured GitHub source repository triggers a build, installs Python dependencies, runs the pytest suite, and publishes a ZIP artifact to Amazon S3 when the build succeeds.

## Architecture

```text
Git push
   |
   v
GitHub webhook
   |
   v
AWS CodeBuild
   |---- Install Python dependencies
   |---- Run pytest
   |---- Send build logs to CloudWatch Logs
   |
   +---- On success: upload ZIP artifact to Amazon S3
```

## Technology stack

| Area | Technology |
|---|---|
| Application | Python, Flask |
| Testing | pytest |
| Source control | GitHub |
| CI / build | AWS CodeBuild |
| Artifact storage | Amazon S3 |
| Build logs | Amazon CloudWatch Logs |
| Permissions | IAM service role |

## Project structure

```text
01-codebuild-python-demo/
├── app.py
├── test_app.py
├── requirements.txt
├── buildspec.yml
└── README.md
```

## Run locally

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install and test:

```bash
pip install -r requirements.txt
python -m pytest -v
```

Run the Flask app:

```bash
python app.py
```

Open http://localhost:5000.

## CodeBuild configuration

The `buildspec.yml` file defines the build phases:

1. **install:** Selects Python 3.12 and installs dependencies.
2. **pre_build:** Prints a test-start message.
3. **build:** Runs `pytest -v`. A failing test causes a non-zero exit code and fails the build.
4. **post_build:** Prints a completion message.
5. **artifacts:** Packages the application and build files for S3 artifact storage.

## AWS setup overview

1. Create an S3 bucket for build artifacts.
2. Create an IAM service role for CodeBuild with the required CloudWatch Logs and S3 permissions.
3. Create a CodeBuild project connected to the source repository.
4. Configure the project to use the repository's `buildspec.yml`.
5. Enable webhook-triggered builds for pushes to the `main` branch.
6. Inspect build results in CodeBuild and logs in CloudWatch Logs.

## Verification

The original project repository's README records successful baseline and webhook-triggered builds, as well as an intentional failing-test run used to verify that test failures fail the build.

## Note about this portfolio copy

This folder is a portfolio copy of the project. The original repository remains available at [codebuild-python-demo](https://github.com/DHRUVRAJPUTTT/codebuild-python-demo). The CodeBuild webhook and project configuration may still point to that original repository; this portfolio copy does not automatically change the AWS source connection.

## Author

Dhruv Rajput · [GitHub](https://github.com/DHRUVRAJPUTTT)
