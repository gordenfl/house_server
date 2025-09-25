<template>
  <div class="houses-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1>Irvine房屋列表</h1>
      <p>发现最适合您的理想家园</p>
    </div>

    <!-- 筛选器 -->
    <div class="filters-section">
      <el-card class="filter-card">
        <div class="filters-grid">
          <div class="filter-group">
            <label>价格范围</label>
            <div class="price-range">
              <el-input
                v-model.number="filters.minPrice"
                placeholder="最低价格"
                type="number"
                @input="handleFilterChange"
              >
                <template #prepend>$</template>
              </el-input>
              <span class="range-separator">-</span>
              <el-input
                v-model.number="filters.maxPrice"
                placeholder="最高价格"
                type="number"
                @input="handleFilterChange"
              >
                <template #prepend>$</template>
              </el-input>
            </div>
          </div>

          <div class="filter-group">
            <label>卧室数量</label>
            <el-select
              v-model="filters.minBedrooms"
              placeholder="最少卧室"
              @change="handleFilterChange"
              clearable
            >
              <el-option label="不限" :value="null" />
              <el-option label="1+" :value="1" />
              <el-option label="2+" :value="2" />
              <el-option label="3+" :value="3" />
              <el-option label="4+" :value="4" />
              <el-option label="5+" :value="5" />
            </el-select>
          </div>

          <div class="filter-group">
            <label>卫生间数量</label>
            <el-select
              v-model="filters.minBathrooms"
              placeholder="最少卫生间"
              @change="handleFilterChange"
              clearable
            >
              <el-option label="不限" :value="null" />
              <el-option label="1+" :value="1" />
              <el-option label="1.5+" :value="1.5" />
              <el-option label="2+" :value="2" />
              <el-option label="2.5+" :value="2.5" />
              <el-option label="3+" :value="3" />
              <el-option label="3.5+" :value="3.5" />
              <el-option label="4+" :value="4" />
            </el-select>
          </div>

          <div class="filter-group">
            <label>房屋类型</label>
            <el-select
              v-model="filters.houseType"
              placeholder="选择类型"
              @change="handleFilterChange"
              clearable
            >
              <el-option label="不限" :value="null" />
              <el-option label="House" value="House" />
              <el-option label="Condo" value="Condo" />
              <el-option label="Townhouse" value="Townhouse" />
            </el-select>
          </div>

          <div class="filter-group">
            <label>房屋状态</label>
            <el-select
              v-model="filters.houseStatus"
              placeholder="选择状态"
              @change="handleFilterChange"
              clearable
            >
              <el-option label="不限" :value="null" />
              <el-option label="出售中" value="FOR_SALE" />
              <el-option label="已售出" value="SOLD" />
              <el-option label="法拍" value="FORECLOSED" />
            </el-select>
          </div>

          <div class="filter-actions">
            <el-button @click="resetFilters">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
            <el-button type="primary" @click="applyFilters">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 结果统计 -->
    <div class="results-header">
      <div class="results-info">
        <h3>找到 {{ filteredHouses.length }} 个符合条件的房屋</h3>
        <div class="view-options">
          <el-radio-group v-model="viewMode" size="small">
            <el-radio-button label="grid">
              <el-icon><Grid /></el-icon>
              网格视图
            </el-radio-button>
            <el-radio-button label="list">
              <el-icon><List /></el-icon>
              列表视图
            </el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="sort-options">
        <el-select v-model="sortBy" placeholder="排序方式" @change="handleSortChange">
          <el-option label="价格从低到高" value="price-asc" />
          <el-option label="价格从高到低" value="price-desc" />
          <el-option label="面积从大到小" value="area-desc" />
          <el-option label="面积从小到大" value="area-asc" />
          <el-option label="卧室数量" value="bedrooms-desc" />
        </el-select>
      </div>
    </div>

    <!-- 房屋列表 -->
    <div class="houses-container" v-loading="loading">
      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="houses-grid">
        <div
          v-for="house in sortedHouses"
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
            <div class="house-meta">
              <span class="house-type">{{ house.houseType }}</span>
              <span v-if="house.buildYear" class="build-year">{{ house.buildYear }}年建</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-else class="houses-list">
        <div
          v-for="house in sortedHouses"
          :key="house.id"
          class="house-list-item"
          @click="goToHouseDetail(house.id)"
        >
          <div class="house-image">
            <img :src="house.imageUrl" :alt="house.address" />
          </div>
          <div class="house-content">
            <div class="house-header">
              <h3 class="house-address">{{ house.address }}</h3>
              <div class="house-price">${{ formatPrice(house.price) }}</div>
            </div>
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
              <span class="detail-item">
                <el-icon><OfficeBuilding /></el-icon>
                {{ house.houseType }}
              </span>
            </div>
            <div class="house-footer">
              <div class="house-status" :class="house.houseStatus.toLowerCase()">
                {{ getStatusText(house.houseStatus) }}
              </div>
              <span v-if="house.buildYear" class="build-year">{{ house.buildYear }}年建</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && sortedHouses.length === 0" class="empty-state">
        <el-empty description="没有找到符合条件的房屋">
          <el-button type="primary" @click="resetFilters">清除筛选条件</el-button>
        </el-empty>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="sortedHouses.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 48]"
        :total="sortedHouses.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHousesStore } from '../stores/houses'

