<template>
  <div class="not-found-page">
    <div class="error-container">
      <div class="error-content">
        <div class="error-code">404</div>
        <h1 class="error-title">页面未找到</h1>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移除。
        </p>
        <div class="error-actions">
          <el-button type="primary" size="large" @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
          <el-button size="large" @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
      </div>
      <div class="error-illustration">
        <div class="house-illustration">
          <div class="house">
            <div class="roof"></div>
            <div class="walls">
              <div class="door"></div>
              <div class="windows">
                <div class="window"></div>
                <div class="window"></div>
              </div>
            </div>
          </div>
          <div class="question-mark">?</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.error-container {
  max-width: 800px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.error-content {
  text-align: left;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #667eea;
  line-height: 1;
  margin-bottom: 20px;
  text-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.error-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 16px;
  font-weight: 600;
}

.error-description {
  font-size: 1.1rem;
  color: #7f8c8d;
  line-height: 1.6;
  margin-bottom: 40px;
}

.error-actions {
  display: flex;
  gap: 16px;
}

.error-illustration {
  display: flex;
  justify-content: center;
  align-items: center;
}

.house-illustration {
  position: relative;
  width: 200px;
  height: 200px;
}

.house {
  position: relative;
  width: 120px;
  height: 100px;
  margin: 0 auto;
}

.roof {
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-bottom: 40px solid #e74c3c;
  position: relative;
}

.roof::before {
  content: '';
  position: absolute;
  top: 40px;
  left: -60px;
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-bottom: 30px solid #c0392b;
}

.walls {
  width: 100%;
  height: 60px;
  background: #3498db;
  position: relative;
  border-radius: 0 0 8px 8px;
}

.door {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 40px;
  background: #8b4513;
  border-radius: 10px 10px 0 0;
}

.windows {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}

.window {
  width: 15px;
  height: 15px;
  background: #87ceeb;
  border: 2px solid #4682b4;
  border-radius: 2px;
}

.question-mark {
  position: absolute;
  top: -20px;
  right: -20px;
  font-size: 4rem;
  color: #f39c12;
  font-weight: bold;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .error-container {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .error-content {
    text-align: center;
  }
  
  .error-code {
    font-size: 6rem;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .house-illustration {
    width: 150px;
    height: 150px;
  }
  
  .house {
    width: 90px;
    height: 75px;
  }
  
  .roof {
    border-left: 45px solid transparent;
    border-right: 45px solid transparent;
    border-bottom: 30px solid #e74c3c;
  }
  
  .roof::before {
    top: 30px;
    left: -45px;
    border-left: 45px solid transparent;
    border-right: 45px solid transparent;
    border-bottom: 22px solid #c0392b;
  }
  
  .walls {
    height: 45px;
  }
}
</style>
