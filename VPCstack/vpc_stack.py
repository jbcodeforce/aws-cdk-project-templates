from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct
from helpers.BaseStack import BaseStack
import requests

CIDR="10.0.0.0/16"

class VPCstack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc= self.lookup_vpc(self.config.get("vpc_name"))
        if self.vpc is None:
            self.vpc = self.create_vpc(construct_id)
        CfnOutput(self,"VPC", value=self.vpc.vpc_id, export_name="vpc")

        
    def create_vpc(self, vpc_name: str) -> ec2.Vpc:

        vpc = ec2.Vpc(self, vpc_name,
            cidr=self.config.get("vpc_cidr"),
            max_azs=2,
            vpc_name=vpc_name,
            nat_gateways=2,
            ip_addresses=ec2.IpAddresses.cidr(CIDR),
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=self.config.get("cidr_mask")
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=self.config.get("cidr_mask")
                )
            ]
        )

        return vpc
    
       