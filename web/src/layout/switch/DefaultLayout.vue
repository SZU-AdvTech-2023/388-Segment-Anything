<script setup>
</script>

<template>
  <div>
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
      <el-main>
        <router-view v-slot="{ Component }">
          <component :is="Component" />
        </router-view>
      </el-main>
      <el-footer>
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped>

</style>


