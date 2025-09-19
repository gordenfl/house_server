# 系统架构说明

## 微服务架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client (Frontend)                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTPS
┌─────────────────────▼───────────────────────────────────────────┐
│                    Gateway Service (8080)                       │
│                    - API Gateway                                │
│                    - Load Balancing                             │
│                    - Authentication                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼────┐ ┌─────▼────────┐ ┌─────────▼─────────┐
│ User Service │ │House   │ │Data Collection│ │Admin Service      │
│ (8081)       │ │Service │ │Service (8083) │ │(8084)             │
│              │ │(8082)  │ │               │ │                   │
│ - 用户管理    │ │- 房屋管理│ │- Zillow数据   │ │- 数据处理器       │
│ - 认证授权    │ │- 地理搜索│ │- 定时任务     │ │- 消息队列监听     │
│ - 密码管理    │ │- 缓存   │ │- 异步处理     │ │- 权限控制         │
└───────┬──────┘ └───┬────┘ └─────┬────────┘ └─────────┬─────────┘
        │             │            │                     │
        └─────────────┼────────────┼─────────────────────┘
                      │            │
┌─────────────────────▼────────────▼─────────────────────────────┐
│                Eureka Server (8761)                           │
│                - Service Discovery                            │
│                - Service Registration                         │
└───────────────────────────────────────────────────────────────┘
```

## 数据层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  User Service │ House Service │ Data Collection │ Admin Service │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                      Service Layer                              │
│  - Business Logic  - Data Processing  - Message Handling       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                      Data Layer                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   MySQL     │ │    Redis    │ │Elasticsearch│ │ RabbitMQ    ││
│  │ (主数据库)   │ │   (缓存)    │ │ (地理搜索)   │ │ (消息队列)   ││
│  │- 用户数据    │ │- 房屋缓存   │ │- 空间索引   │ │- 异步处理   ││
│  │- 房屋数据    │ │- 会话缓存   │ │- 全文搜索   │ │- 数据采集   ││
│  │- 历史记录    │ │- 查询缓存   │ │- 聚合查询   │ │- 事件驱动   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 数据流图

### 1. 用户请求流程
```
Client → Gateway → Service → Database
       ↓
    Authentication
       ↓
    Load Balancing
       ↓
    Service Discovery
```

### 2. 数据采集流程
```
Zillow API → Data Collection Service → RabbitMQ → Admin Service → MySQL
    ↓              ↓                      ↓           ↓
  Schedule      WebClient             Message    Data Processor
  (定时任务)      (HTTP请求)            Queue      (数据转换)
```

### 3. 地理空间搜索流程
```
Client Request → House Service → Elasticsearch → MySQL
      ↓              ↓              ↓
  Coordinates    Geospatial      Spatial      House Data
                 Query           Index        (详细信息)
```

## 技术栈

### 后端技术
- **Spring Boot 3.2**: 微服务框架
- **Spring Cloud**: 微服务治理
- **Spring Security**: 安全认证
- **Spring Data JPA**: 数据访问
- **Spring Data Redis**: 缓存
- **Spring Data Elasticsearch**: 地理搜索
- **Spring AMQP**: 消息队列

### 数据库
- **MySQL 8.0**: 主数据库
- **Redis 7**: 缓存和会话存储
- **Elasticsearch 8**: 地理空间搜索

### 消息队列
- **RabbitMQ**: 异步消息处理

### 服务发现
- **Eureka**: 服务注册与发现

### 网关
- **Spring Cloud Gateway**: API网关

## 部署架构

### Docker容器化
```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Compose                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   MySQL     │ │    Redis    │ │Elasticsearch│ │ RabbitMQ    ││
│  │ Container   │ │ Container   │ │ Container   │ │ Container   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 微服务部署
```
┌─────────────────────────────────────────────────────────────────┐
│                    Microservices                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │ Eureka      │ │ Gateway     │ │ User        │ │ House       ││
│  │ Server      │ │ Service     │ │ Service     │ │ Service     ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
│  ┌─────────────┐ ┌─────────────┐                                │
│  │ Data        │ │ Admin       │                                │
│  │ Collection  │ │ Service     │                                │
│  └─────────────┘ └─────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
```

## 安全架构

### 认证流程
```
1. Client → Login Request
2. User Service → Validate Credentials
3. Generate JWT Token
4. Return Token to Client
5. Client → API Request with Token
6. Gateway → Validate Token
7. Forward to Service
```

### 权限控制
```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Layers                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   Gateway   │ │   Service   │ │  Database   │ │   Network   ││
│  │ Security    │ │ Security    │ │ Security    │ │ Security    ││
│  │ - CORS      │ │ - JWT       │ │ - Encryption│ │ - Firewall  ││
│  │ - Rate Limit│ │ - Roles     │ │ - Access    │ │ - VPN       ││
│  │ - Auth      │ │ - Perms     │ │ Control     │ │ - SSL/TLS   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 监控和日志

### 监控指标
- 服务健康状态
- API响应时间
- 数据库连接池
- 缓存命中率
- 消息队列状态

### 日志聚合
```
┌─────────────────────────────────────────────────────────────────┐
│                    Logging Architecture                         │
│  Services → Log Files → Log Aggregation → Monitoring Dashboard │
│     ↓           ↓            ↓                    ↓            │
│  Application  File    Centralized Log      Real-time          │
│  Logs         System  Storage             Monitoring          │
└─────────────────────────────────────────────────────────────────┘
```

## 扩展性设计

### 水平扩展
- 微服务独立部署
- 数据库读写分离
- 缓存集群
- 负载均衡

### 性能优化
- Redis缓存策略
- Elasticsearch索引优化
- 数据库查询优化
- 异步消息处理

这个架构设计确保了系统的可扩展性、可维护性和高性能。
