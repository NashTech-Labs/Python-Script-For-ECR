import base64
import boto3
import docker
ecr_client = boto3.client('ecr','ap-south-1')

#CREATE REPO
response = ecr_client.create_repository(
    registryId='<resgitry_id>',
    repositoryName='<repo_name>',
    tags=[
        {
            'Key': 'docker',
            'Value': 'image'
        },
    ],
    imageTagMutability='MUTABLE',
    imageScanningConfiguration={
        'scanOnPush': True
    }
)

#SAVING REPO URL INTO `repo` VARIABLE
url= response.get('repository')
repo=url['repositoryUri']
profile = "default"
region = "ap-south-1"
local_tag = "myproj"

#DEFINE DOCKER CLIENT FOR BUILDING DOCKER IMAGE AND TAG
docker_client = docker.APIClient()

#BUILD DOCKER IMAGE WITH DOCKERFILE
print("Building image " + local_tag)
for line in docker_client.build(path='.', tag=local_tag, dockerfile='./Dockerfile'):
    print(line)

#GET AWS ECR REGISTRY TOKEN FOR AUTHENTICATION
token = ecr_client.get_authorization_token(registryIds=['<AWS_ACCOUNT_ID>'])
#THE TOKEN IS BASE64 ENCODED SO WE NEED TO DECODE IT 
#ALSO USERNAME AND PASSWORD ARE SEPARTED BY ':' WE NEED TO SPLIT IT
username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
endpoint = token["authorizationData"][0]["proxyEndpoint"]

auth_config_payload = {'username': username, 'password': password}

version_tag = repo + ':latest'
latest_tag = repo + ':' + '1.0'

print("Tagging version " + version_tag)
if docker_client.tag(local_tag, version_tag) is False:
    raise RuntimeError("Tag appeared to fail: " + version_tag)


print("Pushing to repo " + version_tag)
for line in docker_client.push(version_tag, stream=True, auth_config=auth_config_payload):
    print(line)
