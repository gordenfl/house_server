#!/bin/bash

echo "🏠 House Server Frontend - Vue 3 客户端"
echo "========================================"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装。请先安装 Node.js 16+ 版本"
    echo "   下载地址: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装。请先安装 npm"
    exit 1
fi

echo "✅ npm 版本: $(npm --version)"

# 安装依赖
echo "📦 安装项目依赖..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"

# 启动开发服务器
echo "🚀 启动开发服务器..."
echo ""
echo "前端应用将在以下地址启动:"
echo "  - 本地地址: http://localhost:3000"
echo "  - 网络地址: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "功能特性:"
echo "  ✅ 响应式设计 - 支持桌面和移动设备"
echo "  ✅ 房屋列表和详情页面"
echo "  ✅ 高级筛选和搜索功能"
echo "  ✅ 地图集成和地理空间搜索"
echo "  ✅ 数据分析和统计图表"
echo "  ✅ 用户认证和管理"
echo "  ✅ 管理员后台"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev
