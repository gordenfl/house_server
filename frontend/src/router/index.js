import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/houses',
    name: 'Houses',
    component: () => import('../views/Houses.vue'),
    meta: { title: '房屋列表' }
  },
  {
    path: '/houses/:id',
    name: 'HouseDetail',
    component: () => import('../views/HouseDetail.vue'),
    meta: { title: '房屋详情' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('../views/Search.vue'),
    meta: { title: '地图搜索' }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: () => import('../views/Analytics.vue'),
    meta: { title: '数据分析' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { title: '个人资料', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - House Server Irvine CA`
  
  // 检查认证
  const userStore = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth && !userStore.token) {
    next('/')
    return
  }
  
  if (to.meta.requiresAdmin && userStore.user?.role !== 'ADMIN') {
    next('/')
    return
  }
  
  next()
})

export default router
