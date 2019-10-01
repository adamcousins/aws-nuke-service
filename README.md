# AWS Account Nuke Service - Serverless Executor

## Overview
This repository is an example of how to execute [aws-nuke](https://github.com/rebuy-de/aws-nuke) within a serverless environment on AWS leveraging [AWS CodePipeline](https://aws.amazon.com/codepipeline/) and [AWS CodeBuild](https://aws.amazon.com/codebuild/).   
AWS CodePipeline has been selected due to the native integration with Github, as opposed to AWS CodeBuild which requires a manual association with a git repository.   

[aws-nuke](https://github.com/rebuy-de/aws-nuke) prerequisites must be followed and completed before deployment which can be found here: https://github.com/rebuy-de/aws-nuke#caution

![Nuke Service](https://github.com/adamcousins/aws-nuke-service/raw/master/aws_nuke_service.png "Nuke Service")

### Installation

0. Fork this repository
https://help.github.com/en/articles/fork-a-repo

1. Install sceptre with pip   
`pip install sceptre`   
https://sceptre.cloudreach.com/latest/docs/install.html

2. Install sceptre custom resolver for ssm   
`cd custom_resolvers/sceptre-ssm-resolver && pip install .`   
https://sceptre.cloudreach.com/latest/docs/resolvers.html#custom-resolvers

3. Check Installation Successful
`sceptre --version`

### Configuration
1. Update GitHub Details for the source repository where the aws-nuke config file exists   
`cat sceptre/config/sandbox/executor.yaml | grep Git`

2. Update Email address for CodePipeline notifications   
`cat sceptre/config/sandbox/executor.yaml | grep NotificationEmailAddress`

#### Note: 
For aws-nuke to access all services and to perform deletions on all services the IAM Role assigned to the AWS CodeBuild project `CodeBuildPolicy` is completely permissive. Please review these permissions in your environment to ensure suitable.

### Deployment

1. Create SSM Parameter `/github/token` with github personal access token   
Follow the prompts to enter your CLI profile, region and token. SSM Parameter name can be changed if desired.   
If so, it must also be updated here:   `cat sceptre/config/sandbox/executor.yaml | grep GitToken`   

    `chmod +x ./scripts/create-github-token-ssm.sh && ./scripts/create-github-token-ssm.sh`   

2. Deploy stack with sceptre   
`cd sceptre && sceptre launch sandbox`   


## References

### aws-nuke
[aws-nuke](https://github.com/rebuy-de/aws-nuke) is a project which will nuke a whole AWS account and delete all its resources.   

### sceptre
This example leverages Cloudreach's [sceptre](https://github.com/Sceptre/sceptre) project to deploy the Cloudformation stack for this solution.   