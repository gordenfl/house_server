#!/bin/bash

echo "🏠 House Server Frontend Demo - Vue 3 地图房屋展示系统"
echo "======================================================="

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
echo "🚀 启动Vue 3前端应用..."
echo ""
echo "🎯 系统功能特性:"
echo "  📍 交互式地图显示所有房屋位置"
echo "  🔍 基于地理位置的智能搜索"
echo "  🏠 房屋列表和详情页面"
echo "  📊 数据分析和统计图表"
echo "  👤 用户认证和管理系统"
echo "  🛠️ 管理员后台面板"
echo "  📱 完全响应式设计"
echo ""
echo "🌐 访问地址:"
echo "  - 本地地址: http://localhost:3000"
echo "  - 网络地址: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "🗺️ 地图功能:"
echo "  ✅ 显示所有Irvine房屋位置标记"
echo "  ✅ 支持地图/卫星视图切换"
echo "  ✅ 缩放控制和平移功能"
echo "  ✅ 点击标记查看房屋详情"
echo "  ✅ 半径搜索和筛选功能"
echo "  ✅ 距离计算和排序"
echo ""
echo "📋 页面导航:"
echo "  🏠 首页 - 系统概览和精选房屋"
echo "  🏘️ 房屋列表 - 完整的房屋展示"
echo "  🗺️ 地图搜索 - 基于地图的房屋搜索"
echo "  📈 数据分析 - 市场统计和趋势"
echo "  👤 个人资料 - 用户信息管理"
echo "  ⚙️ 管理后台 - 系统管理功能"
echo ""
echo "💡 使用提示:"
echo "  - 在地图页面可以点击房屋标记查看详情"
echo "  - 使用筛选器可以快速找到符合条件的房屋"
echo "  - 支持按价格、类型、卧室数量等多维度筛选"
echo "  - 地图支持缩放和拖拽操作"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev
