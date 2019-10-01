# AWS Account Nuke Service - Serverless Executor

## Overview
This repository is an example of how to execute [aws-nuke](https://github.com/rebuy-de/aws-nuke) within a serverless environment on AWS leveraging [AWS CodePipeline](https://aws.amazon.com/codepipeline/) and [AWS CodeBuild](https://aws.amazon.com/codebuild/).   
AWS CodePipeline has been selected due to the native integration with Github, as opposed to AWS CodeBuild which requires a manual association with a git repository.   

[aws-nuke](https://github.com/rebuy-de/aws-nuke) prerequisites must be followed and completed before deployment which can be found here: https://github.com/rebuy-de/aws-nuke#caution

![Nuke Service](https://github.com/adamcousins/aws-nuke-service/raw/master/aws_nuke_service.png "Nuke Service")

### Dynamic AWS Account Id to target   
A place holder exists in the aws-nuke config file for AWS CodeBuild to dynamically update with the current running AWS Account Id.   
This allows for multiple deployments across many sandbox accounts without having to manage the AWS account Id.   
`cat aws-nuke-config/config.yaml | grep -A 1 accounts`

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

3. Push this code to a repository you can access with a GitHub personal access token   

#### Note: 
For aws-nuke to access and delete all services the IAM Role assigned to the AWS CodeBuild project `CodeBuildPolicy` is completely permissive. Please review these permissions in your environment to ensure suitable.

### Deployment

1. Create SSM Parameter `/github/token` with github personal access token   
Follow the prompts to enter your CLI profile, region and token. SSM Parameter name can be changed if desired.   
If so, it must also be updated here:   `cat sceptre/config/sandbox/executor.yaml | grep GitToken`   

    `chmod +x ./scripts/create-github-token-ssm.sh && ./scripts/create-github-token-ssm.sh`   

2. Deploy stack with sceptre   
`cd sceptre && sceptre launch sandbox`   

---
### Cloudformation Template
Deployment of this Cloudformation stack can be achieved without sceptre and just using the AWS Console.   
`cat sceptre/templates/aws-nuke-service.yaml`

### aws-nuke Config File 
`cat aws-nuke-config/config.yaml`   
Included in this config file are resources which the above Cloudformation template provisions.
```
presets: #Blocks of Filters to exclude resources
  aws-nuke-service: #Exclude service deploy by this solution
    filters:
      SSMParameter:
      - "/github/token"
      IAMRole:
      - type: contains
        value: "aws-nuke"
      IAMRolePolicyAttachment:
      - type: contains
        value: "aws-nuke"
      IAMRolePolicy:
      - type: contains
        value: "aws-nuke"
      S3Bucket:
      - type: contains
        value: "aws-nuke"
      S3Object:
      - type: contains
        value: "aws-nuke"
      CodePipelinePipeline:
      - type: contains
        value: "aws-nuke"
      CodeBuildProject:
      - type: contains
        value: "aws-nuke"
      SNSTopic:
      - type: contains
        value: "aws-nuke"
      SNSTopicPolicy:
      - type: contains
        value: "aws-nuke"
      CloudWatchLogsLogGroup:
      - type: contains
        value: "aws-nuke"
      CloudWatchEventsRule:
      - type: contains
        value: "aws-nuke"
      CloudWatchEventsTarget:
      - type: contains
        value: "aws-nuke"
      CloudFormationStack:
      - type: contains
        value: "aws-nuke"
      SNSSubscription:
      - type: contains
        value: "aws-nuke"
```

More information about the aws-nuke config file [here](https://github.com/rebuy-de/aws-nuke#usage)


## References

### aws-nuke
[aws-nuke](https://github.com/rebuy-de/aws-nuke) is a project which will nuke a whole AWS account and delete all its resources.   

### sceptre
This example leverages Cloudreach's [sceptre](https://github.com/Sceptre/sceptre) project to deploy the Cloudformation stack for this solution.   