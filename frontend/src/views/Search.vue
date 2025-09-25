<template>
  <div class="search-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1>地图搜索房屋</h1>
      <p>在Irvine地区找到您理想的居住位置</p>
    </div>

    <!-- 搜索控制面板 -->
    <div class="search-controls">
      <el-card class="control-card">
        <div class="controls-grid">
          <!-- 位置搜索 -->
          <div class="control-group">
            <label>搜索位置</label>
            <el-input
              v-model="searchLocation"
              placeholder="输入地址或地点..."
              @keyup.enter="searchByLocation"
            >
              <template #prefix>
                <el-icon><Location /></el-icon>
              </template>
              <template #append>
                <el-button @click="searchByLocation" type="primary">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>

          <!-- 半径设置 -->
          <div class="control-group">
            <label>搜索半径</label>
            <el-slider
              v-model="searchRadius"
              :min="0.5"
              :max="10"
              :step="0.5"
              show-input
              :format-tooltip="formatRadius"
            />
            <div class="radius-label">{{ searchRadius }} 公里</div>
          </div>

          <!-- 价格范围 -->
          <div class="control-group">
            <label>价格范围</label>
            <div class="price-range">
              <el-input
                v-model.number="priceRange[0]"
                placeholder="最低价格"
                type="number"
              >
                <template #prepend>$</template>
              </el-input>
              <span class="range-separator">-</span>
              <el-input
                v-model.number="priceRange[1]"
                placeholder="最高价格"
                type="number"
              >
                <template #prepend>$</template>
              </el-input>
            </div>
          </div>

          <!-- 房屋类型 -->
          <div class="control-group">
            <label>房屋类型</label>
            <el-checkbox-group v-model="selectedTypes">
              <el-checkbox label="House">House</el-checkbox>
              <el-checkbox label="Condo">Condo</el-checkbox>
              <el-checkbox label="Townhouse">Townhouse</el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 卧室数量 -->
          <div class="control-group">
            <label>卧室数量</label>
            <el-select v-model="minBedrooms" placeholder="最少卧室" clearable>
              <el-option label="不限" :value="null" />
              <el-option label="1+" :value="1" />
              <el-option label="2+" :value="2" />
              <el-option label="3+" :value="3" />
              <el-option label="4+" :value="4" />
              <el-option label="5+" :value="5" />
            </el-select>
          </div>

          <!-- 卫生间数量 -->
          <div class="control-group">
            <label>卫生间数量</label>
            <el-select v-model="minBathrooms" placeholder="最少卫生间" clearable>
              <el-option label="不限" :value="null" />
              <el-option label="1+" :value="1" />
              <el-option label="1.5+" :value="1.5" />
              <el-option label="2+" :value="2" />
              <el-option label="2.5+" :value="2.5" />
              <el-option label="3+" :value="3" />
            </el-select>
          </div>

          <!-- 操作按钮 -->
          <div class="control-actions">
            <el-button @click="resetFilters" size="large">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
            <el-button type="primary" @click="performSearch" size="large">
              <el-icon><Search /></el-icon>
              搜索房屋
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 地图和结果 -->
    <div class="search-results">
      <el-row :gutter="20">
        <!-- 地图区域 -->
        <el-col :xs="24" :lg="16">
          <el-card class="map-card">
            <template #header>
              <div class="map-header">
                <h3>地图视图</h3>
                <div class="map-controls">
                  <el-button-group size="small">
                    <el-button 
                      :type="mapView === 'map' ? 'primary' : 'default'"
                      @click="mapView = 'map'"
                    >
                      地图
                    </el-button>
                    <el-button 
                      :type="mapView === 'satellite' ? 'primary' : 'default'"
                      @click="mapView = 'satellite'"
                    >
                      卫星
                    </el-button>
                  </el-button-group>
                </div>
              </div>
            </template>
            
            <div class="map-container">
              <HouseMap 
                :houses="searchResults"
                :center-location="centerLocation"
                :search-radius="searchRadius"
                @house-selected="handleHouseSelected"
              />
            </div>
          </el-card>
        </el-col>

        <!-- 搜索结果 -->
        <el-col :xs="24" :lg="8">
          <el-card class="results-card">
            <template #header>
              <div class="results-header">
                <h3>搜索结果</h3>
                <el-badge :value="searchResults.length" type="primary">
                  <el-button size="small" type="text">
                    <el-icon><House /></el-icon>
                  </el-button>
                </el-badge>
              </div>
            </template>

            <div class="results-content">
              <!-- 搜索统计 -->
              <div class="search-stats">
                <div class="stat-item">
                  <span class="stat-label">找到房屋</span>
                  <span class="stat-value">{{ searchResults.length }} 个</span>
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

              <!-- 房屋列表 -->
              <div class="houses-list" v-loading="searchLoading">
                <div 
                  v-for="house in searchResults"
                  :key="house.id"
                  class="house-item"
                  :class="{ 'selected': selectedHouse?.id === house.id }"
                  @click="selectHouse(house)"
                >
                  <div class="house-image">
                    <img :src="house.imageUrl" :alt="house.address" />
                  </div>
                  <div class="house-info">
                    <h4>{{ house.address }}</h4>
                    <p class="house-location">{{ house.city }}, {{ house.state }} {{ house.zipCode }}</p>
                    <div class="house-price">${{ formatPrice(house.price) }}</div>
                    <div class="house-details">
                      <span>{{ house.bedrooms }}床</span>
                      <span>{{ house.bathrooms }}卫</span>
                      <span>{{ formatArea(house.areaSqft) }}</span>
                    </div>
                    <div class="house-distance" v-if="house.distance">
                      距离: {{ house.distance.toFixed(2) }} 公里
                    </div>
                  </div>
                  <div class="house-actions">
                    <el-button size="small" @click.stop="goToHouseDetail(house.id)">
                      详情
                    </el-button>
                    <el-button size="small" type="primary" @click.stop="centerOnHouse(house)">
                      定位
                    </el-button>
                  </div>
                </div>

                <!-- 空状态 -->
                <div v-if="!searchLoading && searchResults.length === 0" class="empty-results">
                  <el-empty description="没有找到符合条件的房屋">
                    <el-button type="primary" @click="resetFilters">
                      调整搜索条件
                    </el-button>
                  </el-empty>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 房屋详情弹窗 -->
    <el-dialog
      v-model="showHouseDetail"
      :title="selectedHouse?.address"
      width="800px"
    >
      <div v-if="selectedHouse" class="house-detail-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="detail-image">
              <img :src="selectedHouse.imageUrl" :alt="selectedHouse.address" />
            </div>
          </el-col>
          <el-col :span="12">
            <div class="detail-info">
              <div class="detail-price">${{ formatPrice(selectedHouse.price) }}</div>
              <div class="detail-location">{{ selectedHouse.city }}, {{ selectedHouse.state }} {{ selectedHouse.zipCode }}</div>
              <div class="detail-specs">
                <div class="spec-item">
                  <el-icon><Bed /></el-icon>
                  <span>{{ selectedHouse.bedrooms }} 卧室</span>
                </div>
                <div class="spec-item">
                  <el-icon><Bath /></el-icon>
                  <span>{{ selectedHouse.bathrooms }} 卫生间</span>
                </div>
                <div class="spec-item">
                  <el-icon><Expand /></el-icon>
                  <span>{{ formatArea(selectedHouse.areaSqft) }}</span>
                </div>
                <div class="spec-item">
                  <el-icon><OfficeBuilding /></el-icon>
                  <span>{{ selectedHouse.houseType }}</span>
                </div>
              </div>
              <div v-if="selectedHouse.distance" class="detail-distance">
                <el-icon><Location /></el-icon>
                <span>距离搜索中心: {{ selectedHouse.distance.toFixed(2) }} 公里</span>
              </div>
              <div class="detail-actions">
                <el-button type="primary" @click="goToHouseDetail(selectedHouse.id)">
                  查看完整详情
                </el-button>
                <el-button @click="centerOnHouse(selectedHouse)">
                  在地图中查看
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHousesStore } from '../stores/houses'
import HouseMap from '../components/HouseMap.vue'

