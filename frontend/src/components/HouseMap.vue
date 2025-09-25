<template>
  <div class="house-map-container">
    <!-- 地图工具栏 -->
    <div class="map-toolbar">
      <div class="toolbar-left">
        <el-button-group>
          <el-button 
            :type="viewMode === 'map' ? 'primary' : 'default'"
            @click="viewMode = 'map'"
            size="small"
          >
            <el-icon><Location /></el-icon>
            地图视图
          </el-button>
          <el-button 
            :type="viewMode === 'satellite' ? 'primary' : 'default'"
            @click="viewMode = 'satellite'"
            size="small"
          >
            <el-icon><Picture /></el-icon>
            卫星视图
          </el-button>
        </el-button-group>
        
        <el-divider direction="vertical" />
        
        <div class="zoom-controls">
          <el-button @click="zoomIn" size="small" circle>
            <el-icon><Plus /></el-icon>
          </el-button>
          <el-button @click="zoomOut" size="small" circle>
            <el-icon><Minus /></el-icon>
          </el-button>
        </div>
      </div>
      
      <div class="toolbar-right">
        <el-button @click="centerOnIrvine" size="small">
          <el-icon><Aim /></el-icon>
          回到Irvine
        </el-button>
        <el-button @click="showAllHouses" size="small">
          <el-icon><House /></el-icon>
          显示所有房屋
        </el-button>
      </div>
    </div>

    <!-- 地图容器 -->
    <div class="map-wrapper">
      <div id="map" class="map-container"></div>
      
      <!-- 地图加载状态 -->
      <div v-if="mapLoading" class="map-loading">
        <el-loading-spinner />
        <p>正在加载地图...</p>
      </div>
    </div>

    <!-- 侧边栏 -->
    <div class="map-sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h3>房屋列表</h3>
        <el-button 
          @click="sidebarCollapsed = !sidebarCollapsed"
          type="text"
          size="small"
        >
          <el-icon>
            <component :is="sidebarCollapsed ? 'ArrowRight' : 'ArrowLeft'" />
          </el-icon>
        </el-button>
      </div>
      
      <div v-if="!sidebarCollapsed" class="sidebar-content">
        <!-- 筛选器 -->
        <div class="sidebar-filters">
          <el-input
            v-model="searchQuery"
            placeholder="搜索房屋地址..."
            @input="filterHouses"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="priceFilter"
            placeholder="价格范围"
            @change="filterHouses"
            clearable
            size="small"
          >
            <el-option label="不限" :value="null" />
            <el-option label="50万以下" value="500000" />
            <el-option label="50-100万" value="1000000" />
            <el-option label="100-150万" value="1500000" />
            <el-option label="150万以上" value="2000000" />
          </el-select>
          
          <el-select
            v-model="typeFilter"
            placeholder="房屋类型"
            @change="filterHouses"
            clearable
            size="small"
          >
            <el-option label="不限" :value="null" />
            <el-option label="House" value="House" />
            <el-option label="Condo" value="Condo" />
            <el-option label="Townhouse" value="Townhouse" />
          </el-select>
        </div>
        
        <!-- 房屋列表 -->
        <div class="houses-list">
          <div 
            v-for="house in filteredHouses"
            :key="house.id"
            class="house-list-item"
            :class="{ 'active': selectedHouse?.id === house.id }"
            @click="selectHouse(house)"
          >
            <div class="house-image">
              <img :src="house.imageUrl" :alt="house.address" />
            </div>
            <div class="house-info">
              <h4>{{ house.address }}</h4>
              <p class="house-price">${{ formatPrice(house.price) }}</p>
              <div class="house-details">
                <span>{{ house.bedrooms }}床</span>
                <span>{{ house.bathrooms }}卫</span>
                <span>{{ formatArea(house.areaSqft) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 统计信息 -->
        <div class="map-stats">
          <h4>地图统计</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">总房屋数</span>
              <span class="stat-value">{{ houses.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">平均价格</span>
              <span class="stat-value">${{ formatPrice(averagePrice) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">价格范围</span>
              <span class="stat-value">${{ formatPrice(minPrice) }} - ${{ formatPrice(maxPrice) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 房屋详情弹窗 -->
    <el-dialog
      v-model="showHouseDetail"
      :title="selectedHouse?.address"
      width="600px"
      @close="closeHouseDetail"
    >
      <div v-if="selectedHouse" class="house-detail-popup">
        <div class="detail-image">
          <img :src="selectedHouse.imageUrl" :alt="selectedHouse.address" />
        </div>
        <div class="detail-info">
          <div class="detail-price">${{ formatPrice(selectedHouse.price) }}</div>
          <div class="detail-location">{{ selectedHouse.city }}, {{ selectedHouse.state }} {{ selectedHouse.zipCode }}</div>
          <div class="detail-specs">
            <span>{{ selectedHouse.bedrooms }} 卧室</span>
            <span>{{ selectedHouse.bathrooms }} 卫生间</span>
            <span>{{ formatArea(selectedHouse.areaSqft) }}</span>
            <span>{{ selectedHouse.houseType }}</span>
          </div>
          <div v-if="selectedHouse.description" class="detail-description">
            {{ selectedHouse.description }}
          </div>
          <div class="detail-actions">
            <el-button type="primary" @click="goToHouseDetail(selectedHouse.id)">
              查看详情
            </el-button>
            <el-button @click="centerMapOnHouse(selectedHouse)">
              在地图中查看
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useHousesStore } from '../stores/houses'

const router = useRouter()
const housesStore = useHousesStore()

// 响应式数据
const mapLoading = ref(true)
const viewMode = ref('map')
const sidebarCollapsed = ref(false)
const searchQuery = ref('')
const priceFilter = ref(null)
const typeFilter = ref(null)
const selectedHouse = ref(null)
const showHouseDetail = ref(false)

// 地图相关
let map = null
let markers = []
let markerGroup = null

// 计算属性
const houses = computed(() => housesStore.houses)

const filteredHouses = computed(() => {
  let result = houses.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(house => 
      house.address.toLowerCase().includes(query) ||
      house.city.toLowerCase().includes(query) ||
      house.zipCode.includes(query)
    )
  }

  // 价格过滤
  if (priceFilter.value) {
    const price = priceFilter.value
    if (price === '500000') {
      result = result.filter(house => house.price < 500000)
    } else if (price === '1000000') {
      result = result.filter(house => house.price >= 500000 && house.price < 1000000)
    } else if (price === '1500000') {
      result = result.filter(house => house.price >= 1000000 && house.price < 1500000)
    } else if (price === '2000000') {
      result = result.filter(house => house.price >= 1500000)
    }
  }

  // 类型过滤
  if (typeFilter.value) {
    result = result.filter(house => house.houseType === typeFilter.value)
  }

  return result
})

const averagePrice = computed(() => {
  if (!houses.value.length) return 0
  const total = houses.value.reduce((sum, house) => sum + (house.price || 0), 0)
  return Math.round(total / houses.value.length)
})

const minPrice = computed(() => {
  if (!houses.value.length) return 0
  return Math.min(...houses.value.map(h => h.price || 0))
})

const maxPrice = computed(() => {
  if (!houses.value.length) return 0
  return Math.max(...houses.value.map(h => h.price || 0))
})

// 方法
const formatPrice = (price) => {
  if (!price) return '0'
  return new Intl.NumberFormat('en-US').format(price)
}

const formatArea = (area) => {
  if (!area) return '0 sqft'
  return `${new Intl.NumberFormat('en-US').format(area)} sqft`
}

const initMap = async () => {
  mapLoading.value = true
  
  try {
    // 创建地图（使用简化的地图实现）
    const mapContainer = document.getElementById('map')
    if (!mapContainer) return

    // 创建地图HTML结构
    mapContainer.innerHTML = `
      <div class="simple-map">
        <div class="map-overlay">
          <div class="map-center">
            <div class="location-pin">📍</div>
            <div class="location-text">Irvine, CA</div>
            <div class="coordinates">33.6846, -117.8265</div>
          </div>
          <div class="map-controls">
            <div class="control-group">
              <button onclick="zoomIn()" class="map-control-btn">+</button>
              <button onclick="zoomOut()" class="map-control-btn">-</button>
            </div>
          </div>
        </div>
      </div>
    `

    // 添加CSS样式
    const style = document.createElement('style')
    style.textContent = `
      .simple-map {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #87CEEB 0%, #98FB98 100%);
        position: relative;
        overflow: hidden;
      }
      
      .map-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .map-center {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      }
      
      .location-pin {
        font-size: 3rem;
        margin-bottom: 10px;
      }
      
      .location-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 5px;
      }
      
      .coordinates {
        color: #7f8c8d;
        font-size: 0.9rem;
      }
      
      .map-controls {
        position: absolute;
        top: 20px;
        right: 20px;
      }
      
      .control-group {
        display: flex;
        flex-direction: column;
        gap: 5px;
      }
      
      .map-control-btn {
        width: 40px;
        height: 40px;
        border: none;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .map-control-btn:hover {
        background: #f0f0f0;
      }
    `
    document.head.appendChild(style)

    // 添加房屋标记
    await addHouseMarkers()
    
  } catch (error) {
    console.error('地图初始化失败:', error)
  } finally {
    mapLoading.value = false
  }
}

const addHouseMarkers = async () => {
  const mapContainer = document.getElementById('map')
  if (!mapContainer || !houses.value.length) return

  // 创建房屋标记容器
  const markersContainer = document.createElement('div')
  markersContainer.className = 'house-markers'
  markersContainer.style.cssText = `
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  `

  // 为每个房屋添加标记
  houses.value.forEach((house, index) => {
    const marker = createHouseMarker(house, index)
    markersContainer.appendChild(marker)
  })

  mapContainer.appendChild(markersContainer)
}

const createHouseMarker = (house, index) => {
  const marker = document.createElement('div')
  marker.className = 'house-marker'
  marker.style.cssText = `
    position: absolute;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 3px solid white;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 0.9rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    pointer-events: auto;
    transition: all 0.3s ease;
    z-index: 10;
  `

  // 计算标记位置（基于房屋坐标）
  const x = 30 + (index * 15) % 60 // 模拟X坐标
  const y = 30 + (index * 20) % 50 // 模拟Y坐标
  
  marker.style.left = `${x}%`
  marker.style.top = `${y}%`

  // 添加价格标签
  const priceLabel = document.createElement('div')
  priceLabel.className = 'price-label'
  priceLabel.textContent = `$${(house.price / 1000).toFixed(0)}K`
  priceLabel.style.cssText = `
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.7rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s ease;
  `
  
  marker.appendChild(priceLabel)

  // 添加悬停效果
  marker.addEventListener('mouseenter', () => {
    marker.style.transform = 'scale(1.2)'
    priceLabel.style.opacity = '1'
  })

  marker.addEventListener('mouseleave', () => {
    marker.style.transform = 'scale(1)'
    priceLabel.style.opacity = '0'
  })

  // 添加点击事件
  marker.addEventListener('click', () => {
    selectHouse(house)
    showHouseDetail.value = true
  })

  marker.textContent = index + 1
  return marker
}

const selectHouse = (house) => {
  selectedHouse.value = house
}

const closeHouseDetail = () => {
  showHouseDetail.value = false
  selectedHouse.value = null
}

const goToHouseDetail = (id) => {
  router.push(`/houses/${id}`)
}

const centerMapOnHouse = (house) => {
  // 在实际实现中，这里会移动地图到房屋位置
  showHouseDetail.value = false
  ElMessage.success(`已定位到 ${house.address}`)
}

const centerOnIrvine = () => {
  ElMessage.info('已回到Irvine中心')
}

const showAllHouses = () => {
  ElMessage.info(`显示了 ${houses.value.length} 个房屋`)
}

const zoomIn = () => {
  ElMessage.info('放大地图')
}

const zoomOut = () => {
  ElMessage.info('缩小地图')
}

const filterHouses = () => {
  // 过滤逻辑在计算属性中处理
}

// 生命周期
onMounted(async () => {
  await housesStore.fetchHouses()
  await initMap()
})

// 监听房屋数据变化
watch(houses, () => {
  if (houses.value.length > 0) {
    initMap()
  }
})
</script>

<style scoped>
.house-map-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.map-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.zoom-controls {
  display: flex;
  gap: 4px;
}

.map-wrapper {
  flex: 1;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 1000;
}

.map-sidebar {
  position: absolute;
  top: 60px;
  right: 0;
  width: 350px;
  height: calc(100vh - 60px);
  background: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  z-index: 999;
}

.sidebar-collapsed {
  transform: translateX(calc(100% - 40px));
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
}

.sidebar-header h3 {
  margin: 0;
  color: #2c3e50;
}

.sidebar-content {
  height: calc(100% - 60px);
  overflow-y: auto;
  padding: 20px;
}

.sidebar-filters {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.houses-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.house-list-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.house-list-item:hover {
  border-color: #667eea;
  background: #f8fafc;
}

.house-list-item.active {
  border-color: #667eea;
  background: #f0f9ff;
}

.house-image {
  width: 60px;
  height: 45px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.house-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.house-info h4 {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: 600;
}

.house-price {
  font-size: 1rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 4px;
}

.house-details {
  display: flex;
  gap: 8px;
  font-size: 0.8rem;
  color: #7f8c8d;
}

.map-stats {
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.map-stats h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
}

.stats-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  color: #2c3e50;
  font-weight: 600;
}

.house-detail-popup {
  display: flex;
  gap: 20px;
}

.detail-image {
  width: 200px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-info {
  flex: 1;
}

.detail-price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.detail-location {
  color: #7f8c8d;
  margin-bottom: 12px;
}

.detail-specs {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 0.9rem;
  color: #5a6c7d;
}

.detail-description {
  color: #5a6c7d;
  line-height: 1.5;
  margin-bottom: 16px;
}

.detail-actions {
  display: flex;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .map-sidebar {
    width: 100%;
    height: 50vh;
    top: auto;
    bottom: 0;
    transform: translateY(calc(100% - 60px));
  }
  
  .sidebar-collapsed {
    transform: translateY(calc(100% - 60px));
  }
  
  .house-detail-popup {
    flex-direction: column;
  }
  
  .detail-image {
    width: 100%;
    height: 200px;
  }
}
</style>
