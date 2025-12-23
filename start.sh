#!/bin/bash

# AI Film Studio Hub - Quick Start Script
# This script helps you get started with the AI Film Studio Hub

set -e

echo "🎬 AI Film Studio Hub - Quick Start"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your configuration."
    echo ""
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "✅ Services are starting!"
echo ""
echo "📍 Service URLs:"
echo "   - Frontend:  http://localhost:3000"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/api/v1/docs"
echo "   - Redis:     localhost:6379"
echo ""
echo "📊 Check logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "🎉 Happy filmmaking!"
