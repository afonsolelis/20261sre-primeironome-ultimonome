# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Deploy the CloudFormation stack (requires `.env` copied from `.env.example` and populated):

```bash
bash scripts/deploy.sh
```

Inspect stack state:

```bash
aws cloudformation describe-stacks --stack-name "${AWS_STACK_NAME}"
```

Run the local S3 reader (requires `PIPELINE_BUCKET` env var and AWS credentials):

```bash
PIPELINE_BUCKET=<bucket> python3 app/read_s3.py
```

There is no test suite, linter, or build step configured.

## Architecture

Single CloudFormation stack (`cloudformation/template.yaml`) provisions an entire two-workload environment in one shot:

- **Networking**: one VPC with two public subnets across `us-east-1a`/`us-east-1b` (two AZs are required by the ALB), IGW, public route table shared by both subnets.
- **Two EC2 workloads, both bootstrapped via `UserData`** (the Python files in `app/` are reference copies — the actual code that runs on the instances is inlined as heredocs inside the template's `UserData`):
  - `PipelineInstance` — runs `read_s3.py` once at boot, logging to `/var/log/read_s3.log`. Sits in its own SG with SSH open and no inbound app port.
  - `StreamlitInstance` — runs `streamlit_app.py` on port 8501. Its SG only accepts 8501 from the ALB SG (not the public internet); SSH is open.
- **Public entry point**: `StreamlitLoadBalancer` (ALB) listens on :80 and forwards to the Streamlit instance on :8501. This is the only public HTTP path — reaching Streamlit directly on the instance is blocked by the SG layering.
- **IAM**: uses a pre-existing instance profile named via the `InstanceProfileName` parameter (default `LabInstanceProfile`). The stack does **not** create the role — it must already exist in the AWS account (this is an AWS Academy / "LabRole" pattern).
- **S3**: a single bucket with AES256 SSE; both instances inherit access through the instance profile role.

### Deploy flow

`scripts/deploy.sh` sources `.env` with `set -a`, then calls `aws cloudformation deploy` with `CAPABILITY_NAMED_IAM` and passes `InstanceProfileName` as a parameter override. Credentials flow via the standard AWS SDK env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) set in `.env` — there is deliberately no `~/.aws/credentials` or `AWS_PROFILE` step, because the target audience is AWS Academy Learner Lab users whose temporary credentials rotate every ~4h. Reproducibility in Codespaces relies on this: the only setup is `cp .env.example .env` + paste.

### Editing UserData

When changing instance bootstrap behavior, edit the heredoc blocks inside `template.yaml` `UserData` — not the files in `app/`. The `app/` files are not deployed by CloudFormation; they exist for local development and as readable references. Keeping them in sync with the heredocs is manual.
