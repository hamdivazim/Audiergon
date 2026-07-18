#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import AudiergonCDKStack


app = cdk.App()
AudiergonCDKStack(app, "AudiergonCDKStack")

app.synth()
