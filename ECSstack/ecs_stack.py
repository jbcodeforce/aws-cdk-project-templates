from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecs as ecs
)
from constructs import Construct
from helpers.BaseStack import BaseStack

class ECSstack(BaseStack): 

    def __init__(self,scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = vpc

        self.ecs_cluster: ecs.Cluster = ecs.Cluster(
            self, "ECSCluster", 
            vpc=self.vpc, 
            cluster_name=self.config.get("ecs_cluster_name")
        )