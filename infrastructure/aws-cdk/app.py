#!/usr/bin/env python3
"""
AWS CDK App Entry Point
AI Film Studio - Enterprise Studio Operating System Infrastructure
"""
import aws_cdk as cdk
from stacks.ai_film_studio_stack import AIFilmStudioStack

app = cdk.App()

# Environment configuration
env = cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region") or "us-east-1"
)

# Main stack
AIFilmStudioStack(
    app,
    "AIFilmStudio",
    env=env,
    description="AI Film Studio - Enterprise Studio Operating System Infrastructure"
)

app.synth()
