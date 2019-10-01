#!/bin/bash

read -e -p 'Type the name of the profile to source, followed by [ENTER]: ' -i "default" PROFILE
read -e -p 'Type the name of the aws region to use, followed by [ENTER]: ' -i "ap-southeast-2" REGION
read -e -p 'SSM Parameter Name to Create: ' -i "/github/token" name
read -sp 'GitHub Personal Access Token: ' token

export AWS_DEFAULT_REGION=$REGION
export AWS_PROFILE=$PROFILE

#create secure string ssm parameter
aws ssm put-parameter \
   --name $name \
   --value $token \
   --type SecureString \
   --overwrite

echo "Done"