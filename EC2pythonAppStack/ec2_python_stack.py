from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct
from helpers.BaseStack import BaseStack


amzn_linux = ec2.MachineImage.latest_amazon_linux2(
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./EC2pythonAppStack/user_data/user_data.sh") as f:
    user_data = f.read()

class EC2stack(BaseStack): 

    def __init__(self,scope: Construct, construct_id: str, vpc: ec2.Vpc,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ec2_security_group = ec2.SecurityGroup(self, "EC2privateSG",
                                                  vpc=vpc,
                                                  description="SecurityGroup for EC2 in private subnet",
                                                  security_group_name="EC2privateSG",
                                                  allow_all_outbound=True,
                                                  )

        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(80), "allow HTTP access from the internet")

        self.instance = ec2.Instance(self, "FlaskApp",
                                     instance_type=ec2.InstanceType("t2.micro"),
                                     instance_name="FlaskApp",
                                     machine_image=amzn_linux,
                                     vpc=vpc,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                     security_group=self.ec2_security_group,
                                     user_data=ec2.UserData.custom(user_data),
                                     )
        CfnOutput(self,"EC2 URL", value=self.instance.instance_public_ip)

        