const router = useRouter()
const housesStore = useHousesStore()

// 响应式数据
const searchLocation = ref('Irvine, CA')
const searchRadius = ref(5)
const priceRange = ref([500000, 2000000])
const selectedTypes = ref(['House', 'Condo', 'Townhouse'])
const minBedrooms = ref(null)
const minBathrooms = ref(null)
const mapView = ref('map')
const searchResults = ref([])
const searchLoading = ref(false)
const selectedHouse = ref(null)
const showHouseDetail = ref(false)
const centerLocation = ref({ lat: 33.6846, lng: -117.8265 })

// 计算属性
const averagePrice = computed(() => {
  if (!searchResults.value.length) return 0
  const total = searchResults.value.reduce((sum, house) => sum + (house.price || 0), 0)
  return Math.round(total / searchResults.value.length)
})

const minPrice = computed(() => {
  if (!searchResults.value.length) return 0
  return Math.min(...searchResults.value.map(h => h.price || 0))
})

const maxPrice = computed(() => {
  if (!searchResults.value.length) return 0
  return Math.max(...searchResults.value.map(h => h.price || 0))
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

const formatRadius = (value) => {
  return `${value} 公里`
}

const searchByLocation = async () => {
  if (!searchLocation.value.trim()) {
    ElMessage.warning('请输入搜索位置')
    return
  }

  // 模拟地理位置解析
  centerLocation.value = { lat: 33.6846, lng: -117.8265 }
  ElMessage.success(`已定位到: ${searchLocation.value}`)
  await performSearch()
}

const performSearch = async () => {
  searchLoading.value = true
  
  try {
    // 获取所有房屋数据
    await housesStore.fetchHouses()
    let results = [...housesStore.houses]

    // 应用筛选条件
    results = results.filter(house => {
      // 价格筛选
      if (priceRange.value[0] && house.price < priceRange.value[0]) return false
      if (priceRange.value[1] && house.price > priceRange.value[1]) return false

      // 房屋类型筛选
      if (selectedTypes.value.length > 0 && !selectedTypes.value.includes(house.houseType)) {
        return false
      }

      // 卧室数量筛选
      if (minBedrooms.value && house.bedrooms < minBedrooms.value) return false

      // 卫生间数量筛选
      if (minBathrooms.value && house.bathrooms < minBathrooms.value) return false

      return true
    })

    // 计算距离（模拟）
    results = results.map(house => ({
      ...house,
      distance: calculateDistance(centerLocation.value.lat, centerLocation.value.lng, house.latitude, house.longitude)
    }))

    // 按距离排序
    results.sort((a, b) => a.distance - b.distance)

    // 应用半径筛选
    results = results.filter(house => house.distance <= searchRadius.value)

    searchResults.value = results
    ElMessage.success(`找到 ${results.length} 个符合条件的房屋`)
    
  } catch (error) {
    ElMessage.error('搜索失败：' + error.message)
  } finally {
    searchLoading.value = false
  }
}

const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371 // 地球半径（公里）
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng/2) * Math.sin(dLng/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}

const resetFilters = () => {
  searchLocation.value = 'Irvine, CA'
  searchRadius.value = 5
  priceRange.value = [500000, 2000000]
  selectedTypes.value = ['House', 'Condo', 'Townhouse']
  minBedrooms.value = null
  minBathrooms.value = null
  searchResults.value = []
  centerLocation.value = { lat: 33.6846, lng: -117.8265 }
}

const selectHouse = (house) => {
  selectedHouse.value = house
  showHouseDetail.value = true
}

const goToHouseDetail = (id) => {
  router.push(`/houses/${id}`)
}

const centerOnHouse = (house) => {
  centerLocation.value = { lat: house.latitude, lng: house.longitude }
  showHouseDetail.value = false
  ElMessage.success(`已定位到 ${house.address}`)
}

const handleHouseSelected = (house) => {
  selectHouse(house)
}

// 生命周期
onMounted(async () => {
  await performSearch()
})
</script>

<style scoped>
.search-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 16px;
}

