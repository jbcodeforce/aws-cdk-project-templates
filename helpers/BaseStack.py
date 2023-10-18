
from aws_cdk import  Stack, aws_ec2 as ec2

from constructs import Construct
from .helpers import getAppEnv
import boto3

class BaseStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        # Order is important to avoid unexpected keyword argument 'config' exception.
        self.config = kwargs.pop("config", {})
        self.app_env = getAppEnv()
        super().__init__(scope, id, **kwargs)                  

    def lookup_vpc(self, vpc_name: str) -> ec2.Vpc:
        client = boto3.client('ec2')
        response = client.describe_vpcs(
                        Filters=[{
                            'Name': 'tag:Name',
                            'Values': [
                                vpc_name
                            ]
                        }]
                    )
        if len(response['Vpcs']) > 0:
            vpc=response['Vpcs'][0]
        else:
            vpc= None
        return vpc
    