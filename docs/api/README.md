# API Documentation - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Base URL:** `https://api.ai-film-studio.com/v1`

---

## 📚 API Overview

This directory contains comprehensive API documentation for all microservices in the AI Film Studio platform.

### **Available API Documentation**

- [User Service API](./user-service-api.md) - Authentication, user management, profiles
- [Project Service API](./project-service-api.md) - Project CRUD operations, assets
- [Credit Service API](./credit-service-api.md) - Credits, subscriptions, payments
- [AI Job Service API](./ai-job-service-api.md) - Video generation jobs, status tracking
- [YouTube Service API](./youtube-service-api.md) - YouTube integration, uploads, playlists
- [Admin Service API](./admin-service-api.md) - Administrative functions (admin only)

---

## 🔐 Authentication

All API requests (except public endpoints) require authentication using JWT tokens.

### **Obtaining a Token**

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 86400,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "creator"
  }
}
```

### **Using the Token**

Include the access token in the `Authorization` header:

```http
GET /api/v1/projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Refreshing the Token**

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 📊 Response Format

### **Success Response**

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully"
}
```

### **Error Response**

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": {}
  }
}
```

---

## 🚦 HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success - Request completed successfully |
| `201` | Created - Resource created successfully |
| `202` | Accepted - Request accepted for processing |
| `204` | No Content - Success with no response body |
| `400` | Bad Request - Invalid request parameters |
| `401` | Unauthorized - Authentication required |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found - Resource not found |
| `422` | Unprocessable Entity - Validation errors |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error - Server error occurred |
| `503` | Service Unavailable - Service temporarily down |

---

## 🔢 Error Codes

| Code | Description |
|------|-------------|
| `AUTH_REQUIRED` | Authentication is required |
| `INVALID_TOKEN` | JWT token is invalid or expired |
| `INVALID_CREDENTIALS` | Email or password is incorrect |
| `USER_NOT_FOUND` | User account does not exist |
| `USER_ALREADY_EXISTS` | Email is already registered |
| `INSUFFICIENT_CREDITS` | Not enough credits for operation |
| `PROJECT_NOT_FOUND` | Project does not exist |
| `JOB_NOT_FOUND` | Job does not exist |
| `INVALID_PARAMETERS` | Request parameters are invalid |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `INTERNAL_ERROR` | Internal server error |

---

## 📝 Pagination

List endpoints support pagination using query parameters:

```http
GET /api/v1/projects?page=2&perPage=20
```

**Parameters:**
- `page` (integer, default: 1) - Page number
- `perPage` (integer, default: 20, max: 100) - Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 2,
      "perPage": 20,
      "totalItems": 150,
      "totalPages": 8,
      "hasNextPage": true,
      "hasPreviousPage": true
    }
  }
}
```

---

## 🔍 Filtering & Sorting

### **Filtering**

```http
GET /api/v1/projects?status=completed&userId=550e8400-e29b-41d4-a716-446655440000
```

### **Sorting**

```http
GET /api/v1/projects?sortBy=createdAt&sortOrder=desc
```

**Common sort fields:**
- `createdAt` - Creation date
- `updatedAt` - Last update date
- `title` - Project title (alphabetical)

**Sort orders:**
- `asc` - Ascending
- `desc` - Descending (default)

---

## 🚀 Rate Limiting

API requests are rate-limited to ensure fair usage:

### **Rate Limits by Plan**

| Plan | Rate Limit |
|------|------------|
| Free (Creator) | 60 requests/minute |
| Standard | 120 requests/minute |
| Pro | 300 requests/minute |
| Enterprise | 1000 requests/minute |

### **Rate Limit Headers**

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1672531200
```

### **Rate Limit Exceeded Response**

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in 30 seconds.",
    "retryAfter": 30
  }
}
```

---

## 🌐 Webhooks (Coming Soon)

Receive real-time notifications for events:

### **Available Events**
- `job.completed` - Video generation completed
- `job.failed` - Video generation failed
- `credit.low` - Credits running low
- `subscription.renewed` - Subscription renewed
- `subscription.cancelled` - Subscription cancelled

### **Webhook Payload Example**

```json
{
  "event": "job.completed",
  "timestamp": "2025-12-31T12:00:00Z",
  "data": {
    "jobId": "550e8400-e29b-41d4-a716-446655440000",
    "projectId": "660e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "videoUrl": "https://s3.amazonaws.com/..."
  }
}
```

---

## 🧪 Testing

### **Sandbox Environment**

Test API endpoints without affecting production data:

**Base URL:** `https://sandbox-api.ai-film-studio.com/v1`

### **Test Credentials**

```
Email: test@ai-film-studio.com
Password: TestPassword123
```

### **Postman Collection**

Download our Postman collection for easy API testing:
[Download Collection](https://api.ai-film-studio.com/postman/collection.json)

---

## 📖 OpenAPI / Swagger

Interactive API documentation:

**Swagger UI:** `https://api.ai-film-studio.com/docs`  
**OpenAPI Spec:** `https://api.ai-film-studio.com/openapi.json`

---

## 💬 Support

- **Documentation:** [https://docs.ai-film-studio.com](https://docs.ai-film-studio.com)
- **Email:** api-support@ai-film-studio.com
- **Discord:** [Join our community](https://discord.gg/ai-film-studio)

---

## 📜 Changelog

### **v1.0.0** (2025-12-31)
- Initial API release
- User authentication
- Project management
- Video generation
- Credit system
- YouTube integration

---

**🎬 Happy Building!**
