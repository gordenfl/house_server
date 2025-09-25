<template>
  <div class="house-detail-page" v-loading="loading">
    <div v-if="house" class="detail-container">
      <!-- 返回按钮 -->
      <div class="back-section">
        <el-button @click="$router.back()" type="text">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
      </div>

      <!-- 房屋基本信息 -->
      <div class="house-header">
        <div class="house-title">
          <h1>{{ house.address }}</h1>
          <p class="house-location">{{ house.city }}, {{ house.state }} {{ house.zipCode }}</p>
        </div>
        <div class="house-price-section">
          <div class="price">${{ formatPrice(house.price) }}</div>
          <div class="status" :class="house.houseStatus.toLowerCase()">
            {{ getStatusText(house.houseStatus) }}
          </div>
        </div>
      </div>

      <!-- 图片画廊 -->
      <div class="image-gallery">
        <div class="main-image">
          <img :src="house.imageUrl" :alt="house.address" />
        </div>
        <div class="image-thumbnails">
          <div 
            v-for="(image, index) in additionalImages" 
            :key="index"
            class="thumbnail"
            @click="currentImageIndex = index"
          >
            <img :src="image" :alt="`${house.address} - 图片 ${index + 1}`" />
          </div>
        </div>
      </div>

      <!-- 房屋详细信息 -->
      <div class="house-details">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="16">
            <!-- 基本信息 -->
            <el-card class="info-card">
              <template #header>
                <h3>房屋信息</h3>
              </template>
              <div class="info-grid">
                <div class="info-item">
                  <el-icon><House /></el-icon>
                  <div class="info-content">
                    <label>房屋类型</label>
                    <span>{{ house.houseType }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <el-icon><Bed /></el-icon>
                  <div class="info-content">
                    <label>卧室</label>
                    <span>{{ house.bedrooms }} 间</span>
                  </div>
                </div>
                <div class="info-item">
                  <el-icon><Bath /></el-icon>
                  <div class="info-content">
                    <label>卫生间</label>
                    <span>{{ house.bathrooms }} 间</span>
                  </div>
                </div>
                <div class="info-item">
                  <el-icon><Expand /></el-icon>
                  <div class="info-content">
                    <label>建筑面积</label>
                    <span>{{ formatArea(house.areaSqft) }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <el-icon><OfficeBuilding /></el-icon>
                  <div class="info-content">
                    <label>土地面积</label>
                    <span>{{ formatArea(house.lotAreaSqft) }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <el-icon><Calendar /></el-icon>
                  <div class="info-content">
                    <label>建造年份</label>
                    <span>{{ house.buildYear || '未知' }}</span>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 房屋描述 -->
            <el-card class="description-card" v-if="house.description">
              <template #header>
                <h3>房屋描述</h3>
              </template>
              <p>{{ house.description }}</p>
            </el-card>

            <!-- 地图位置 -->
            <el-card class="map-card">
              <template #header>
                <h3>位置信息</h3>
              </template>
              <div class="map-container">
                <div id="house-map" class="map"></div>
              </div>
              <div class="location-details">
                <p><strong>地址:</strong> {{ house.address }}</p>
                <p><strong>城市:</strong> {{ house.city }}, {{ house.state }}</p>
                <p><strong>邮编:</strong> {{ house.zipCode }}</p>
                <p><strong>坐标:</strong> {{ house.latitude }}, {{ house.longitude }}</p>
              </div>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="8">
            <!-- 联系信息 -->
            <el-card class="contact-card">
              <template #header>
                <h3>联系信息</h3>
              </template>
              <div class="contact-actions">
                <el-button type="primary" size="large" class="contact-btn">
                  <el-icon><Phone /></el-icon>
                  立即联系
                </el-button>
                <el-button size="large" class="contact-btn">
                  <el-icon><Message /></el-icon>
                  发送消息
                </el-button>
                <el-button size="large" class="contact-btn">
                  <el-icon><Star /></el-icon>
                  收藏房屋
                </el-button>
              </div>
              <div class="contact-info">
                <div class="contact-item">
                  <el-icon><User /></el-icon>
                  <span>房产经纪人</span>
                </div>
                <div class="contact-item">
                  <el-icon><Phone /></el-icon>
                  <span>(949) 123-4567</span>
                </div>
                <div class="contact-item">
                  <el-icon><Message /></el-icon>
                  <span>agent@houseserver.com</span>
                </div>
              </div>
            </el-card>

            <!-- 房屋统计 -->
            <el-card class="stats-card">
              <template #header>
                <h3>房屋统计</h3>
              </template>
              <div class="stats-list">
                <div class="stat-item">
                  <span class="stat-label">挂牌时间</span>
                  <span class="stat-value">{{ formatDate(house.createdAt) }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">上次更新</span>
                  <span class="stat-value">{{ formatDate(house.updatedAt) }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">房屋ID</span>
                  <span class="stat-value">#{{ house.id }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Zillow ID</span>
                  <span class="stat-value">{{ house.zillowId || 'N/A' }}</span>
                </div>
              </div>
            </el-card>

            <!-- 相关房屋 -->
            <el-card class="related-card">
              <template #header>
                <h3>附近房屋</h3>
              </template>
              <div class="related-houses">
                <div 
                  v-for="relatedHouse in relatedHouses" 
                  :key="relatedHouse.id"
                  class="related-house"
                  @click="goToHouseDetail(relatedHouse.id)"
                >
                  <img :src="relatedHouse.imageUrl" :alt="relatedHouse.address" />
                  <div class="related-info">
                    <h4>{{ relatedHouse.address }}</h4>
                    <p>${{ formatPrice(relatedHouse.price) }}</p>
                    <div class="related-details">
                      <span>{{ relatedHouse.bedrooms }}床</span>
                      <span>{{ relatedHouse.bathrooms }}卫</span>
                    </div>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="!loading" class="error-state">
      <el-empty description="房屋信息不存在">
        <el-button type="primary" @click="$router.push('/houses')">返回房屋列表</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHousesStore } from '../stores/houses'

const route = useRoute()
const router = useRouter()
const housesStore = useHousesStore()

// 响应式数据
const loading = ref(false)
const currentImageIndex = ref(0)

// 计算属性
const house = computed(() => housesStore.currentHouse)

const additionalImages = computed(() => {
  if (!house.value?.additionalImages) return []
  return house.value.additionalImages
})

const relatedHouses = computed(() => {
  return housesStore.houses
    .filter(h => h.id !== house.value?.id)
    .slice(0, 3)
})

// 方法
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

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const getStatusText = (status) => {
  const statusMap = {
    'FOR_SALE': '出售中',
    'SOLD': '已售出',
    'FORECLOSED': '法拍'
  }
  return statusMap[status] || status
}

const initMap = async () => {
  if (!house.value) return

  await nextTick()

  // 简单的地图显示（实际项目中可以使用 Leaflet）
  const mapContainer = document.getElementById('house-map')
  if (mapContainer) {
    mapContainer.innerHTML = `
      <div style="
        width: 100%; 
        height: 200px; 
        background: #f0f0f0; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        border-radius: 8px;
        color: #666;
      ">
        <div style="text-align: center;">
          <div style="font-size: 2rem; margin-bottom: 8px;">📍</div>
          <div>地图位置</div>
          <div style="font-size: 0.9rem; margin-top: 4px;">
            ${house.value.latitude}, ${house.value.longitude}
          </div>
        </div>
      </div>
    `
  }
}

// 生命周期
onMounted(async () => {
  loading.value = true
  try {
    await housesStore.fetchHouseById(route.params.id)
    if (house.value) {
      await initMap()
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.house-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.back-section {
  margin-bottom: 20px;
}

.house-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.house-title h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 8px;
}

.house-location {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.house-price-section {
  text-align: right;
}

.price {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.status {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status.for_sale {
  background: #f0f9ff;
  color: #0369a1;
}

.status.sold {
  background: #fef2f2;
  color: #dc2626;
}

.status.foreclosed {
  background: #fffbeb;
  color: #d97706;
}

.image-gallery {
  margin-bottom: 30px;
}

.main-image {
  margin-bottom: 16px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.main-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.image-thumbnails {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.thumbnail {
  flex-shrink: 0;
  width: 80px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #667eea;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.house-details {
  margin-bottom: 40px;
}

.info-card,
.description-card,
.map-card,
.contact-card,
.stats-card,
.related-card {
  margin-bottom: 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-item .el-icon {
  font-size: 1.5rem;
  color: #667eea;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-content label {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: 500;
}

.info-content span {
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 600;
}

.map-container {
  margin-bottom: 16px;
}

.map {
  width: 100%;
  height: 200px;
  border-radius: 8px;
}

.location-details {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
}

.location-details p {
  margin: 4px 0;
  color: #5a6c7d;
}

.contact-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.contact-btn {
  width: 100%;
}

.contact-info {
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  color: #5a6c7d;
}

.contact-item .el-icon {
  color: #667eea;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  color: #2c3e50;
  font-weight: 500;
}

.related-houses {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.related-house {
  display: flex;
  gap: 12px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.related-house:hover {
  background: #f8fafc;
}

.related-house img {
  width: 60px;
  height: 45px;
  object-fit: cover;
  border-radius: 6px;
}

.related-info {
  flex: 1;
}

.related-info h4 {
  font-size: 0.9rem;
  color: #2c3e50;
  margin-bottom: 4px;
}

.related-info p {
  font-size: 1rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 4px;
}

.related-details {
  display: flex;
  gap: 12px;
  font-size: 0.8rem;
  color: #7f8c8d;
}

.error-state {
  text-align: center;
  padding: 60px 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .house-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .house-price-section {
    text-align: left;
  }
  
  .price {
    font-size: 2rem;
  }
  
  .main-image img {
    height: 250px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-actions {
    gap: 8px;
  }
}
</style>
