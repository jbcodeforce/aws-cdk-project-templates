#!/bin/bash
yum update -y
yum install python3 python3-pip wget
cd /home/ec2-user
wget https://raw.githubusercontent.com/jbcodeforce/aws-cdk-project-templates/main/app-samples/flask-app/app.py
wget https://raw.githubusercontent.com/jbcodeforce/aws-cdk-project-templates/main/app-samples/flask-app/requirements.txt
pip3 install -r requirements.txt
python3 app.py
