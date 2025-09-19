#!/bin/bash

echo "Starting House Server Infrastructure..."

# Start infrastructure services
echo "Starting infrastructure services (MySQL, Redis, Elasticsearch, RabbitMQ)..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Start microservices
echo "Starting microservices..."

# Start Eureka Server
echo "Starting Eureka Server..."
cd eureka-server
mvn spring-boot:run &
EUREKA_PID=$!
cd ..

# Wait for Eureka to start
sleep 20

# Start Gateway Service
echo "Starting Gateway Service..."
cd gateway-service
mvn spring-boot:run &
GATEWAY_PID=$!
cd ..

# Start User Service
echo "Starting User Service..."
cd user-service
mvn spring-boot:run &
USER_PID=$!
cd ..

# Start House Service
echo "Starting House Service..."
cd house-service
mvn spring-boot:run &
HOUSE_PID=$!
cd ..

# Start Admin Service
echo "Starting Admin Service..."
cd admin-service
mvn spring-boot:run &
ADMIN_PID=$!
cd ..

# Start Data Collection Service
echo "Starting Data Collection Service..."
cd data-collection-service
mvn spring-boot:run &
DATA_COLLECTION_PID=$!
cd ..

echo "All services started!"
echo "Eureka Server PID: $EUREKA_PID"
echo "Gateway Service PID: $GATEWAY_PID"
echo "User Service PID: $USER_PID"
echo "House Service PID: $HOUSE_PID"
echo "Admin Service PID: $ADMIN_PID"
echo "Data Collection Service PID: $DATA_COLLECTION_PID"

echo ""
echo "Services are running on:"
echo "- Gateway: http://localhost:8080"
echo "- Eureka Dashboard: http://localhost:8761"
echo "- User Service: http://localhost:8081"
echo "- House Service: http://localhost:8082"
echo "- Data Collection Service: http://localhost:8083"
echo "- Admin Service: http://localhost:8084"
echo ""
echo "To stop all services, run: ./stop.sh"

# Save PIDs to file for stop script
echo "$EUREKA_PID $GATEWAY_PID $USER_PID $HOUSE_PID $ADMIN_PID $DATA_COLLECTION_PID" > .pids
