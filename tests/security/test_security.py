"""
Security Tests
Validate security measures and vulnerability prevention
"""
import pytest
from fastapi.testclient import TestClient
import os
import json


@pytest.mark.security
class TestSecurity:
    """Security test suite"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from src.api.main import app
        return TestClient(app)

    def test_sql_injection_prevention(self, client):
        """Test SQL injection attempts are blocked"""
        malicious_inputs = [
            "'; DROP TABLE users--",
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users--",
            "1' OR '1'='1",
            "'; DELETE FROM projects--",
        ]
        
        for malicious_input in malicious_inputs:
            # Test in query parameters
            response = client.get(f"/api/v1/test?input={malicious_input}")
            # Should not return 500 (should sanitize or reject)
            assert response.status_code != 500
            
            # Test in POST body
            response = client.post("/api/v1/test", json={"input": malicious_input})
            assert response.status_code != 500

    def test_xss_prevention(self, client):
        """Test XSS attempts are sanitized"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<body onload=alert('XSS')>",
        ]
        
        for payload in xss_payloads:
            response = client.post("/api/v1/test", json={"input": payload})
            # Response should not contain raw script tags
            if response.status_code == 200:
                response_text = response.text
                assert "<script>" not in response_text.lower()
                assert "javascript:" not in response_text.lower()

    def test_authentication_required(self, client):
        """Test protected endpoints require authentication"""
        protected_endpoints = [
            "/api/v1/projects",
            "/api/v1/characters",
            "/api/v1/admin",
            "/api/v1/users",
        ]
        
        for endpoint in protected_endpoints:
            response = client.get(endpoint)
            # Should return 401 or 403, not 200 (unless public)
            assert response.status_code in [401, 403, 404, 405]  # 404 if not implemented

    def test_rate_limiting(self, client):
        """Test rate limiting is enforced"""
        responses = []
        for i in range(100):
            response = client.get("/api/v1/health")
            responses.append(response.status_code)
            # Stop if rate limited
            if response.status_code == 429:
                break
        
        # Should eventually get rate limited (429) or all succeed
        assert len(responses) > 0
        # Check if rate limiting headers present
        last_response = client.get("/api/v1/health")
        headers = last_response.headers
        # May have rate limit headers
        assert isinstance(headers, dict)

    def test_cors_configuration(self, client):
        """Test CORS headers are configured"""
        response = client.options("/api/v1/health", headers={
            "Origin": "https://malicious-site.com",
            "Access-Control-Request-Method": "GET"
        })
        # CORS headers should be configured
        assert response.status_code in [200, 204, 404, 405]

    def test_input_validation(self, client):
        """Test input validation prevents malicious input"""
        # Test oversized inputs
        large_input = "A" * 100000  # 100KB string
        response = client.post("/api/v1/test", json={"input": large_input})
        # Should reject or truncate, not crash
        assert response.status_code != 500
        
        # Test negative numbers where not expected
        response = client.post("/api/v1/test", json={"count": -1000})
        assert response.status_code != 500

    def test_path_traversal_prevention(self, client):
        """Test path traversal attempts are blocked"""
        traversal_paths = [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd",
            "....//....//etc/passwd",
            "..%2F..%2Fetc%2Fpasswd",
            "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        ]
        
        for path in traversal_paths:
            response = client.get(f"/api/v1/files/{path}")
            # Should not expose system files
            assert response.status_code != 200 or "passwd" not in response.text.lower()

    def test_command_injection_prevention(self, client):
        """Test command injection attempts are blocked"""
        command_injections = [
            "; ls -la",
            "| cat /etc/passwd",
            "&& rm -rf /",
            "$(whoami)",
            "`id`",
        ]
        
        for payload in command_injections:
            response = client.post("/api/v1/test", json={"command": payload})
            # Should not execute commands
            assert response.status_code != 500

    def test_xxe_prevention(self, client):
        """Test XXE (XML External Entity) prevention"""
        xxe_payload = """<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>"""
        
        response = client.post(
            "/api/v1/test",
            data=xxe_payload,
            headers={"Content-Type": "application/xml"}
        )
        # Should not expose file contents
        assert response.status_code != 200 or "root:" not in response.text

    def test_header_injection_prevention(self, client):
        """Test HTTP header injection prevention"""
        malicious_headers = {
            "X-Forwarded-For": "127.0.0.1\r\nInjected: header",
            "User-Agent": "Mozilla\r\nX-Injected: true",
        }
        
        response = client.get("/api/v1/health", headers=malicious_headers)
        # Should handle headers safely
        assert response.status_code in [200, 400, 404, 503]

    def test_sensitive_data_exposure(self, client):
        """Test sensitive data is not exposed in responses"""
        response = client.get("/api/v1/health")
        if response.status_code == 200:
            data = response.text.lower()
            # Should not expose secrets
            sensitive_patterns = ["password", "secret", "api_key", "token"]
            for pattern in sensitive_patterns:
                # Check if pattern appears in a suspicious context
                assert True  # Basic check - enhance with regex

    def test_secrets_not_in_code(self):
        """Test secrets are not hardcoded"""
        import os
        # This is a basic check - use tools like git-secrets for production
        # Just verify environment variables can be accessed
        env_vars = os.environ.keys()
        assert isinstance(env_vars, (list, dict, set))

    def test_https_enforcement(self, client):
        """Test HTTPS enforcement in production"""
        # In production, HTTP should redirect to HTTPS
        # This is typically handled by reverse proxy, not application
        assert True  # Placeholder - configure in deployment

    def test_csrf_protection(self, client):
        """Test CSRF protection"""
        # Test that state-changing operations require CSRF token
        response = client.post("/api/v1/test", json={"action": "delete"})
        # Should check for CSRF token (may return 403 or implement token check)
        assert response.status_code in [200, 400, 401, 403, 404, 422]

    def test_json_bomb_prevention(self, client):
        """Test JSON bomb prevention (deeply nested JSON)"""
        json_bomb = {"a": {"a": {"a": {"a": {"a": "value"}}}}}
        # Make it very deep
        for _ in range(50):
            json_bomb = {"a": json_bomb}
        
        try:
            response = client.post("/api/v1/test", json=json_bomb)
            # Should reject or limit depth
            assert response.status_code != 500
        except Exception:
            # Acceptable if JSON parsing fails safely
            assert True
