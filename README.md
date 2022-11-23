# python script to create ECR repo and push docker image on the same repo:
 This repo conatains a python script that will simply create a ECR repo on your aws account 
 after that it will build a docker image with Dockerfile provided path and tag that image according to ECR and push that image to same ECR repo.
# AWS ECR:
  Amazon ECR is a fully managed container registry offering high-performance hosting, so you can reliably deploy application images and artifacts anywhere.
# Pre-requisites:
  - AWS Account.
  - Configure aws access_key and secret_key.
  - Python3 installed.

# How to Run?:
  * Before running the python script install python module using pip  
    - boto3
    - docker
  * Provide `registryId='<aws_account_id>'` and `repositoryName='<repo_name>'` in line nubmer `8`  and `9` respectively in create-ecr-repo.py file also in line number `38` as well
  * You can check install python module using this command   
                ` pip list `  
            ` python3 create-ecr-repo.py `