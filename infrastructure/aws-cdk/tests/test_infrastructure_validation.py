"""
Infrastructure validation tests
Tests stack synthesis and validation
"""
import pytest
import json
from pathlib import Path
from aws_cdk import App
from stacks.ai_film_studio_stack import AIFilmStudioStack


class TestStackSynthesis:
    """Test that stack synthesizes correctly"""
    
    def test_stack_synthesizes(self):
        """Test that stack can be synthesized"""
        app = App()
        stack = AIFilmStudioStack(
            app,
            "TestStack",
            env={
                "account": "123456789012",
                "region": "us-east-1"
            }
        )
        
        # Should not raise exception
        app.synth()
        assert True
    
    def test_stack_has_all_components(self):
        """Test that stack has all required components"""
        app = App()
        stack = AIFilmStudioStack(
            app,
            "TestStack",
            env={
                "account": "123456789012",
                "region": "us-east-1"
            }
        )
        
        # Synthesize to get template
        assembly = app.synth()
        template = assembly.get_stack_by_name("TestStack").template
        
        # Check for key resources
        resources = template.get("Resources", {})
        
        # VPC
        assert any("VPC" in key for key in resources.keys())
        
        # ECS
        assert any("Cluster" in key for key in resources.keys())
        assert any("Service" in key for key in resources.keys())
        
        # RDS
        assert any("Database" in key for key in resources.keys())
        
        # S3
        assert any("Bucket" in key for key in resources.keys())
        
        # SQS
        assert any("Queue" in key for key in resources.keys())
        
        # CloudFront
        assert any("Distribution" in key for key in resources.keys())


class TestStackValidation:
    """Test stack validation"""
    
    def test_no_circular_dependencies(self):
        """Test that stack has no circular dependencies"""
        app = App()
        stack = AIFilmStudioStack(
            app,
            "TestStack",
            env={
                "account": "123456789012",
                "region": "us-east-1"
            }
        )
        
        # Synthesize - should not raise circular dependency error
        try:
            app.synth()
            assert True
        except Exception as e:
            if "circular" in str(e).lower():
                pytest.fail(f"Circular dependency detected: {e}")
            raise


class TestEnvironmentConfiguration:
    """Test environment-specific configuration"""
    
    @pytest.mark.parametrize("environment", ["dev", "staging", "production"])
    def test_environment_configuration(self, environment):
        """Test that stack works for all environments"""
        app = App()
        app.node.set_context("environment", environment)
        
        stack = AIFilmStudioStack(
            app,
            f"TestStack-{environment}",
            env={
                "account": "123456789012",
                "region": "us-east-1"
            }
        )
        
        # Should synthesize without errors
        app.synth()
        assert True
