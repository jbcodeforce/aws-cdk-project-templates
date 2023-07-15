import aws_cdk as core
import aws_cdk.assertions as assertions

from VPCstack.vpc_stack import VPCstack

def test_vpc_created():
    app = core.App()
    stack = VPCstack(app, "avpc")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
