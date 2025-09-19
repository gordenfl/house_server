#!/bin/bash

echo "Testing House Server API..."

# 等待服务启动
echo "Waiting for services to start..."
sleep 30

BASE_URL="http://localhost:8080"

echo ""
echo "=== Testing User Registration ==="
curl -X POST $BASE_URL/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "passwordHash": "password123",
    "firstName": "Test",
    "lastName": "User"
  }' \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "=== Testing House Search ==="
curl -X POST $BASE_URL/api/houses/search/location \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "radiusKm": 5.0
  }' \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "=== Testing House List ==="
curl -X GET $BASE_URL/api/houses \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "=== Testing Data Collection Status ==="
curl -X GET $BASE_URL/api/data-collection/status \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "=== Testing Eureka Dashboard ==="
curl -X GET http://localhost:8761 \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "API testing completed!"
