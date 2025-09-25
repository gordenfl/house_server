import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useHousesStore = defineStore('houses', () => {
  // 状态
  const houses = ref([])
  const currentHouse = ref(null)
  const loading = ref(false)
  const total = ref(0)
  const filters = ref({
    city: 'Irvine',
    state: 'CA',
    minPrice: null,
    maxPrice: null,
    minBedrooms: null,
    minBathrooms: null,
    houseType: null,
    houseStatus: null
  })
  const pagination = ref({
    page: 1,
    pageSize: 12,
    total: 0
  })

  // 计算属性
  const filteredHouses = computed(() => {
    let result = houses.value

    if (filters.value.minPrice) {
      result = result.filter(house => house.price >= filters.value.minPrice)
    }
    if (filters.value.maxPrice) {
      result = result.filter(house => house.price <= filters.value.maxPrice)
    }
    if (filters.value.minBedrooms) {
      result = result.filter(house => house.bedrooms >= filters.value.minBedrooms)
    }
    if (filters.value.minBathrooms) {
      result = result.filter(house => house.bathrooms >= filters.value.minBathrooms)
    }
    if (filters.value.houseType) {
      result = result.filter(house => house.houseType === filters.value.houseType)
    }
    if (filters.value.houseStatus) {
      result = result.filter(house => house.houseStatus === filters.value.houseStatus)
    }

    return result
  })

  const houseStats = computed(() => {
    if (!houses.value.length) return null

    const prices = houses.value.map(h => h.price).filter(p => p)
    const bedrooms = houses.value.map(h => h.bedrooms).filter(b => b)
    const bathrooms = houses.value.map(h => h.bathrooms).filter(b => b)

    return {
      total: houses.value.length,
      avgPrice: prices.length ? Math.round(prices.reduce((a, b) => a + b, 0) / prices.length) : 0,
      minPrice: prices.length ? Math.min(...prices) : 0,
      maxPrice: prices.length ? Math.max(...prices) : 0,
      avgBedrooms: bedrooms.length ? Math.round((bedrooms.reduce((a, b) => a + b, 0) / bedrooms.length) * 10) / 10 : 0,
      avgBathrooms: bathrooms.length ? Math.round((bathrooms.reduce((a, b) => a + b, 0) / bathrooms.length) * 10) / 10 : 0,
      houseTypes: houses.value.reduce((acc, house) => {
        acc[house.houseType] = (acc[house.houseType] || 0) + 1
        return acc
      }, {})
    }
  })

  // 动作
  const fetchHouses = async (params = {}) => {
    loading.value = true
    try {
      const response = await api.get('/houses', { params })
      houses.value = response.data || []
      total.value = response.data?.length || 0
      pagination.value.total = total.value
      return response.data
    } catch (error) {
      console.error('获取房屋列表失败:', error)
      // 使用模拟数据
      houses.value = getMockHouses()
      total.value = houses.value.length
      pagination.value.total = total.value
      return houses.value
    } finally {
      loading.value = false
    }
  }

  const fetchHouseById = async (id) => {
    loading.value = true
    try {
      const response = await api.get(`/houses/${id}`)
      currentHouse.value = response.data
      return response.data
    } catch (error) {
      console.error('获取房屋详情失败:', error)
      // 使用模拟数据
      currentHouse.value = getMockHouses().find(h => h.id == id)
      return currentHouse.value
    } finally {
      loading.value = false
    }
  }

  const searchHousesByLocation = async (searchParams) => {
    loading.value = true
    try {
      const response = await api.post('/houses/search/location', searchParams)
      houses.value = response.data?.map(item => item.house) || []
      return response.data
    } catch (error) {
      console.error('地理位置搜索失败:', error)
      // 使用模拟数据
      houses.value = getMockHouses().filter(house => {
        const distance = calculateDistance(
          searchParams.latitude,
          searchParams.longitude,
          house.latitude,
          house.longitude
        )
        return distance <= searchParams.radiusKm
      })
      return houses.value
    } finally {
      loading.value = false
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1
  }

  const resetFilters = () => {
    filters.value = {
      city: 'Irvine',
      state: 'CA',
      minPrice: null,
      maxPrice: null,
      minBedrooms: null,
      minBathrooms: null,
      houseType: null,
      houseStatus: null
    }
    pagination.value.page = 1
  }

  // 模拟数据（当API不可用时使用）
  const getMockHouses = () => {
    return [
      {
        id: 1,
        address: "123 Harvard Ave",
        city: "Irvine",
        state: "CA",
        zipCode: "92614",
        latitude: 33.6846,
        longitude: -117.8265,
        houseType: "House",
        areaSqft: 2500,
        lotAreaSqft: 8000,
        houseStatus: "FOR_SALE",
        buildYear: 2010,
        bathrooms: 3.0,
        bedrooms: 4,
        price: 1200000,
        description: "Beautiful single-family home in Irvine with modern amenities",
        imageUrl: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400",
        createdAt: "2024-01-01T00:00:00Z"
      },
      {
        id: 2,
        address: "456 Yale Loop",
        city: "Irvine",
        state: "CA",
        zipCode: "92620",
        latitude: 33.6900,
        longitude: -117.8200,
        houseType: "Condo",
        areaSqft: 1800,
        lotAreaSqft: 0,
        houseStatus: "FOR_SALE",
        buildYear: 2015,
        bathrooms: 2.5,
        bedrooms: 3,
        price: 850000,
        description: "Modern condominium with updated kitchen and bathrooms",
        imageUrl: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=400",
        createdAt: "2024-01-01T00:00:00Z"
      },
      {
        id: 3,
        address: "789 Stanford Dr",
        city: "Irvine",
        state: "CA",
        zipCode: "92612",
        latitude: 33.6750,
        longitude: -117.8350,
        houseType: "House",
        areaSqft: 3200,
        lotAreaSqft: 12000,
        houseStatus: "FOR_SALE",
        buildYear: 2008,
        bathrooms: 4.0,
        bedrooms: 5,
        price: 1500000,
        description: "Spacious family home with pool and large backyard",
        imageUrl: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400",
        createdAt: "2024-01-01T00:00:00Z"
      },
      {
        id: 4,
        address: "321 MIT Way",
        city: "Irvine",
        state: "CA",
        zipCode: "92618",
        latitude: 33.6800,
        longitude: -117.8150,
        houseType: "Townhouse",
        areaSqft: 2200,
        lotAreaSqft: 4000,
        houseStatus: "FOR_SALE",
        buildYear: 2012,
        bathrooms: 2.5,
        bedrooms: 3,
        price: 950000,
        description: "Charming townhouse with private garage and courtyard",
        imageUrl: "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=400",
        createdAt: "2024-01-01T00:00:00Z"
      },
      {
        id: 5,
        address: "654 Berkeley St",
        city: "Irvine",
        state: "CA",
        zipCode: "92617",
        latitude: 33.6850,
        longitude: -117.8250,
        houseType: "House",
        areaSqft: 2800,
        lotAreaSqft: 9000,
        houseStatus: "FOR_SALE",
        buildYear: 2018,
        bathrooms: 3.5,
        bedrooms: 4,
        price: 1350000,
        description: "New construction home with smart home features",
        imageUrl: "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=400",
        createdAt: "2024-01-01T00:00:00Z"
      }
    ]
  }

  // 计算距离（公里）
  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371 // 地球半径（公里）
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLon = (lon2 - lon1) * Math.PI / 180
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    return R * c
  }

  return {
    // 状态
    houses,
    currentHouse,
    loading,
    total,
    filters,
    pagination,
    
    // 计算属性
    filteredHouses,
    houseStats,
    
    // 动作
    fetchHouses,
    fetchHouseById,
    searchHousesByLocation,
    updateFilters,
    resetFilters
  }
})
