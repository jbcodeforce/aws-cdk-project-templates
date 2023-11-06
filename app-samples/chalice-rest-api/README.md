# A REST API demo for car ride order resource

A Car Ride is for autonomous car, within one of the supported cities.


## Pre-requisites

* Install AWS chalice CLI: `python3 -m pip install chalice`
* The project was created with: `chalice new-project`, then select cdk with dynamoDB project type.
* Use CDK to deploy the application: Under `infrastructure` use: `cdk deploy`

    This project template combines a CDK application and a Chalice application. These correspond to the ``infrastructure`` and ``runtime`` directory respectively.  To run any CDK CLI commands, ensure you're in the ``infrastructure`` directory, and to run any Chalice CLI commands ensure you're in the ``runtime`` directory.

* Under `runtime` deploy the app: `chalice deploy`

    * It zips the application and deploys it as lambda function.
    * It Create IAM role: so lambda can do stsAssumeRole and a policy to create logs
    * Declares a API and API Gateway resource, with a generated domain name
    * .chalice/config.json file contains app parameters.