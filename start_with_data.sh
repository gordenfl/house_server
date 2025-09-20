#!/bin/bash

echo "🏠 House Server with Irvine Data - Complete Setup"
echo "=================================================="

# 检查Docker状态
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Starting infrastructure services..."
docker-compose up -d mysql redis elasticsearch rabbitmq

echo "⏳ Waiting for services to start..."
sleep 30

echo "📊 Setting up database..."
./setup-database.sh

echo "🔄 Migrating Irvine data to MySQL..."
cd zillow-scraper
source venv/bin/activate
python3 migrate_to_mysql.py
cd ..

echo "🚀 Starting microservices..."
echo "Starting Eureka Server..."
cd eureka-server
mvn spring-boot:run &
EUREKA_PID=$!
cd ..

sleep 20

echo "Starting Gateway Service..."
cd gateway-service
mvn spring-boot:run &
GATEWAY_PID=$!
cd ..

echo "Starting User Service..."
cd user-service
mvn spring-boot:run &
USER_PID=$!
cd ..

echo "Starting House Service..."
cd house-service
mvn spring-boot:run &
HOUSE_PID=$!
cd ..

echo "Starting Admin Service..."
cd admin-service
mvn spring-boot:run &
ADMIN_PID=$!
cd ..

echo "Starting Data Collection Service..."
cd data-collection-service
mvn spring-boot:run &
DATA_COLLECTION_PID=$!
cd ..

echo "✅ All services started!"
echo ""
echo "📊 Services running on:"
echo "   - Gateway: http://localhost:8080"
echo "   - Eureka Dashboard: http://localhost:8761"
echo "   - User Service: http://localhost:8081"
echo "   - House Service: http://localhost:8082"
echo "   - Data Collection Service: http://localhost:8083"
echo "   - Admin Service: http://localhost:8084"
echo ""
echo "🏠 Irvine CA House Data:"
echo "   - 10 houses loaded in database"
echo "   - Price range: \$750,000 - \$1,650,000"
echo "   - Average price: \$1,130,000"
echo "   - House types: House, Condo, Townhouse"
echo ""
echo "🔍 Test the API:"
echo "   curl http://localhost:8080/api/houses"
echo "   curl http://localhost:8080/api/houses/search/location"
echo ""
echo "To stop all services, run: ./stop.sh"

# 保存PIDs
echo "$EUREKA_PID $GATEWAY_PID $USER_PID $HOUSE_PID $ADMIN_PID $DATA_COLLECTION_PID" > .pids
