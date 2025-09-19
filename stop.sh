#!/bin/bash

echo "Stopping House Server Services..."

# Stop microservices
if [ -f .pids ]; then
    echo "Stopping microservices..."
    for pid in $(cat .pids); do
        if kill -0 $pid 2>/dev/null; then
            echo "Stopping process $pid"
            kill $pid
        fi
    done
    rm .pids
fi

# Stop infrastructure services
echo "Stopping infrastructure services..."
docker-compose down

echo "All services stopped!"
