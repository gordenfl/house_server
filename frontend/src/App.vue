<template>
  <div id="app">
    <el-container>
      <!-- 头部导航 -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon class="logo-icon"><House /></el-icon>
            <span class="logo-text">House Server</span>
            <span class="location">Irvine, CA</span>
          </div>
          
          <el-menu
            mode="horizontal"
            :default-active="activeIndex"
            class="header-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="home">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="houses">
              <el-icon><House /></el-icon>
              <span>房屋列表</span>
            </el-menu-item>
            <el-menu-item index="search">
              <el-icon><Search /></el-icon>
              <span>地图搜索</span>
            </el-menu-item>
            <el-menu-item index="analytics">
              <el-icon><TrendCharts /></el-icon>
              <span>数据分析</span>
            </el-menu-item>
          </el-menu>

          <div class="user-actions">
            <el-button v-if="!isLoggedIn" @click="showLogin = true" type="primary">
              <el-icon><User /></el-icon>
              登录
            </el-button>
            <el-dropdown v-else>
              <el-button type="text">
                <el-icon><User /></el-icon>
                {{ userInfo.username }}
                <el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToProfile">个人资料</el-dropdown-item>
                  <el-dropdown-item v-if="isAdmin" @click="goToAdmin">管理后台</el-dropdown-item>
                  <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <!-- 主要内容区域 -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- 页脚 -->
      <el-footer class="app-footer">
        <div class="footer-content">
          <p>&copy; 2024 House Server - Irvine CA Real Estate Management System</p>
          <div class="footer-links">
            <a href="#" @click.prevent>关于我们</a>
            <a href="#" @click.prevent>联系我们</a>
            <a href="#" @click.prevent>隐私政策</a>
          </div>
        </div>
      </el-footer>
    </el-container>

    <!-- 登录对话框 -->
    <el-dialog v-model="showLogin" title="用户登录" width="400px">
      <el-form :model="loginForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showLogin = false">取消</el-button>
        <el-button type="primary" @click="handleLogin" :loading="loginLoading">登录</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from './stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 响应式数据
const showLogin = ref(false)
const loginForm = ref({
  username: '',
  password: ''
})
const loginLoading = ref(false)

// 计算属性
const activeIndex = computed(() => {
  const path = route.path
  if (path === '/') return 'home'
  if (path.startsWith('/houses')) return 'houses'
  if (path.startsWith('/search')) return 'search'
  if (path.startsWith('/analytics')) return 'analytics'
  return 'home'
})

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userInfo = computed(() => userStore.userInfo)
const isAdmin = computed(() => userStore.userInfo?.role === 'ADMIN')

// 方法
const handleMenuSelect = (index) => {
  switch (index) {
    case 'home':
      router.push('/')
      break
    case 'houses':
      router.push('/houses')
      break
    case 'search':
      router.push('/search')
      break
    case 'analytics':
      router.push('/analytics')
      break
  }
}

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loginLoading.value = true
  try {
    await userStore.login(loginForm.value.username, loginForm.value.password)
    ElMessage.success('登录成功')
    showLogin.value = false
    loginForm.value = { username: '', password: '' }
  } catch (error) {
    ElMessage.error('登录失败：' + (error.message || '用户名或密码错误'))
  } finally {
    loginLoading.value = false
  }
}

const goToProfile = () => {
  router.push('/profile')
}

const goToAdmin = () => {
  router.push('/admin')
}

const logout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

// 生命周期
onMounted(() => {
  userStore.checkAuth()
})
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  color: white;
}

.location {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: normal;
  margin-left: 8px;
}

.header-menu {
  background: transparent;
  border: none;
}

.header-menu .el-menu-item {
  color: white;
  border-bottom: 2px solid transparent;
}

.header-menu .el-menu-item:hover,
.header-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-bottom-color: white;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-main {
  min-height: calc(100vh - 120px);
  padding: 20px;
  background: #f5f7fa;
}

.app-footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 10px;
    padding: 10px;
  }
  
  .header-menu {
    width: 100%;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
