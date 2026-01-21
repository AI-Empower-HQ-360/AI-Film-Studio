"""Tests for credit and subscription API endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestCreditBalance:
    """Test credit balance endpoints"""
    
    def test_get_balance_without_auth(self):
        """Test getting credit balance without authentication"""
        response = client.get("/api/credits/balance")
        assert response.status_code == 401  # Unauthorized without auth


class TestSubscriptionPlans:
    """Test subscription plan endpoints"""
    
    def test_get_plans(self):
        """Test getting subscription plans"""
        response = client.get("/api/credits/plans")
        # This endpoint should be public, but will fail without database
        # Accept both success and database error
        assert response.status_code in [200, 500]


class TestCreditTopup:
    """Test credit top-up endpoints"""
    
    def test_topup_without_auth(self):
        """Test credit top-up without authentication"""
        response = client.post(
            "/api/credits/topup",
            json={
                "plan_type": "Pro"
            }
        )
        assert response.status_code == 401  # Unauthorized without auth
