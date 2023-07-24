# CDK project template to define a set of reusable CloudFormation stacks

## What it builds

**VPCStack:**

* VPC on 2 AZs with 2 public and 2 private subnets, one internet gateway, a default security group
* In each public subnet: one Elastic IP, a route table ,  a NAT gateway, a default route for outbound traffic
* In each private subnet: one route table, with route for outbound traffic to NAT gateway, 
* A lambda function to remove all inbound/outbound rules from the VPC default security group
* A EC2 Bastion host for SSH to private hosts, and get connection from your working laptop.

**ECSstack**:

* Create the ECS Cluster within the VPC

**ECStasks**: a Task definition for a Quarkus hello world to deploy from ECR. 

**RDSStack**: to declare a RDS postgresql inside the VPC private subnet.

## CDK Setup

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```sh
# Be sure to use the good configuration (e.g folder config/acr.yaml)
export APP_NAME=acr
# select one of the available stacks: cdk dep
cdk synth acr-vpc 
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Java Quarkus app sample

The scripts under `app-samples/quarkus-app` should help to get quarkus CLI, get AWS account id and region, generate basic code, build the app, the docker image and push to ECR repo. 

On EC2 machine, we need Java JDK 17, Maven 3.6

```sh
sudo yum update
sudo yum install git
wget --no-check-certificate -c --header "Cookie: oraclelicense=accept-securebackup-cookie" https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.rpm
sudo rpm -Uvh jdk-17_linux-x64_bin.rpm
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/7/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
sudo yum install docker
sudo usermod -a -G docker ec2-user
newgrp docker
sudo systemctl start docker.service
```

Here are the steps:

```sh
cd app-samples/quarkus-app
# Build with mvnw
./mvnw package
# Build the image
docker build -f ../Dockerfile -t 403993201276.dkr.ecr.us-west-2.amazonaws.com/demo-customer-api:latest .


```





