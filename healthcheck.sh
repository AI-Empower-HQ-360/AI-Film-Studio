#!/bin/bash

# AI Film Studio Hub - Health Check Script
# Checks if all services are running correctly

set -e

echo "🏥 AI Film Studio Hub - Health Check"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in Docker
if command -v docker &> /dev/null && docker-compose ps &> /dev/null; then
    echo "🐳 Checking Docker services..."
    echo ""
    
    # Check Redis
    if docker-compose ps redis | grep -q "Up"; then
        echo -e "${GREEN}✅ Redis is running${NC}"
    else
        echo -e "${RED}❌ Redis is not running${NC}"
    fi
    
    # Check Backend
    if docker-compose ps backend | grep -q "Up"; then
        echo -e "${GREEN}✅ Backend is running${NC}"
        
        # Check backend health
        if curl -f http://localhost:8000/health &> /dev/null; then
            echo -e "${GREEN}✅ Backend is healthy${NC}"
        else
            echo -e "${YELLOW}⚠️  Backend is running but not responding${NC}"
        fi
    else
        echo -e "${RED}❌ Backend is not running${NC}"
    fi
    
    # Check Worker
    if docker-compose ps worker | grep -q "Up"; then
        echo -e "${GREEN}✅ Worker is running${NC}"
    else
        echo -e "${RED}❌ Worker is not running${NC}"
    fi
    
    # Check Frontend
    if docker-compose ps frontend | grep -q "Up"; then
        echo -e "${GREEN}✅ Frontend is running${NC}"
        
        # Check frontend health
        if curl -f http://localhost:3000 &> /dev/null; then
            echo -e "${GREEN}✅ Frontend is healthy${NC}"
        else
            echo -e "${YELLOW}⚠️  Frontend is running but not responding${NC}"
        fi
    else
        echo -e "${RED}❌ Frontend is not running${NC}"
    fi
else
    echo "📝 Checking local services..."
    echo ""
    
    # Check Redis
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✅ Redis is running${NC}"
    else
        echo -e "${RED}❌ Redis is not running${NC}"
    fi
    
    # Check Backend
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo -e "${GREEN}✅ Backend is running and healthy${NC}"
    else
        echo -e "${RED}❌ Backend is not responding${NC}"
    fi
    
    # Check Frontend
    if curl -f http://localhost:3000 &> /dev/null; then
        echo -e "${GREEN}✅ Frontend is running${NC}"
    else
        echo -e "${RED}❌ Frontend is not responding${NC}"
    fi
fi

echo ""
echo "📍 Service URLs:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/api/v1/docs"
echo ""
