import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const userInfo = computed(() => user.value)

  // 动作
  const login = async (username, password) => {
    loading.value = true
    try {
      const response = await api.post('/users/login', {
        username,
        password
      })
      
      const { token: userToken, user: userData } = response.data
      
      token.value = userToken
      user.value = userData
      
      // 保存到本地存储
      localStorage.setItem('user', JSON.stringify({
        token: userToken,
        user: userData
      }))
      
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || '登录失败')
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
  }

  const checkAuth = () => {
    const stored = localStorage.getItem('user')
    if (stored) {
      try {
        const { token: storedToken, user: storedUser } = JSON.parse(stored)
        if (storedToken && storedUser) {
          token.value = storedToken
          user.value = storedUser
        }
      } catch (error) {
        localStorage.removeItem('user')
      }
    }
  }

  const updateProfile = async (userData) => {
    loading.value = true
    try {
      const response = await api.put(`/users/${user.value.id}`, userData)
      user.value = { ...user.value, ...response.data }
      
      // 更新本地存储
      localStorage.setItem('user', JSON.stringify({
        token: token.value,
        user: user.value
      }))
      
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || '更新失败')
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (newPassword) => {
    loading.value = true
    try {
      await api.post(`/users/${user.value.id}/change-password`, {
        newPassword
      })
      return true
    } catch (error) {
      throw new Error(error.response?.data?.error || '密码修改失败')
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    user,
    token,
    loading,
    
    // 计算属性
    isLoggedIn,
    userInfo,
    
    // 动作
    login,
    logout,
    checkAuth,
    updateProfile,
    changePassword
  }
})
