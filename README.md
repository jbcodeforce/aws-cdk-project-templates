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

**JavaAppstack**: an example of a Quarkus hello world to deploy from ECR

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

```
$ cdk synth
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

The scripts under `app-samples/quarkus-app` should help to get quarkus CLI, get AWS account id and region, generate basic code, build the app, the docker image and push to ECR repo. Here are the steps:

```sh
cd app-samples/quarkus-app
# Get quarkus cli, maven quarkus repository reference, export AWS ACCOUNT_ID and REGION
./setup.sh
./createApp.sh
./build.sh
./aws_push.sh
```





