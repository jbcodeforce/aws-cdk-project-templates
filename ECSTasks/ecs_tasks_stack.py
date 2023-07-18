from aws_cdk import (
    # Duration,
    CfnOutput,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_logs,
    aws_elasticloadbalancingv2 as elbv2
)

from constructs import Construct
from helpers.BaseStack import BaseStack

# Define a task and service  for a given app/microservice
class ECSJavaTask(BaseStack):
    def __init__(self,scope: Construct, construct_id: str, cluster: ecs.Cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role: iam.Role = iam.Role(
            self,
            "task-def-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Allows ECS tasks to call AWS services.",
        )
        # Access to back end service like RDS or DynamoDB
      
        task_def = ecs.FargateTaskDefinition(
            self,
            "Java-task-def",
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64,
            ),
            task_role=role,
            cpu=256,
            memory_limit_mib=1024,
        )


        appContainer = ecs.ContainerImage.from_ecr_repository(
            repository=ecr.Repository.from_repository_name(
                self,
                "quakurs-app-repo",
                repository_name="demo-customer-api",
            )
        )

        javaApp=task_def.add_container("app",
                                       image=appContainer,
                                        logging=ecs.LogDriver.aws_logs(
                                            stream_prefix="nginx",
                                            log_retention=aws_logs.RetentionDays.ONE_MONTH,
                                        ),
                                        essential=True,)
        javaApp.add_port_mappings(ecs.PortMapping(container_port=8080))

        exposedSvc = ecs.FargateService(self,"javaAppService",cluster=cluster, task_definition=task_def)

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=cluster.vpc, internet_facing=True)
        listener = lb.add_listener("Listener", port=8080)
        ecsTarget=ecs.EcsTarget(container_name="app",
                container_port=8080,
                new_target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(listener,
                    protocol=elbv2.ApplicationProtocol.HTTPS
                ))
        exposedSvc.register_load_balancer_targets(ecsTarget)