.page-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

/* 搜索控制面板 */
.search-controls {
  margin-bottom: 30px;
}

.control-card {
  border-radius: 12px;
}

.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  align-items: end;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-group label {
  font-weight: 500;
  color: #5a6c7d;
  font-size: 0.9rem;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.range-separator {
  color: #7f8c8d;
  font-weight: 500;
}

.radius-label {
  text-align: center;
  color: #667eea;
  font-weight: 600;
  margin-top: 4px;
}

.control-actions {
  display: flex;
  gap: 12px;
  grid-column: 1 / -1;
  justify-content: center;
  margin-top: 10px;
}

/* 搜索结果 */
.search-results {
  margin-bottom: 40px;
}

.map-card,
.results-card {
  height: 600px;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.map-header h3 {
  margin: 0;
  color: #2c3e50;
}

.map-container {
  height: 520px;
  border-radius: 8px;
  overflow: hidden;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-header h3 {
  margin: 0;
  color: #2c3e50;
}

.results-content {
  height: 520px;
  overflow-y: auto;
}

/* 搜索统计 */
.search-stats {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  color: #2c3e50;
  font-weight: 600;
}

/* 房屋列表 */
.houses-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.house-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.house-item:hover {
  border-color: #667eea;
  background: #f8fafc;
}

.house-item.selected {
  border-color: #667eea;
  background: #f0f9ff;
}

.house-image {
  width: 80px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.house-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.house-info {
  flex: 1;
}

.house-info h4 {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: 600;
}

.house-location {
  color: #7f8c8d;
  font-size: 0.8rem;
  margin-bottom: 4px;
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
  margin-bottom: 4px;
}

.house-distance {
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 500;
}

.house-actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-self: flex-start;
}

.empty-results {
  text-align: center;
  padding: 40px 20px;
}

/* 房屋详情弹窗 */
.house-detail-content {
  padding: 20px 0;
}

.detail-image {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
}

.detail-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.detail-info {
  padding: 0 20px;
}

.detail-price {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.detail-location {
  color: #7f8c8d;
  margin-bottom: 16px;
}

.detail-specs {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #5a6c7d;
}

.spec-item .el-icon {
  color: #667eea;
}

.detail-distance {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: 500;
  margin-bottom: 20px;
}

.detail-actions {
  display: flex;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .map-card,
  .results-card {
    height: 500px;
  }
  
  .map-container {
    height: 420px;
  }
  
  .results-content {
    height: 420px;
  }
}

@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
  }
  
  .control-actions {
    flex-direction: column;
  }
  
  .house-item {
    flex-direction: column;
  }
  
  .house-image {
    width: 100%;
    height: 120px;
  }
  
  .house-actions {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .detail-actions {
    flex-direction: column;
  }
}
</style>
