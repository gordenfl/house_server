#!/bin/bash

echo "🏠 Irvine CA House Data Test Script"
echo "===================================="

# 检查SQLite数据库
if [ -f "zillow-scraper/irvine_houses.db" ]; then
    echo "✅ SQLite database found"
    echo ""
    echo "📊 House Data Summary:"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT COUNT(*) as 'Total Houses' FROM houses;"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT AVG(price) as 'Average Price' FROM houses;"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT MIN(price) as 'Min Price', MAX(price) as 'Max Price' FROM houses;"
    echo ""
    echo "🏠 Sample Houses:"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT address, price, bedrooms, bathrooms, house_type FROM houses LIMIT 5;"
    echo ""
    echo "🏘️  House Types Distribution:"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT house_type, COUNT(*) as count FROM houses GROUP BY house_type;"
    echo ""
    echo "📍 Location Distribution:"
    sqlite3 zillow-scraper/irvine_houses.db "SELECT zip_code, COUNT(*) as count FROM houses GROUP BY zip_code;"
else
    echo "❌ SQLite database not found"
    echo "Please run the data generation script first"
fi

echo ""
echo "📁 Generated Files:"
ls -la zillow-scraper/ | grep -E "\.(db|json)$"

echo ""
echo "🖼️  Images:"
ls -la zillow-scraper/images/ | head -5

echo ""
echo "📋 JSON Data Preview:"
if [ -f "zillow-scraper/irvine_houses_data.json" ]; then
    echo "First house data:"
    head -20 zillow-scraper/irvine_houses_data.json
fi

echo ""
echo "📊 Statistics:"
if [ -f "zillow-scraper/irvine_stats.json" ]; then
    cat zillow-scraper/irvine_stats.json
fi

echo ""
echo "🔧 Available Commands:"
echo "   - View all houses: sqlite3 zillow-scraper/irvine_houses.db 'SELECT * FROM houses;'"
echo "   - Search by price: sqlite3 zillow-scraper/irvine_houses.db \"SELECT address, price FROM houses WHERE price > 1000000;\""
echo "   - Search by type: sqlite3 zillow-scraper/irvine_houses.db \"SELECT address, house_type FROM houses WHERE house_type = 'House';\""
echo "   - Search by bedrooms: sqlite3 zillow-scraper/irvine_houses.db \"SELECT address, bedrooms, bathrooms FROM houses WHERE bedrooms >= 4;\""
