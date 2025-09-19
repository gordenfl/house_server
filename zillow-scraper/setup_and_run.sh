#!/bin/bash

echo "🏠 Zillow Irvine CA House Data Scraper Setup"
echo "============================================="

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# 创建虚拟环境
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# 运行抓取器
echo "🚀 Starting Irvine house data scraping..."
echo "This will scrape house data from Zillow Irvine, CA area"
echo "Estimated time: 5-10 minutes"
echo ""

python3 irvine_simple_scraper.py

echo ""
echo "🎉 Scraping completed!"
echo "📁 Check the following files:"
echo "   - irvine_houses.db (SQLite database)"
echo "   - irvine_houses_data.json (Raw data)"
echo "   - irvine_stats.json (Statistics)"
echo "   - images/ (House images)"
echo ""
echo "💡 To view the data:"
echo "   sqlite3 irvine_houses.db 'SELECT address, price, bedrooms, bathrooms FROM houses LIMIT 10;'"