const router = useRouter()
const housesStore = useHousesStore()

// 响应式数据
const loading = ref(false)
const viewMode = ref('grid')
const sortBy = ref('price-asc')
const currentPage = ref(1)
const pageSize = ref(12)

const filters = ref({
  minPrice: null,
  maxPrice: null,
  minBedrooms: null,
  minBathrooms: null,
  houseType: null,
  houseStatus: null
})

// 计算属性
const filteredHouses = computed(() => {
  return housesStore.filteredHouses
})

const sortedHouses = computed(() => {
  let houses = [...filteredHouses.value]
  
  switch (sortBy.value) {
    case 'price-asc':
      houses.sort((a, b) => (a.price || 0) - (b.price || 0))
      break
    case 'price-desc':
      houses.sort((a, b) => (b.price || 0) - (a.price || 0))
      break
    case 'area-desc':
      houses.sort((a, b) => (b.areaSqft || 0) - (a.areaSqft || 0))
      break
    case 'area-asc':
      houses.sort((a, b) => (a.areaSqft || 0) - (b.areaSqft || 0))
      break
    case 'bedrooms-desc':
      houses.sort((a, b) => (b.bedrooms || 0) - (a.bedrooms || 0))
      break
  }
  
  return houses
})

const paginatedHouses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return sortedHouses.value.slice(start, end)
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

const getStatusText = (status) => {
  const statusMap = {
    'FOR_SALE': '出售中',
    'SOLD': '已售出',
    'FORECLOSED': '法拍'
  }
  return statusMap[status] || status
}

const handleFilterChange = () => {
  housesStore.updateFilters(filters.value)
}

const applyFilters = () => {
  housesStore.updateFilters(filters.value)
}

const resetFilters = () => {
  filters.value = {
    minPrice: null,
    maxPrice: null,
    minBedrooms: null,
    minBathrooms: null,
    houseType: null,
    houseStatus: null
  }
  housesStore.resetFilters()
}

const handleSortChange = () => {
  // 排序变化时重置到第一页
  currentPage.value = 1
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
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

// 监听筛选器变化
watch(filters, () => {
  handleFilterChange()
}, { deep: true })
</script>

<style scoped>
.houses-page {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
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

/* 筛选器 */
.filters-section {
  margin-bottom: 30px;
}

.filter-card {
  border-radius: 12px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
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

.filter-actions {
  display: flex;
  gap: 12px;
  align-items: end;
}

/* 结果头部 */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 1px solid #e5e7eb;
}

.results-info h3 {
  color: #2c3e50;
  margin-bottom: 12px;
}

.view-options {
  margin-top: 12px;
}

/* 房屋网格 */
.houses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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

.house-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.house-type {
  background: #f0f9ff;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.build-year {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* 房屋列表 */
.houses-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.house-list-item {
  display: flex;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.house-list-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.house-list-item .house-image {
  width: 200px;
  height: 150px;
  flex-shrink: 0;
}

.house-list-item .house-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.house-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.house-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.house-list-item .house-price {
  background: none;
  color: #667eea;
  font-size: 1.5rem;
  font-weight: bold;
  position: static;
  padding: 0;
}

.house-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.house-list-item .house-status {
  position: static;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .houses-grid {
    grid-template-columns: 1fr;
  }
  
  .house-list-item {
    flex-direction: column;
  }
  
  .house-list-item .house-image {
    width: 100%;
    height: 200px;
  }
  
  .house-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .house-list-item .house-price {
    font-size: 1.2rem;
  }
}
</style>
