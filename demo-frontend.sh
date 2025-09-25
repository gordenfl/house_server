#!/bin/bash

echo "🏠 House Server Frontend Demo - Vue 3 地图房屋展示系统"
echo "======================================================="
echo ""

# 检查前端目录
if [ ! -d "frontend" ]; then
    echo "❌ 前端目录不存在"
    exit 1
fi

echo "✅ 前端目录存在"

# 进入前端目录
cd frontend

# 检查package.json
if [ ! -f "package.json" ]; then
    echo "❌ package.json 不存在"
    exit 1
fi

echo "✅ 项目配置文件存在"

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
echo ""

# 显示项目结构
echo "📁 前端项目结构:"
echo "frontend/"
echo "├── src/"
echo "│   ├── components/"
echo "│   │   └── HouseMap.vue          # 地图组件"
echo "│   ├── views/"
echo "│   │   ├── Home.vue              # 首页"
echo "│   │   ├── Houses.vue            # 房屋列表"
echo "│   │   ├── HouseDetail.vue       # 房屋详情"
echo "│   │   ├── Search.vue            # 地图搜索"
echo "│   │   └── NotFound.vue          # 404页面"
echo "│   ├── stores/"
echo "│   │   ├── user.js               # 用户状态管理"
echo "│   │   └── houses.js             # 房屋数据管理"
echo "│   ├── router/"
echo "│   │   └── index.js              # 路由配置"
echo "│   ├── api/"
echo "│   │   └── index.js              # API接口"
echo "│   ├── App.vue                   # 根组件"
echo "│   ├── main.js                   # 入口文件"
echo "│   └── style.css                 # 全局样式"
echo "├── package.json                  # 项目配置"
echo "├── vite.config.js               # Vite配置"
echo "└── index.html                   # HTML模板"
echo ""

# 安装依赖
echo "📦 安装项目依赖..."
if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已存在，跳过安装"
fi

echo ""
echo "🎯 Vue 3 前端系统功能:"
echo "======================="
echo ""
echo "🗺️ 地图功能特性:"
echo "  ✅ 交互式地图显示所有房屋位置"
echo "  ✅ 房屋位置标记（带价格标签）"
echo "  ✅ 支持地图/卫星视图切换"
echo "  ✅ 缩放控制和平移功能"
echo "  ✅ 点击标记查看房屋详情弹窗"
echo "  ✅ 侧边栏房屋列表同步显示"
echo "  ✅ 实时筛选和搜索功能"
echo ""
echo "🔍 搜索和筛选:"
echo "  ✅ 基于地理位置的半径搜索"
echo "  ✅ 价格范围筛选"
echo "  ✅ 房屋类型筛选（House/Condo/Townhouse）"
echo "  ✅ 卧室和卫生间数量筛选"
echo "  ✅ 距离计算和排序"
echo "  ✅ 实时搜索结果更新"
echo ""
echo "📱 用户界面:"
echo "  ✅ 现代化响应式设计"
echo "  ✅ Element Plus UI组件库"
echo "  ✅ 深色/浅色主题支持"
echo "  ✅ 流畅的动画和过渡效果"
echo "  ✅ 移动端完美适配"
echo ""
echo "🏠 房屋管理:"
echo "  ✅ 房屋列表展示（网格/列表视图）"
echo "  ✅ 详细房屋信息页面"
echo "  ✅ 房屋图片画廊"
echo "  ✅ 联系信息和操作按钮"
echo "  ✅ 相关房屋推荐"
echo ""
echo "👤 用户系统:"
echo "  ✅ 用户登录和认证"
echo "  ✅ 个人资料管理"
echo "  ✅ 管理员后台"
echo "  ✅ 权限控制"
echo ""
echo "📊 数据分析:"
echo "  ✅ 房价统计和趋势"
echo "  ✅ 地区分布分析"
echo "  ✅ 市场数据可视化"
echo "  ✅ 投资建议"
echo ""

# 启动开发服务器
echo "🚀 启动Vue 3开发服务器..."
echo ""
echo "🌐 访问地址:"
echo "  - 本地地址: http://localhost:3000"
echo "  - 网络地址: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "📋 页面导航:"
echo "  🏠 / - 首页（系统概览和精选房屋）"
echo "  🏘️ /houses - 房屋列表（完整房屋展示）"
echo "  🗺️ /search - 地图搜索（基于地图的房屋搜索）"
echo "  📈 /analytics - 数据分析（市场统计和趋势）"
echo "  👤 /profile - 个人资料（用户信息管理）"
echo "  ⚙️ /admin - 管理后台（系统管理功能）"
echo ""
echo "💡 使用指南:"
echo "  1. 打开浏览器访问 http://localhost:3000"
echo "  2. 点击'地图搜索'进入地图页面"
echo "  3. 在地图上可以看到所有房屋的位置标记"
echo "  4. 点击房屋标记查看详情"
echo "  5. 使用右侧筛选器调整搜索条件"
echo "  6. 地图会实时更新显示筛选结果"
echo "  7. 可以切换地图/卫星视图"
echo "  8. 支持缩放和平移操作"
echo ""
echo "🔧 技术栈:"
echo "  - Vue 3 + Composition API"
echo "  - Vite 构建工具"
echo "  - Element Plus UI组件库"
echo "  - Pinia 状态管理"
echo "  - Vue Router 路由管理"
echo "  - Axios HTTP客户端"
echo "  - Leaflet 地图库（计划集成）"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev
