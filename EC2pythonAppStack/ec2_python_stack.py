from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from constructs import Construct
from helpers.BaseStack import BaseStack
import requests

amzn_linux = ec2.MachineImage.latest_amazon_linux2(
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./EC2pythonAppStack/user_data/user_data.sh") as f:
    user_data = f.read()

'''
Create a EC2 in first AZ, private subnet with inbound rule on port 22 and 80. This EC2 runs
 a Python Flask app as an example.
It also add a Bastion host to connect to the EC2 via ssh
'''
class EC2stack(BaseStack): 

    def __init__(self,scope: Construct, construct_id: str, vpc: ec2.Vpc,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.createBastionHost(vpc)
        self.createEC2PythonApp(vpc)
        

    
    def createBastionHost(self, vpc):
        r=requests.get("https://checkip.amazonaws.com")
        my_ip = r.text.strip()

        sg = ec2.SecurityGroup(self, "bastion-sg", vpc=vpc, allow_all_outbound=True,)

        role = iam.Role(
            self,
            "BastionRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Role for Bastion host",
        )
        policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        role.add_managed_policy(policy)
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilderECRContainerBuilds"))
        bastion = ec2.Instance(
            self,
            "BastionHost",
            instance_name=self.config.get("bastion_name"),
            key_name=self.config.get("key_name"),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=amzn_linux,
            security_group=sg,
            role=role,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        bastion.connections.allow_from(ec2.Peer.ipv4(f"{my_ip}/32"), ec2.Port.all_traffic())

        CfnOutput(self, "bastion-public-dns-name", value=bastion.instance_public_dns_name)
        CfnOutput(self, "bastion-private-ip", value=bastion.instance_private_ip)

        return sg


    def createEC2PythonApp(self,vpc,bastionIP):
        self.ec2_security_group = ec2.SecurityGroup(self, "EC2privateSG",
                                                  vpc=vpc,
                                                  description="SecurityGroup for EC2 in private subnet",
                                                  security_group_name="EC2privateSG",
                                                  allow_all_outbound=True,
                                                  )
        
        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(80), "allow HTTP access from the public subnet")
        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(bastionIP), ec2.Port.tcp(22), "allow SSH access from the bastion")

        self.instance = ec2.Instance(self, "FlaskApp",
                                     instance_type=ec2.InstanceType("t2.micro"),
                                     instance_name="FlaskApp",
                                     machine_image=amzn_linux,
                                     vpc=vpc,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                     security_group=self.ec2_security_group,
                                     user_data=ec2.UserData.custom(user_data),
                                     )
        CfnOutput(self,"EC2 URL", value=self.instance.instance_public_ip)



        