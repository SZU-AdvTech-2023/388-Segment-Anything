<script setup>
import { ArrowRight } from '@element-plus/icons'
// 侧边栏收缩状态
const collapsed = ref(false)
</script>

<template>

  <div class="sidebar-layout">
    <el-container>
      <el-header style="border-bottom: 1px solid #eee;">
        <navbar>
          <template #left>
            <Logo></Logo>
          </template>
          <template #center>
            <div style="height:100%;display: flex;">
              <p style="display: flex;cursor: pointer;align-items: center;">手术导航系统</p>
            </div>
          </template>
        </navbar>
      </el-header>
      <el-container>
        <Menu mode="vertical" :collapsed="collapsed" />
        <div :class="[collapsed ? 'icon2' : 'icon']">
          <el-icon v-model="collapsed" @click="collapsed = !collapsed" class="arrowRight">
            <ArrowRight />
          </el-icon>
        </div>

        <el-main>
          <router-view v-slot="{ Component }">
            <component :is="Component" />
          </router-view>
        </el-main>

      </el-container>
    </el-container>

  </div>
</template>

<style scoped>
.icon {
  transition: all 0.3s ease;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99;
  border-top: 1px solid #eee;
  position: fixed;
  bottom: 5px;
  font-size: 20px;
  width: 200px;
}

.icon2 {
  transition: all 0.3s ease;
  height: 30px;
  z-index: 99;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 1px solid #eee;
  position: fixed;
  bottom: 5px;
  font-size: 20px;
  width: 63px;
}
</style>


