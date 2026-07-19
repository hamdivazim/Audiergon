import os
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigw,
    aws_logs as logs,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct

class AudiergonCDKStack(Stack):
    """
    CDK Stack for Audiergon Cloud

    Check out Audiergon at https://github.com/hamdivazim/Audiergon :)
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # path fixing (°_o)
        current_dir = os.path.dirname(__path__[0] if hasattr(self, '__path__') else os.path.abspath(__file__))
        lambda_path = os.path.join(current_dir, "..", "..", "lambda")

        # lambda function
        equaliser_lambda = PythonFunction(
            self, "EqualiserHandler",
            entry=lambda_path,
            runtime=_lambda.Runtime.PYTHON_3_11,
            index="handler.py",
            handler="handler",
            timeout=Duration.seconds(29), # 29, limited by API GW 504 timeout
            memory_size=1024, # optimised! check out minimising-lambda-costs.md for a bit of commentary on this :)
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        # API Gateway
        http_api = apigw.HttpApi(
            self, "AudiergonApi",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_methods=[apigw.CorsHttpMethod.POST, apigw.CorsHttpMethod.OPTIONS],
                allow_origins=["*"],
                allow_headers=["Content-Type"]
            )
        )

        # API Gateway --> Lambda (integration)
        lambda_integration = HttpLambdaIntegration("EqualiserIntegration", equaliser_lambda)
        
        http_api.add_routes(
            path="/equalise",
            methods=[apigw.HttpMethod.POST],
            integration=lambda_integration
        )

        cfn_stage = http_api.default_stage.node.default_child
        cfn_stage.default_route_settings = apigw.CfnStage.RouteSettingsProperty(
            throttling_burst_limit=5,
            throttling_rate_limit=2
        )

        CfnOutput(self, "ApiUrl", value=http_api.url or "Deployment failed")