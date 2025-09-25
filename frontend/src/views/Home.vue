<template>
  <div class="home-page">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">在Irvine找到您的理想家园</h1>
        <p class="hero-subtitle">探索Irvine, CA最优质的房地产资源，享受现代化的生活体验</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="goToHouses">
            <el-icon><House /></el-icon>
            浏览房屋
          </el-button>
          <el-button size="large" @click="goToSearch">
            <el-icon><Location /></el-icon>
            地图搜索
          </el-button>
        </div>
      </div>
      <div class="hero-stats">
        <div class="stat-item">
          <div class="stat-number">{{ houseStats?.total || 10 }}</div>
          <div class="stat-label">可用房屋</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">${{ formatPrice(houseStats?.avgPrice || 1130000) }}</div>
          <div class="stat-label">平均价格</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ houseStats?.avgBedrooms || 3.6 }}</div>
          <div class="stat-label">平均卧室</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ houseStats?.avgBathrooms || 3.0 }}</div>
          <div class="stat-label">平均卫生间</div>
        </div>
      </div>
    </section>

    <!-- 特色房屋 -->
    <section class="featured-section">
      <div class="section-header">
        <h2>精选房屋</h2>
        <p>发现Irvine最受欢迎的房产</p>
      </div>
      <div class="houses-grid" v-loading="loading">
        <div 
          v-for="house in featuredHouses" 
          :key="house.id"
          class="house-card"
          @click="goToHouseDetail(house.id)"
        >
          <div class="house-image">
            <img :src="house.imageUrl" :alt="house.address" />
            <div class="house-price">${{ formatPrice(house.price) }}</div>
            <div class="house-status" :class="house.houseStatus.toLowerCase()">
              {{ getStatusText(house.houseStatus) }}
            </div>
          </div>
          <div class="house-info">
            <h3 class="house-address">{{ house.address }}</h3>
            <p class="house-location">{{ house.city }}, {{ house.state }} {{ house.zipCode }}</p>
            <div class="house-details">
              <span class="detail-item">
                <el-icon><House /></el-icon>
                {{ house.bedrooms }} 卧室
              </span>
              <span class="detail-item">
                <el-icon><Bath /></el-icon>
                {{ house.bathrooms }} 卫生间
              </span>
              <span class="detail-item">
                <el-icon><Expand /></el-icon>
                {{ formatArea(house.areaSqft) }}
              </span>
            </div>
            <div class="house-type">{{ house.houseType }}</div>
          </div>
        </div>
      </div>
      <div class="section-footer">
        <el-button type="primary" size="large" @click="goToHouses">
          查看所有房屋
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
    </section>

    <!-- 服务特色 -->
    <section class="features-section">
      <div class="section-header">
        <h2>为什么选择我们</h2>
        <p>专业的房地产服务，让您的购房体验更加顺畅</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><Location /></el-icon>
          </div>
          <h3>地理搜索</h3>
          <p>基于地图的智能搜索，帮您找到理想位置的房产</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <h3>数据分析</h3>
          <p>详细的市场分析报告，助您做出明智的投资决策</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><User /></el-icon>
          </div>
          <h3>专业服务</h3>
          <p>经验丰富的专业团队，为您提供全方位的购房支持</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><Monitor /></el-icon>
          </div>
          <h3>实时更新</h3>
          <p>实时更新的房源信息，确保您获得最新的市场动态</p>
        </div>
      </div>
    </section>

    <!-- 地区信息 -->
    <section class="location-section">
      <div class="section-header">
        <h2>关于Irvine, CA</h2>
        <p>探索这座美丽的南加州城市</p>
      </div>
      <div class="location-content">
        <div class="location-info">
          <h3>为什么选择Irvine？</h3>
          <ul>
            <li>🏫 优质的教育资源 - 拥有全美顶尖的公立学校</li>
            <li>🌳 优美的自然环境 - 四季如春的气候和美丽的公园</li>
            <li>💼 繁荣的商业环境 - 众多科技公司和就业机会</li>
            <li>🛡️ 安全的社区环境 - 全美最安全的城市之一</li>
            <li>🏖️ 便利的地理位置 - 靠近海滩和洛杉矶</li>
          </ul>
        </div>
        <div class="location-stats">
          <div class="location-stat">
            <div class="stat-number">280,000+</div>
            <div class="stat-label">人口</div>
          </div>
          <div class="location-stat">
            <div class="stat-number">66.7</div>
            <div class="stat-label">平方英里</div>
          </div>
          <div class="location-stat">
            <div class="stat-number">$1.1M</div>
            <div class="stat-label">平均房价</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHousesStore } from '../stores/houses'

const router = useRouter()
const housesStore = useHousesStore()

// 响应式数据
const loading = ref(false)

// 计算属性
const houseStats = computed(() => housesStore.houseStats)
const featuredHouses = computed(() => {
  return housesStore.houses.slice(0, 6)
})

// 方法
const goToHouses = () => {
  router.push('/houses')
}

const goToSearch = () => {
  router.push('/search')
}

const goToHouseDetail = (id) => {
  router.push(`/houses/${id}`)
}

const formatPrice = (price) => {
  if (!price) return '0'
  return new Intl.NumberFormat('en-US').format(price)
}

const formatArea = (area) => {
  if (!area) return '0 sqft'
  return `${new Intl.NumberFormat('en-US').format(area)} sqft`
}

const getStatusText = (status) => {
  const statusMap = {
    'FOR_SALE': '出售中',
    'SOLD': '已售出',
    'FORECLOSED': '法拍'
  }
  return statusMap[status] || status
}

// 生命周期
onMounted(async () => {
  loading.value = true
  try {
    await housesStore.fetchHouses()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

/* 英雄区域 */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  border-radius: 16px;
  margin-bottom: 60px;
  text-align: center;
}

.hero-content {
  margin-bottom: 40px;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 20px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 30px;
  max-width: 800px;
  margin: 0 auto;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.8;
}

/* 特色房屋 */
.featured-section {
  margin-bottom: 80px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 16px;
}

.section-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.houses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.house-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.house-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.house-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.house-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.house-price {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: bold;
}

.house-status {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
}

.house-status.for_sale {
  background: #67c23a;
  color: white;
}

.house-status.sold {
  background: #f56c6c;
  color: white;
}

.house-status.foreclosed {
  background: #e6a23c;
  color: white;
}

.house-info {
  padding: 20px;
}

.house-address {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.house-location {
  color: #7f8c8d;
  margin-bottom: 16px;
}

.house-details {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #5a6c7d;
  font-size: 0.9rem;
}

.house-type {
  display: inline-block;
  background: #f0f9ff;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.section-footer {
  text-align: center;
}

/* 服务特色 */
.features-section {
  margin-bottom: 80px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-card {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
}

.feature-card h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 16px;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

/* 地区信息 */
.location-section {
  background: #f8fafc;
  padding: 60px 40px;
  border-radius: 16px;
  margin-bottom: 40px;
}

.location-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  align-items: start;
}

.location-info h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

.location-info ul {
  list-style: none;
  padding: 0;
}

.location-info li {
  padding: 12px 0;
  color: #5a6c7d;
  font-size: 1.1rem;
  border-bottom: 1px solid #e5e7eb;
}

.location-info li:last-child {
  border-bottom: none;
}

.location-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.location-stat {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.location-stat .stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.location-stat .stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .houses-grid {
    grid-template-columns: 1fr;
  }
  
  .location-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .location-section {
    padding: 40px 20px;
  }
}
</style>
