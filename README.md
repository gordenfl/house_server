# House Server - Real Estate Management System

一个基于Java Spring Boot的微服务房屋管理系统，类似Zillow系统，提供房屋数据查询、地理空间搜索、用户管理等功能。

## 系统架构

### 微服务组件
- **Gateway Service (8080)**: API网关，统一入口
- **Eureka Server (8761)**: 服务发现与注册中心
- **User Service (8081)**: 用户管理服务
- **House Service (8082)**: 房屋管理服务
- **Data Collection Service (8083)**: 数据采集服务
- **Admin Service (8084)**: 管理员服务

### 基础设施
- **MySQL**: 主数据库，存储结构化数据
- **Redis**: 缓存层，提升查询性能
- **Elasticsearch**: 地理空间搜索和全文搜索
- **RabbitMQ**: 消息队列，异步处理数据采集

## 功能特性

### 1. 房屋管理
- 房屋信息CRUD操作
- 房屋类型：Apartment, Condo, House
- 房屋状态：正在出售, 已经销售, 贷款逾期
- 房屋详细信息：地址、面积、坐标、卧室数量等

### 2. 地理空间搜索
- 根据坐标点查询附近房屋
- 支持半径搜索
- 高性能地理空间查询

### 3. 用户系统
- 用户注册、登录、密码修改
- 用户基本信息管理
- 角色权限控制

### 4. 管理员功能
- 房屋数据修改权限
- 用户数据管理
- 系统监控

### 5. 数据采集
- 定时从Zillow API获取房屋数据
- 异步数据处理
- 数据同步和更新

### 6. 房屋历史记录
- 销售记录：销售时间、价格
- 维修记录：维修规模、时间、费用
- 灾害记录：火灾、谋杀、坍塌等

## 快速开始

### 环境要求
- Java 17+
- Maven 3.6+
- Docker & Docker Compose

### 启动系统

1. **启动基础设施服务**
```bash
docker-compose up -d
```

2. **启动所有微服务**
```bash
./start.sh
```

3. **停止所有服务**
```bash
./stop.sh
```

### 服务端点

- **API Gateway**: http://localhost:8080
- **Eureka Dashboard**: http://localhost:8761
- **用户服务**: http://localhost:8081
- **房屋服务**: http://localhost:8082
- **数据采集服务**: http://localhost:8083
- **管理员服务**: http://localhost:8084

## API 使用示例

### 用户管理

#### 用户注册
```bash
curl -X POST http://localhost:8080/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "passwordHash": "password123",
    "firstName": "Test",
    "lastName": "User"
  }'
```

#### 获取用户信息
```bash
curl http://localhost:8080/api/users/1
```

### 房屋管理

#### 创建房屋
```bash
curl -X POST http://localhost:8080/api/houses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zipCode": "94102",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "houseType": "HOUSE",
    "areaSqft": 2000,
    "houseStatus": "FOR_SALE",
    "bedrooms": 3,
    "bathrooms": 2
  }'
```

#### 地理空间搜索
```bash
curl -X POST http://localhost:8080/api/houses/search/location \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "radiusKm": 5.0
  }'
```

#### 获取房屋列表
```bash
curl http://localhost:8080/api/houses?city=San Francisco&state=CA
```

### 数据采集

#### 手动触发数据采集
```bash
curl -X POST http://localhost:8080/api/data-collection/trigger \
  -H "Authorization: Bearer <admin-token>"
```

## 数据库设计

### 主要表结构

- **users**: 用户信息
- **houses**: 房屋基本信息
- **house_types**: 房屋类型
- **house_statuses**: 房屋状态
- **house_sales**: 房屋销售记录
- **house_maintenance**: 房屋维修记录
- **house_disasters**: 房屋灾害记录

### 初始化数据
系统启动时会自动创建以下数据：
- 默认管理员用户 (admin/admin123)
- 房屋类型枚举
- 房屋状态枚举
- 维修规模枚举
- 灾害类型枚举

## 配置说明

### 环境变量
```bash
# Zillow API配置
export ZILLOW_API_KEY=your-zillow-api-key
export ZILLOW_BASE_URL=https://www.zillow.com/webservice
```

### 数据库配置
默认配置连接本地MySQL数据库：
- 数据库: house_db
- 用户: house_user
- 密码: house_password

## 开发指南

### 项目结构
```
house_server/
├── common/                 # 公共模块
├── user-service/          # 用户服务
├── house-service/         # 房屋服务
├── admin-service/         # 管理员服务
├── data-collection-service/ # 数据采集服务
├── gateway-service/       # 网关服务
├── eureka-server/         # 服务发现
├── sql/                   # 数据库脚本
└── docker-compose.yml     # 基础设施配置
```

### 添加新功能
1. 在相应服务中添加新的Controller和Service
2. 更新数据库模型（如需要）
3. 添加API文档
4. 编写单元测试

## 监控和日志

### 应用监控
- Eureka Dashboard: 服务注册状态
- Spring Boot Actuator: 应用健康检查

### 日志配置
各服务日志级别可通过application.yml配置：
```yaml
logging:
  level:
    com.house: DEBUG
```

## 故障排除

### 常见问题

1. **服务启动失败**
   - 检查端口是否被占用
   - 确认数据库连接正常
   - 查看应用日志

2. **数据采集失败**
   - 确认Zillow API Key配置正确
   - 检查网络连接
   - 查看数据采集服务日志

3. **地理搜索不准确**
   - 确认Elasticsearch服务正常
   - 检查坐标数据格式
   - 验证索引配置

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系开发团队。
